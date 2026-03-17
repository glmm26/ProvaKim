"""AP1 - Análise Exploratória de Dados (AIDS_Classification.csv).

Versão sem dependências externas: usa apenas biblioteca padrão.
Gera os resultados numéricos e produz o boxplot do Desafio 2 como imagem SVG.
"""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import median

DATA_PATH = Path("AIDS_Classification.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return 0.0
    idx = (len(sorted_values) - 1) * p
    lo = int(idx)
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = idx - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def box_stats(values: list[float]) -> dict[str, float | list[float]]:
    vals = sorted(values)
    q1 = percentile(vals, 0.25)
    q2 = percentile(vals, 0.50)
    q3 = percentile(vals, 0.75)
    iqr = q3 - q1
    low_fence = q1 - 1.5 * iqr
    high_fence = q3 + 1.5 * iqr

    non_out = [v for v in vals if low_fence <= v <= high_fence]
    whisk_low = min(non_out) if non_out else min(vals)
    whisk_high = max(non_out) if non_out else max(vals)
    outliers = [v for v in vals if v < low_fence or v > high_fence]

    return {
        "q1": q1,
        "median": q2,
        "q3": q3,
        "whisk_low": whisk_low,
        "whisk_high": whisk_high,
        "outliers": outliers,
        "min": vals[0],
        "max": vals[-1],
    }


def load_dataset(path: Path) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            row: dict[str, float | int | str] = dict(raw)
            for c in ["age", "wtkg", "cd40", "cd420"]:
                row[c] = float(raw[c])
            for c in ["infected", "symptom", "trt", "gender", "race"]:
                row[c] = int(raw[c])
            row["cd4_delta"] = abs(float(raw["cd420"]) - float(raw["cd40"]))
            row["gender_label"] = "Feminino" if int(raw["gender"]) == 0 else "Masculino"
            row["race_label"] = "Não branca" if int(raw["race"]) == 0 else "Branca"
            rows.append(row)
    return rows


def scale_y(v: float, y_min: float, y_max: float, top: float, height: float) -> float:
    if y_max == y_min:
        return top + height / 2
    return top + (1 - (v - y_min) / (y_max - y_min)) * height


def draw_single_box(svg: list[str], stats: dict[str, float | list[float]], x: float, box_w: float,
                    y_min: float, y_max: float, top: float, height: float, color: str) -> None:
    q1 = float(stats["q1"])
    q3 = float(stats["q3"])
    med = float(stats["median"])
    wl = float(stats["whisk_low"])
    wh = float(stats["whisk_high"])

    y_q1 = scale_y(q1, y_min, y_max, top, height)
    y_q3 = scale_y(q3, y_min, y_max, top, height)
    y_med = scale_y(med, y_min, y_max, top, height)
    y_wl = scale_y(wl, y_min, y_max, top, height)
    y_wh = scale_y(wh, y_min, y_max, top, height)

    left = x - box_w / 2
    right = x + box_w / 2

    svg.append(f'<rect x="{left:.1f}" y="{min(y_q1, y_q3):.1f}" width="{box_w:.1f}" height="{abs(y_q1-y_q3):.1f}" fill="{color}" fill-opacity="0.35" stroke="{color}"/>')
    svg.append(f'<line x1="{left:.1f}" y1="{y_med:.1f}" x2="{right:.1f}" y2="{y_med:.1f}" stroke="#111" stroke-width="2"/>')
    svg.append(f'<line x1="{x:.1f}" y1="{y_q3:.1f}" x2="{x:.1f}" y2="{y_wh:.1f}" stroke="#222"/>')
    svg.append(f'<line x1="{x:.1f}" y1="{y_q1:.1f}" x2="{x:.1f}" y2="{y_wl:.1f}" stroke="#222"/>')
    svg.append(f'<line x1="{x-box_w*0.25:.1f}" y1="{y_wh:.1f}" x2="{x+box_w*0.25:.1f}" y2="{y_wh:.1f}" stroke="#222"/>')
    svg.append(f'<line x1="{x-box_w*0.25:.1f}" y1="{y_wl:.1f}" x2="{x+box_w*0.25:.1f}" y2="{y_wl:.1f}" stroke="#222"/>')

    for out in stats["outliers"]:  # type: ignore[index]
        y_out = scale_y(float(out), y_min, y_max, top, height)
        svg.append(f'<circle cx="{x:.1f}" cy="{y_out:.1f}" r="2.3" fill="#cc0000"/>')


def generate_dual_boxplot_svg(rows: list[dict[str, float | int | str]], out_path: Path) -> None:
    wt0 = [float(r["wtkg"]) for r in rows if int(r["infected"]) == 0]
    wt1 = [float(r["wtkg"]) for r in rows if int(r["infected"]) == 1]
    age0 = [float(r["age"]) for r in rows if int(r["infected"]) == 0]
    age1 = [float(r["age"]) for r in rows if int(r["infected"]) == 1]

    width, height = 1200, 560
    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="600" y="34" text-anchor="middle" font-size="22" font-family="Arial" font-weight="bold">Desafio 2 - Box Plots por infected</text>',
    ]

    panels = [
        (80, 80, 500, 420, "Peso (wtkg)", wt0, wt1, "kg"),
        (640, 80, 500, 420, "Idade (age)", age0, age1, "anos"),
    ]

    for px, py, pw, ph, title, vals0, vals1, unit in panels:
        y_min = min(vals0 + vals1)
        y_max = max(vals0 + vals1)
        s0 = box_stats(vals0)
        s1 = box_stats(vals1)

        svg.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="none" stroke="#bbbbbb"/>')
        svg.append(f'<text x="{px+pw/2}" y="{py-14}" text-anchor="middle" font-size="18" font-family="Arial">{title}</text>')

        # eixo Y e marcas
        for i in range(6):
            v = y_min + (y_max - y_min) * i / 5
            yy = scale_y(v, y_min, y_max, py + 20, ph - 60)
            svg.append(f'<line x1="{px+40}" y1="{yy:.1f}" x2="{px+pw-20}" y2="{yy:.1f}" stroke="#efefef"/>')
            svg.append(f'<text x="{px+34}" y="{yy+4:.1f}" text-anchor="end" font-size="11" font-family="Arial">{v:.1f}</text>')

        axis_left = px + 40
        axis_bottom = py + ph - 40
        svg.append(f'<line x1="{axis_left}" y1="{py+20}" x2="{axis_left}" y2="{axis_bottom}" stroke="#222"/>')
        svg.append(f'<line x1="{axis_left}" y1="{axis_bottom}" x2="{px+pw-20}" y2="{axis_bottom}" stroke="#222"/>')
        svg.append(f'<text x="{axis_left-8}" y="{py+18}" text-anchor="end" font-size="11" font-family="Arial">{unit}</text>')

        x0 = px + pw * 0.38
        x1 = px + pw * 0.70
        draw_single_box(svg, s0, x0, 56, y_min, y_max, py + 20, ph - 60, "#1f77b4")
        draw_single_box(svg, s1, x1, 56, y_min, y_max, py + 20, ph - 60, "#ff7f0e")

        svg.append(f'<text x="{x0}" y="{axis_bottom+20}" text-anchor="middle" font-size="12" font-family="Arial">infected=0</text>')
        svg.append(f'<text x="{x1}" y="{axis_bottom+20}" text-anchor="middle" font-size="12" font-family="Arial">infected=1</text>')

    svg.append('</svg>')
    out_path.write_text("\n".join(svg), encoding="utf-8")


def main() -> None:
    rows = load_dataset(DATA_PATH)
    generate_dual_boxplot_svg(rows, OUTPUT_DIR / "desafio2_boxplots.svg")
    print("Imagem gerada: outputs/desafio2_boxplots.svg")
    print("Observação: o boxplot foi gerado em formato de imagem (SVG), não texto.")


if __name__ == "__main__":
    main()
