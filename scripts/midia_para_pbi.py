"""
Converte um vídeo (MP4) em WebP animado leve e fatia em base64 para o Power BI.

O visual HTML Content bloqueia URLs externas, mas aceita imagens embutidas
(data URI). Como o Power BI corta textos longos numa célula, o base64 vai
fatiado em pedaços de 30 mil caracteres na tabela dMidia (Midia, Ordem, Parte).

Uso:
    python scripts/midia_para_pbi.py <video.mp4> <nome_midia> [--largura 960] [--fps 12] [--qualidade 45]
                                     [--inicio 0] [--duracao 8] [--pingpong]

Exemplo:
    python scripts/midia_para_pbi.py midia/fundo_capa.mp4 capa --pingpong

Saídas:
    midia/<nome_midia>.webp   (para conferir)
    dados/dMidia.csv          (todas as mídias; a mídia <nome_midia> é substituída)
"""
import argparse
import base64
import csv
import shutil
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PEDACO = 30000

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("nome")
ap.add_argument("--largura", type=int, default=960)
ap.add_argument("--fps", type=int, default=12)
ap.add_argument("--qualidade", type=int, default=45)
ap.add_argument("--inicio", type=float, default=0)
ap.add_argument("--duracao", type=float, default=8)
ap.add_argument("--pingpong", action="store_true", help="toca ida e volta para o loop não ter corte")
ap.add_argument("--crop", default="", help="recorte FFmpeg antes de redimensionar, ex.: 1600:900:160:180 (largura:altura:x:y)")
a = ap.parse_args()

ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
saida = RAIZ / "midia" / f"{a.nome}.webp"
saida.parent.mkdir(exist_ok=True)

filtro = (f"crop={a.crop}," if a.crop else "") + f"fps={a.fps},scale={a.largura}:-2:flags=lanczos"
if a.pingpong:
    filtro += ",split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1"

subprocess.run([
    ffmpeg, "-y", "-loglevel", "error", "-ss", str(a.inicio), "-t", str(a.duracao), "-i", a.video,
    "-filter_complex", filtro, "-an", "-c:v", "libwebp", "-loop", "0",
    "-quality", str(a.qualidade), "-compression_level", "6", "-preset", "picture", str(saida),
], check=True)

b64 = base64.b64encode(saida.read_bytes()).decode()
partes = [b64[i:i + PEDACO] for i in range(0, len(b64), PEDACO)]

csv_path = RAIZ / "dados" / "dMidia.csv"
linhas = []
if csv_path.exists():
    with open(csv_path, encoding="utf-8") as f:
        linhas = [r for r in csv.DictReader(f) if r["Midia"] != a.nome]
linhas += [{"Midia": a.nome, "Tipo": "image/webp", "Ordem": i, "Parte": p} for i, p in enumerate(partes, 1)]
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["Midia", "Tipo", "Ordem", "Parte"])
    w.writeheader()
    w.writerows(linhas)

kb = saida.stat().st_size / 1024
print(f"{saida.name}: {kb:,.0f} KB | base64 {len(b64):,} caracteres em {len(partes)} partes -> {csv_path.name}")
if kb > 1500:
    print("Aviso: acima de ~1,5 MB a capa demora a abrir. Reduza --largura, --fps ou --qualidade.")
