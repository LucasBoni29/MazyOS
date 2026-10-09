"""
Legenda estilo TikTok: cada palavra muda de branco pra amarelo no momento em que é falada.

Duas etapas, com revisão humana no meio:

  1) transcrever — gera <video>.legenda.txt pra revisar
     python legendar_video.py transcrever <video.mp4>

  2) gravar — lê o .txt revisado e grava a legenda no vídeo
     python legendar_video.py gravar <video.mp4>
     -> <video>-legendado.mp4

Formato do .txt (editável à mão):
  [00:01.20 - 00:02.40] cara olha o chão
  [00:02.50 - 00:03.10] vai cair
Pode corrigir palavras, apagar linhas inteiras ou ajustar os tempos.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

MODELO = "large-v3-turbo"
MAX_PALAVRAS = 3
MAX_DURACAO = 1.6
PAUSA_QUEBRA = 0.6

LINHA_RE = re.compile(r"^\[(\d+):(\d+(?:\.\d+)?)\s*-\s*(\d+):(\d+(?:\.\d+)?)\]\s*(.*)$")


def caminhos(video: Path):
    base = video.with_suffix("")
    return {
        "txt": Path(f"{base}.legenda.txt"),
        "palavras": Path(f"{base}.palavras.json"),
        "ass": Path(f"{base}.legenda.ass"),
        "saida": Path(f"{base}-legendado.mp4"),
    }


def fmt_txt(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


def fmt_ass(t: float) -> str:
    h, resto = divmod(t, 3600)
    m, s = divmod(resto, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def agrupar(palavras):
    blocos, atual = [], []
    for p in palavras:
        if atual and (
            len(atual) >= MAX_PALAVRAS
            or atual[-1]["texto"][-1] in ".!?"
            or p["inicio"] - atual[-1]["fim"] > PAUSA_QUEBRA
            or p["fim"] - atual[0]["inicio"] > MAX_DURACAO
        ):
            blocos.append(atual)
            atual = []
        atual.append(p)
    if atual:
        blocos.append(atual)
    return blocos


def carregar_audio(video: Path):
    # Áudio via ffmpeg em vez do decoder embutido do faster-whisper (PyAV 19 quebra a API que ele usa)
    import numpy as np

    cmd = ["ffmpeg", "-v", "error", "-i", str(video), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        sys.exit(f"ffmpeg falhou ao extrair o áudio:\n{result.stderr.decode(errors='ignore')[-2000:]}")
    return np.frombuffer(result.stdout, dtype=np.float32)


def transcrever(video: Path):
    from faster_whisper import WhisperModel

    paths = caminhos(video)
    print(f"Carregando modelo {MODELO} (na primeira vez baixa ~1.6GB)...")
    modelo = WhisperModel(MODELO, device="cpu", compute_type="int8")
    segmentos, _ = modelo.transcribe(carregar_audio(video), language="pt", word_timestamps=True)

    palavras = []
    for seg in segmentos:
        for w in seg.words or []:
            texto = w.word.strip()
            if texto:
                palavras.append({"texto": texto, "inicio": w.start, "fim": w.end})

    if not palavras:
        sys.exit("Nenhuma fala detectada no vídeo.")

    paths["palavras"].write_text(json.dumps(palavras, ensure_ascii=False, indent=1), encoding="utf-8")
    linhas = [
        f"[{fmt_txt(b[0]['inicio'])} - {fmt_txt(b[-1]['fim'])}] {' '.join(p['texto'] for p in b)}"
        for b in agrupar(palavras)
    ]
    paths["txt"].write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Transcrição pronta pra revisar: {paths['txt']}")


SEG_POR_PALAVRA = 0.3
MIN_DURACAO_POR_PALAVRA = 0.08  # abaixo disso o tempo do Whisper é lixo (vozes sobrepostas, ruído)


def tempos_das_palavras(n_palavras, inicio, fim, limite, originais):
    # Na revisão o usuário junta linhas sem mexer no tempo: o bloco fica com mais palavras do que cabe
    # no intervalo. Se o Whisper ouviu palavras suficientes, usa o tempo real delas. Se ouviu só
    # algumas, espalha todas as palavras dentro do intervalo REAL que ele ouviu.
    # "Ouvidas" é uma cadeia contígua (sem pausa > PAUSA_QUEBRA entre uma palavra e a próxima) —
    # isso evita pegar palavras de uma fala diferente só porque ela caiu antes do próximo bloco escrito.
    ouvidas = []
    for p in originais:
        if p["inicio"] < inicio - 0.05:
            continue
        if p["inicio"] >= limite:
            break
        if ouvidas and p["inicio"] - ouvidas[-1]["fim"] > PAUSA_QUEBRA:
            break
        ouvidas.append(p)

    # Em trechos com vozes sobrepostas o Whisper às vezes cospe palavras com início/fim quase iguais
    # (duração ~0). Se a média de duração das palavras ouvidas for baixa demais, não é tempo real
    # de fala — é ruído, e confiar nele deixa a legenda passando rápido demais pra ler.
    span_real = (ouvidas[-1]["fim"] - ouvidas[0]["inicio"]) if ouvidas else 0.0
    confiavel = bool(ouvidas) and span_real / len(ouvidas) >= MIN_DURACAO_POR_PALAVRA

    if confiavel and len(ouvidas) >= n_palavras:
        return [(p["inicio"], p["fim"]) for p in ouvidas[:n_palavras]]
    if confiavel:
        ini_real = min(inicio, ouvidas[0]["inicio"])
        fim_real = max(fim, ouvidas[-1]["fim"])
    else:
        ini_real, fim_real = inicio, inicio + n_palavras * SEG_POR_PALAVRA
    fim_real = min(limite, fim_real)
    passo = (fim_real - ini_real) / n_palavras
    return [(ini_real + i * passo, ini_real + (i + 1) * passo) for i in range(n_palavras)]


def gerar_ass(paths) -> None:
    originais = []
    if paths["palavras"].exists():
        originais = json.loads(paths["palavras"].read_text(encoding="utf-8"))

    blocos = []
    for n, linha in enumerate(paths["txt"].read_text(encoding="utf-8").splitlines(), start=1):
        linha = linha.strip()
        if not linha:
            continue
        m = LINHA_RE.match(linha)
        if not m:
            sys.exit(f"Linha {n} fora do formato [mm:ss.cc - mm:ss.cc] texto: {linha!r}")
        inicio = int(m.group(1)) * 60 + float(m.group(2))
        fim = int(m.group(3)) * 60 + float(m.group(4))
        texto = m.group(5).split()
        if texto:
            blocos.append((inicio, fim, texto))

    eventos = []
    for i, (inicio, fim, texto) in enumerate(blocos):
        limite = blocos[i + 1][0] if i + 1 < len(blocos) else inicio + 60
        tempos = tempos_das_palavras(len(texto), inicio, fim, limite, originais)
        fim = min(limite, max(fim, tempos[-1][1]))

        partes = []
        cursor = inicio
        for palavra, (p_ini, p_fim) in zip(texto, tempos):
            espera = max(0.0, p_ini - cursor)
            if espera > 0:
                partes.append(f"{{\\k{round(espera * 100)}}}")
            partes.append(f"{{\\k{max(0, round((p_fim - max(p_ini, cursor)) * 100))}}}{palavra.upper()} ")
            cursor = max(cursor, p_fim)
        eventos.append(f"Dialogue: 0,{fmt_ass(inicio)},{fmt_ass(fim)},Fala,,0,0,0,,{''.join(partes).rstrip()}")

    # Cores ASS em &HAABBGGRR: Primary = palavra já falada (amarelo), Secondary = ainda não falada (branco)
    cabecalho = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Fala,Impact,92,&H0000E5FF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,6,3,2,60,60,440,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    paths["ass"].write_text(cabecalho + "\n".join(eventos) + "\n", encoding="utf-8")


def gravar(video: Path):
    paths = caminhos(video)
    if not paths["txt"].exists():
        sys.exit(f"Transcrição não encontrada: {paths['txt']} (rode 'transcrever' primeiro)")
    gerar_ass(paths)

    # O filtro ass do ffmpeg se perde com "D:\" no caminho; rodando dentro da pasta, passa só o nome do arquivo
    cmd = [
        "ffmpeg", "-y", "-i", video.name,
        "-vf", f"ass={paths['ass'].name}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "copy",
        paths["saida"].name,
    ]
    result = subprocess.run(cmd, cwd=video.parent, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"ffmpeg falhou:\n{result.stderr[-3000:]}")
    print(f"Pronto: {paths['saida']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("etapa", choices=["transcrever", "gravar"])
    parser.add_argument("video", type=Path)
    args = parser.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"Vídeo não encontrado: {video}")

    if args.etapa == "transcrever":
        transcrever(video)
    else:
        gravar(video)


if __name__ == "__main__":
    main()
