# AP1 — Análise Exploratória de Dados (AIDS_Classification.csv)

Este material acompanha o script `ap1_analise_exploratoria.py` e organiza os resultados em formato de relatório.

## Como executar

```bash
python ap1_analise_exploratoria.py
```

> Observação: o script usa `pandas`, `matplotlib` e `seaborn`.

---

## Desafio 1 — Fundação dos Dados (Data Cleaning)

### O que foi feito
1. Verificação de valores ausentes com `df.isna().sum()`.
2. Limpeza com remoção de linhas nulas nas colunas críticas (`age`, `wtkg`, `cd40`, `cd420`, `infected`, `symptom`, `trt`).
3. Conversão explícita de tipos para numérico nas colunas `age`, `wtkg`, `cd40` e `cd420`.
4. Criação da coluna `cd4_delta = abs(cd420 - cd40)`.
5. Recodificação auxiliar de `gender` e `race` para facilitar leitura (`gender_label`, `race_label`).

### Storytelling (parágrafo solicitado)
A limpeza de dados é o alicerce de uma análise clínica confiável porque decisões médicas dependem diretamente da qualidade dos cálculos estatísticos. Se uma coluna numérica estiver como texto (por exemplo, `"350"` em vez de `350`), a média pode falhar, a correlação pode ser distorcida e até a ordenação dos pacientes pode ficar errada (ordem lexicográfica em vez de numérica). Em um contexto hospitalar, esse tipo de erro pode levar a interpretações equivocadas sobre risco, resposta ao tratamento e priorização de recursos, comprometendo condutas clínicas.

---

## Desafio 2 — O Escudo Imunológico (Box Plots)

### O que foi feito
- Dois box plots lado a lado:
  - `wtkg` por `infected`
  - `age` por `infected`
- Arquivo gerado: `outputs/desafio2_boxplots.png`

### Leitura dos resultados (base do dataset)
- **Peso (`wtkg`)**:
  - Mediana (infected=0): **73.94 kg**
  - Mediana (infected=1): **74.70 kg**
- **Idade (`age`)**:
  - Mediana (infected=0): **34 anos**
  - Mediana (infected=1): **35 anos**
- Há outliers em ambos os grupos (idade e peso), indicando casos clínicos incomuns.

### Storytelling
Visualmente, não há separação dramática entre os grupos apenas por idade/peso, porque as medianas são próximas e as distribuições se sobrepõem. Isso sugere que idade e peso, isoladamente, não parecem explicar totalmente a progressão para infecção. Os outliers lembram que medicina é heterogênea: sempre existem pacientes fora do padrão que podem ter comorbidades, adesão diferente ao tratamento ou fatores biológicos específicos.

---

## Desafio 3 — A Eficácia dos Protocolos (Barras)

### O que foi feito
1. Agrupamento por `trt`.
2. Cálculo da média de `cd420` por tratamento.
3. Gráfico de barras com destaque em cor para a maior média.
4. Arquivo gerado: `outputs/desafio3_barras_cd420_por_trt.png`.

### Médias encontradas
- `trt=0`: **336.14**
- `trt=1`: **403.17** ✅ (melhor)
- `trt=2`: **372.04**
- `trt=3`: **374.32**

### Storytelling
Para um comitê de ética, o gráfico comunica de forma direta que o protocolo `trt=1` apresenta o melhor desempenho médio de manutenção imunológica (CD4 na semana 20), superando claramente o pior protocolo (`trt=0`) por cerca de 67 células em média. Mesmo sem teste estatístico inferencial no gráfico, a diferença de altura entre as barras já indica um sinal prático de superioridade que justifica priorizar investigação e investimento nesse protocolo.

---

## Desafio 4 — Correlações Ocultas (Scatter + Estatística)

### O que foi feito
1. Scatter plot de `cd40` (X) vs `cd420` (Y).
2. Coloração por `symptom` com `hue`.
3. Cálculo da correlação linear de Pearson.
4. Arquivo gerado: `outputs/desafio4_scatter_cd40_cd420.png`.

### Resultado
- Correlação `cd40` vs `cd420`: **0.5836** (positiva moderada).

### Storytelling
A nuvem de pontos tende a subir, mas com dispersão relevante. Isso sugere uma “jornada de recuperação” em que o estado imunológico inicial influencia significativamente o desfecho em 20 semanas, porém não o determina sozinho. Em outras palavras: começar com CD4 baixo tende a manter o paciente em desvantagem, mas o tratamento ainda pode gerar trajetórias diferentes entre indivíduos (aderência, protocolo, fatores clínicos adicionais).

---

## Exercício — Risco dos Sintomas Visíveis

### O que foi feito
1. Cálculo da probabilidade simples `P(Infectado)`.
2. Cálculo de `P(Infected | Symptom=1)`.
3. Cálculo de `P(Infected | Symptom=0)`.
4. Gráfico de barras para comparação.
5. Arquivo gerado: `outputs/exercicio_probabilidades_sintomas.png`.

### Probabilidades
- `P(Infectado) = 24.36%`
- `P(Infected | Symptom=1) = 36.49%`
- `P(Infected | Symptom=0) = 21.82%`

### Storytelling
Os sintomas iniciais funcionam como um forte sinal de alerta: o risco condicional de infecção é substancialmente maior em pacientes sintomáticos. No entanto, pacientes sem sintomas não estão “fora de perigo”, pois ainda mantêm risco relevante (~22%). Em política de saúde, isso sugere priorização clínica dos sintomáticos para resposta rápida, mas não exclusão de assintomáticos de estratégias de monitoramento e testagem.

---

## Conclusão
A análise reforça três mensagens: (1) qualidade dos dados é pré-requisito para decisão segura; (2) variáveis demográficas isoladas explicam pouco quando comparadas ao contexto clínico completo; (3) protocolos terapêuticos e estado imunológico basal carregam sinais importantes de prognóstico.
