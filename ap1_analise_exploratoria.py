"""AP1 - Análise Exploratória de Dados (AIDS_Classification.csv).

Gera limpeza, estatísticas e visualizações para os quatro desafios + exercício
probabilístico descritos no enunciado.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATA_PATH = Path("AIDS_Classification.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def carregar_e_limpar_dados(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # 1) Valores ausentes
    ausentes = df.isna().sum()
    print("\n[Limpeza] Valores ausentes por coluna:\n", ausentes)

    # Estratégia: remover linhas com NaN em variáveis críticas para a análise.
    colunas_criticas = ["age", "wtkg", "cd40", "cd420", "infected", "symptom", "trt"]
    antes = len(df)
    df = df.dropna(subset=colunas_criticas).copy()
    print(f"[Limpeza] Linhas removidas por NaN em colunas críticas: {antes - len(df)}")

    # 2) Garantir tipos numéricos
    for col in ["age", "wtkg", "cd40", "cd420"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Reaplicar limpeza se alguma conversão gerou NaN
    antes = len(df)
    df = df.dropna(subset=["age", "wtkg", "cd40", "cd420"]).copy()
    print(f"[Limpeza] Linhas removidas por erro de tipo em colunas numéricas: {antes - len(df)}")

    # 3) Nova coluna: variação absoluta do CD4
    df["cd4_delta"] = (df["cd420"] - df["cd40"]).abs()

    # Decodificação para leitura de relatório (mantendo colunas originais)
    df["gender_label"] = df["gender"].map({0: "Feminino", 1: "Masculino"}).fillna(df["gender"].astype(str))
    df["race_label"] = df["race"].map({0: "Não branca", 1: "Branca"}).fillna(df["race"].astype(str))

    return df


def desafio_2_boxplots(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sns.boxplot(data=df, x="infected", y="wtkg", ax=axes[0])
    axes[0].set_title("Distribuição de wtkg por status infected")
    axes[0].set_xlabel("infected (0 = não, 1 = sim)")
    axes[0].set_ylabel("Peso (kg)")

    sns.boxplot(data=df, x="infected", y="age", ax=axes[1])
    axes[1].set_title("Distribuição de age por status infected")
    axes[1].set_xlabel("infected (0 = não, 1 = sim)")
    axes[1].set_ylabel("Idade (anos)")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "desafio2_boxplots.png", dpi=200)
    plt.close(fig)

    resumo = (
        df.groupby("infected")[["wtkg", "age"]]
        .agg(["median", "min", "max"])
        .round(2)
    )
    print("\n[Desafio 2] Resumo descritivo por infected:\n", resumo)


def desafio_3_barras_tratamento(df: pd.DataFrame) -> pd.Series:
    medias_cd420 = df.groupby("trt")["cd420"].mean().sort_values(ascending=False)
    melhor_trt = medias_cd420.idxmax()

    cores = ["#1f77b4" if trt != melhor_trt else "#d62728" for trt in medias_cd420.index]

    plt.figure(figsize=(9, 6))
    plt.bar(medias_cd420.index.astype(str), medias_cd420.values, color=cores)
    plt.title("Média de CD4 na semana 20 por tratamento (trt)")
    plt.xlabel("Tratamento (trt)")
    plt.ylabel("Média de cd420")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "desafio3_barras_cd420_por_trt.png", dpi=200)
    plt.close()

    print("\n[Desafio 3] Média de cd420 por tratamento:\n", medias_cd420.round(2))
    print(f"[Desafio 3] Melhor tratamento (maior média): trt = {melhor_trt}")
    return medias_cd420


def desafio_4_scatter_correlacao(df: pd.DataFrame) -> float:
    plt.figure(figsize=(9, 6))
    sns.scatterplot(data=df, x="cd40", y="cd420", hue="symptom", alpha=0.7)
    plt.title("Relação entre CD4 inicial (cd40) e CD4 na semana 20 (cd420)")
    plt.xlabel("cd40")
    plt.ylabel("cd420")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "desafio4_scatter_cd40_cd420.png", dpi=200)
    plt.close()

    correlacao = df[["cd40", "cd420"]].corr().loc["cd40", "cd420"]
    print(f"\n[Desafio 4] Correlação cd40 x cd420: {correlacao:.4f}")
    return correlacao


def exercicio_probabilidades(df: pd.DataFrame) -> tuple[float, float, float]:
    p_infectado = df["infected"].mean()
    p_inf_dado_sym1 = df.loc[df["symptom"] == 1, "infected"].mean()
    p_inf_dado_sym0 = df.loc[df["symptom"] == 0, "infected"].mean()

    plt.figure(figsize=(7, 5))
    labels = ["P(Infected | Symptom=1)", "P(Infected | Symptom=0)"]
    valores = [p_inf_dado_sym1, p_inf_dado_sym0]
    plt.bar(labels, valores, color=["#ff7f0e", "#2ca02c"])
    plt.title("Comparação das probabilidades condicionais de infecção")
    plt.ylabel("Probabilidade")
    plt.ylim(0, max(valores) * 1.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "exercicio_probabilidades_sintomas.png", dpi=200)
    plt.close()

    print(f"\n[Exercício Probabilidade] P(Infectado) = {p_infectado:.4f}")
    print(f"[Exercício Probabilidade] P(Infected | Symptom=1) = {p_inf_dado_sym1:.4f}")
    print(f"[Exercício Probabilidade] P(Infected | Symptom=0) = {p_inf_dado_sym0:.4f}")

    return p_infectado, p_inf_dado_sym1, p_inf_dado_sym0


def main() -> None:
    sns.set_theme(style="whitegrid")
    df = carregar_e_limpar_dados(DATA_PATH)

    desafio_2_boxplots(df)
    medias_cd420 = desafio_3_barras_tratamento(df)
    correlacao = desafio_4_scatter_correlacao(df)
    p_infectado, p_sym1, p_sym0 = exercicio_probabilidades(df)

    print("\n=== STORYTELLING SUGERIDO ===")
    print(
        "1) Limpeza é alicerce: sem tipos numéricos corretos, médias e correlações podem ser calculadas "
        "de forma incorreta (ou nem serem calculadas), gerando conclusões clínicas erradas sobre risco e eficácia."
    )
    print(
        "2) Box plots: compare medianas e dispersões para verificar risco por idade/peso; outliers destacam casos "
        "clínicos atípicos que merecem investigação individual."
    )
    print(
        f"3) Barras de tratamento: trt={medias_cd420.idxmax()} teve melhor média de cd420 ({medias_cd420.max():.2f}), "
        f"enquanto o pior foi {medias_cd420.idxmin()} ({medias_cd420.min():.2f})."
    )
    print(
        f"4) Correlação cd40~cd420 = {correlacao:.2f}: tendência positiva moderada, indicando que estado inicial "
        "do sistema imune influencia o desfecho após 20 semanas."
    )
    print(
        f"5) Sintomas iniciais: risco com sintomas ({p_sym1:.2%}) vs sem sintomas ({p_sym0:.2%}); "
        f"risco geral {p_infectado:.2%}. Ausência de sintomas reduz risco, mas não zera o perigo clínico."
    )


if __name__ == "__main__":
    main()
