"""
Corta trechos de um vídeo raw (OBS) a partir de uma lista de timestamps
e concatena tudo num vídeo final montado, via ffmpeg.

Uso:
  python cortar_video.py <raw.mp4> <timestamps.txt> <saida.mp4> [--vertical]

Formato do timestamps.txt — um trecho por linha:
  00:12:30 - 00:13:10
  00:25:00 - 00:26:45
  1:03:10 - 1:04:02

Aceita HH:MM:SS, MM:SS ou SS puro, com ou sem espaço em volta do "-".
--vertical corta o resultado final pra 9:16 (1080x1920), centralizado,
pensado pra TikTok/Shorts. Sem a flag, mantém o formato original (YouTube longo).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def parse_time(token: str) -> float:
    token = token.strip()
    parts = token.split(":")
    parts = [float(p) for p in parts]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    h, m, s = parts
    return h * 3600 + m * 60 + s


def parse_timestamps(path: Path):
    segments = []
    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^(.+?)\s*-\s*(.+)$", line)
        if not match:
            raise ValueError(f"Linha {lineno} inválida (esperado 'inicio - fim'): {raw_line!r}")
        start, end = parse_time(match.group(1)), parse_time(match.group(2))
        if end <= start:
            raise ValueError(f"Linha {lineno}: fim <= início ({raw_line!r})")
        segments.append((start, end))
    if not segments:
        raise ValueError("Nenhum timestamp encontrado no arquivo.")
    return segments


def build_filter_complex(segments):
    trims = []
    refs = []
    for i, (start, end) in enumerate(segments):
        trims.append(
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}];"
        )
        refs.append(f"[v{i}][a{i}]")
    concat = f"{''.join(refs)}concat=n={len(segments)}:v=1:a=1[outv][outa]"
    return "".join(trims) + concat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path, help="Vídeo raw de entrada (OBS)")
    parser.add_argument("timestamps", type=Path, help="Arquivo .txt com os trechos")
    parser.add_argument("saida", type=Path, help="Caminho do vídeo final (.mp4)")
    parser.add_argument("--vertical", action="store_true", help="Corta pra 9:16 (TikTok/Shorts)")
    args = parser.parse_args()

    if not args.raw.exists():
        sys.exit(f"Arquivo raw não encontrado: {args.raw}")
    if not args.timestamps.exists():
        sys.exit(f"Arquivo de timestamps não encontrado: {args.timestamps}")

    segments = parse_timestamps(args.timestamps)
    filter_complex = build_filter_complex(segments)

    final_video_label = "outv"
    if args.vertical:
        filter_complex += ";[outv]crop=ih*9/16:ih,scale=1080:1920[outv9x16]"
        final_video_label = "outv9x16"

    args.saida.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(args.raw),
        "-filter_complex", filter_complex,
        "-map", f"[{final_video_label}]",
        "-map", "[outa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(args.saida),
    ]

    print(f"Cortando {len(segments)} trecho(s) de {args.raw.name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"ffmpeg falhou:\n{result.stderr[-3000:]}")

    print(f"Pronto: {args.saida}")


if __name__ == "__main__":
    main()
