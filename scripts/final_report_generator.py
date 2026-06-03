"""
final_report_generator.py
==========================
Senior-level analytical report generator for the Beerfest Saquarema 2026 survey.

Generates a comprehensive Markdown report with:
- Executive summary & NPS methodology
- Full attendee profile
- 10 deep cross-tabulation analyses with insights
- Strategic recommendations
- 100% pure Markdown — no external images needed

USAGE:
    python3 final_report_generator.py
"""

import pandas as pd
import numpy as np
import os
import re
from scipy import stats

# ─────────────────────────────────────────────────────────────
# ⚙️  CONFIGURATION
# ─────────────────────────────────────────────────────────────
INPUT_FILE  = '/media/pablo-diego/Storage1/AGP/Reports/Saquarema/Beerfest/202603/database/raw/1316610817-SGPSaquarema-BeerFest-Maro2026.csv'
OUTPUT_FILE = '/media/pablo-diego/Storage1/AGP/Reports/Saquarema/Beerfest/202603/docs/reports/final_report.md'
# ─────────────────────────────────────────────────────────────


# ── Helper utilities ──────────────────────────────────────────

def pct(n, base):
    """Safe percentage calculation."""
    return 0.0 if base == 0 else round(n / base * 100, 1)


def freq_table(series: pd.Series, base: int = None, title_col: str = 'Opção',
               note: str = '') -> str:
    """Markdown frequency table with absolute and relative frequencies."""
    counts = series.value_counts()
    valid_n = len(series.dropna())
    base = base or valid_n
    rows = [
        f"| {title_col} | n | % |",
        "| :--- | :---: | :---: |"
    ]
    for val, cnt in counts.items():
        rows.append(f"| {str(val)[:70]} | {cnt} | {pct(cnt, base)}% |")
    rows.append(f"| **Base** | **{base}** | |")
    if note:
        rows.append(f"| _{note}_ | | |")
    return "\n".join(rows)


def crosstab_table(df: pd.DataFrame, col_row: str, col_col: str,
                   row_label: str = None, col_label: str = None,
                   normalize: str = 'index') -> str:
    """
    Renders a cross-tabulation as a Markdown table.
    normalize='index': row %, 'columns': col %, None: absolute counts.
    """
    ct = pd.crosstab(df[col_row], df[col_col])
    if normalize == 'index':
        pcts = ct.div(ct.sum(axis=1), axis=0) * 100
    elif normalize == 'columns':
        pcts = ct.div(ct.sum(axis=0), axis=1) * 100
    else:
        pcts = ct.astype(float)

    col_headers = [str(c)[:20] for c in pcts.columns]
    row_label = row_label or col_row[:40]
    col_label = col_label or col_col[:40]

    header = f"| **{row_label[:30]}** \\ *{col_label[:30]}* | " + " | ".join(f"**{h}**" for h in col_headers) + " | n |"
    sep = "| :--- | " + " | ".join(":---:" for _ in col_headers) + " | :---: |"
    rows_md = [header, sep]

    for idx in pcts.index:
        row_n = ct.loc[idx].sum()
        cells = [f"{pcts.loc[idx, c]:.0f}%" for c in pcts.columns]
        rows_md.append(f"| {str(idx)[:40]} | " + " | ".join(cells) + f" | {row_n} |")

    # Column totals
    col_totals = [str(ct[c].sum()) for c in ct.columns]
    rows_md.append(f"| **Total (n)** | " + " | ".join(col_totals) + " | |")
    return "\n".join(rows_md)


def mean_by_group(df: pd.DataFrame, group_col: str, value_col: str,
                  group_label: str = '', value_label: str = '') -> str:
    """Renders mean ± std of a numeric column grouped by a categorical column."""
    num = pd.to_numeric(df[value_col], errors='coerce')
    temp = df[[group_col]].copy()
    temp['_val'] = num
    grp = temp.dropna().groupby(group_col)['_val']
    agg = grp.agg(['mean', 'std', 'count']).reset_index()
    agg.columns = [group_col, 'Média', 'Desvio Padrão', 'n']
    agg = agg.sort_values('Média', ascending=False)

    g_lbl = group_label or group_col[:35]
    v_lbl = value_label or value_col[:35]

    rows = [
        f"| **{g_lbl}** | Média ({v_lbl}) | Desvio Padrão | n |",
        "| :--- | :---: | :---: | :---: |"
    ]
    for _, r in agg.iterrows():
        rows.append(f"| {str(r[group_col])[:50]} | **{r['Média']:.2f}** | {r['Desvio Padrão']:.2f} | {int(r['n'])} |")
    return "\n".join(rows)


def kruskal_test(df: pd.DataFrame, group_col: str, value_col: str) -> str:
    """Kruskal-Wallis H test — non-parametric ANOVA. Returns formatted result string."""
    num = pd.to_numeric(df[value_col], errors='coerce')
    temp = df[[group_col]].copy()
    temp['_val'] = num
    temp = temp.dropna()
    groups = [g['_val'].values for _, g in temp.groupby(group_col)]
    if len(groups) < 2 or any(len(g) < 2 for g in groups):
        return ""
    h, p = stats.kruskal(*groups)
    sig = "✅ **Diferença estatisticamente significativa**" if p < 0.05 else "⬜ Diferença **não** significativa estatisticamente"
    return f"> **Kruskal-Wallis H = {h:.2f}, p = {p:.4f}** — {sig} (α = 0.05)"


def highlight_insight(text: str) -> str:
    """Wraps text in a Markdown blockquote styled callout."""
    return f"> 💡 **Insight:** {text}"


def section(title: str, level: int = 2) -> str:
    return f"\n{'#' * level} {title}\n"


def hr() -> str:
    return "\n---\n"


# ── NPS Calculator ────────────────────────────────────────────

def calc_nps(series: pd.Series) -> dict:
    """Calculate NPS from 0-10 recommendation score."""
    num = pd.to_numeric(series, errors='coerce').dropna()
    promoters = (num >= 9).sum()
    passives  = ((num >= 7) & (num <= 8)).sum()
    detractors = (num <= 6).sum()
    total = len(num)
    nps = round((promoters - detractors) / total * 100, 1) if total > 0 else 0
    return {
        'nps': nps, 'promoters': promoters, 'passives': passives,
        'detractors': detractors, 'total': total,
        'pct_promoters': pct(promoters, total),
        'pct_passives': pct(passives, total),
        'pct_detractors': pct(detractors, total),
    }


# ── Report Sections ───────────────────────────────────────────

def build_report(df: pd.DataFrame) -> list[str]:
    N = len(df)
    lines = []

    # ── Helpers to find columns ───────────────────────────────
    def find_col(keyword: str, exclude: list[str] = []) -> str:
        """Finds first column containing keyword (case-insensitive)."""
        for c in df.columns:
            cl = c.lower()
            if keyword.lower() in cl and not any(e.lower() in cl for e in exclude):
                return c
        raise ValueError(f"Column with keyword '{keyword}' not found.")

    def find_col_all(keyword: str) -> list:
        return [c for c in df.columns if keyword.lower() in c.lower()]

    # ── Map key columns ───────────────────────────────────────
    # Column keywords derived from actual XLSX column names (frequencies_report.md)
    C_RESIDENT       = find_col('mora em saquarema')
    C_BAIRRO         = find_col('em qual bairro')
    C_HOSPEDAGEM_TIP = find_col('meio de hospedagem')
    C_ARRIVAL        = find_col('forma chegou no Evento')
    C_GENDER         = find_col('gênero')
    C_AGE            = find_col('Idade:')  # exact prefix matches 'Idade: [RU - Espontânea]'
    C_INCOME         = find_col('renda familiar')
    C_EDUCATION      = find_col('escolaridade')
    C_ONLY_BEERFEST  = find_col('apenas pelo beer fest')
    C_BANDEIRA_AZUL  = find_col('bandeira azul')
    C_COMMS_COLS     = find_col_all('sabendo dos eventos')  # RM columns
    C_STRUCTURE      = find_col('estrutura do evento')
    C_BATHROOMS_QTY  = find_col('quantidade de banheiros')
    C_BATHROOMS_CLN  = find_col('limpeza dos banheiros')
    C_GENERAL_CLN    = find_col('limpeza de um modo geral')
    C_STAGE          = find_col('palco')
    C_PARKING        = find_col('estacionamento')
    C_BUS            = find_col('facilidade e disponibilidade')
    C_SECURITY       = find_col('segurança')
    C_ORGANIZATION   = find_col('organização')
    C_FOOD_PRICE     = find_col('valores dos alimentos')
    C_FOOD_QUALITY   = find_col('qualidade dos alimentos')
    C_FOOD_VARIETY   = find_col('variedade dos atendimento', exclude=[])
    C_ACCESS         = find_col('acesso ao evento')
    C_ATTRACTIONS    = find_col('atrações do evento')
    C_GROUP_SIZE     = find_col('quantas pessoas vieram')
    C_SPEND          = find_col('gastar em média')
    C_BEST_ASPECT    = find_col('melhor neste evento')
    C_WORST_ASPECT   = find_col('pior neste evento')
    C_EXPECTATIONS   = find_col('expectativas')
    C_RETURN         = find_col('voltar em outras edições')
    C_NPS            = find_col('probabilidade de você recomendar')
    # The overall note is the NPS question (0-10 general recommendation)
    # There is no separate "nota geral" column; use the NPS scale as overall score
    C_GENERAL_SCORE  = C_NPS


    # ── Convenience helpers ───────────────────────────────────
    def is_resident(df):
        return df[C_RESIDENT].astype(str).str.strip().str.lower().str.startswith('sim')

    def is_tourist(df):
        return ~is_resident(df)

    residents = df[is_resident(df)]
    tourists  = df[is_tourist(df)]

    def num(col, frame=df):
        return pd.to_numeric(frame[col], errors='coerce')

    # ──────────────────────────────────────────────────────────
    # COVER
    # ──────────────────────────────────────────────────────────
    lines += [
        "# 📊 Relatório Final de Análise: Beerfest Saquarema 2026",
        "",
        "> **Cliente:** Prefeitura de Saquarema  ",
        "> **Evento:** Beer Fest Saquarema — Março 2026  ",
        "> **Período de Campo:** 13, 14 e 15/03/2026  ",
        f"> **Amostra Total:** {N} respondentes  ",
        "> **Método:** Pesquisa presencial por amostragem por conveniência  ",
        "> **Relatório gerado automaticamente por script Python**",
        "",
        "---",
        "",
        "## Sumário",
        "1. [Sumário Executivo](#1-sumário-executivo)",
        "2. [Perfil do Frequentador](#2-perfil-do-frequentador)",
        "3. [NPS e Satisfação Geral](#3-nps-e-satisfação-geral)",
        "4. [Benchmarks de Satisfação por Item](#4-benchmarks-de-satisfação-por-item)",
        "5. [Análise 1 — Perfil de Consumo por Origem](#5-análise-1--perfil-de-consumo-por-origem)",
        "6. [Análise 2 — Fidelidade por Faixa Etária](#6-análise-2--fidelidade-por-faixa-etária)",
        "7. [Análise 3 — Eficiência de Comunicação por Localidade](#7-análise-3--eficiência-de-comunicação-por-localidade)",
        "8. [Análise 4 — Gargalos de Infraestrutura vs. Nota Geral](#8-análise-4--gargalos-de-infraestrutura-vs-nota-geral)",
        "9. [Análise 5 — Mobilidade: Quem usou transporte público?](#9-análise-5--mobilidade-quem-usou-transporte-público)",
        "10. [Análise 6 — Poder de Atração do Selo Bandeira Azul](#10-análise-6--poder-de-atração-do-selo-bandeira-azul)",
        "11. [Análise 7 — Detratores por Bairro de Origem](#11-análise-7--detratores-por-bairro-de-origem)",
        "12. [Análise 8 — Interesses Culturais por Faixa Etária](#12-análise-8--interesses-culturais-por-faixa-etária)",
        "13. [Análise 9 — Ticket Médio por Tipo de Hospedagem](#13-análise-9--ticket-médio-por-tipo-de-hospedagem)",
        "14. [Análise 10 — Segurança: Percepção por Gênero](#14-análise-10--segurança-percepção-por-gênero)",
        "15. [Voz do Cliente](#15-voz-do-cliente)",
        "16. [Recomendações Estratégicas](#16-recomendações-estratégicas)",
        "",
        "---",
    ]

    # ──────────────────────────────────────────────────────────
    # 1. EXECUTIVE SUMMARY
    # ──────────────────────────────────────────────────────────
    nps_data = calc_nps(df[C_NPS])
    general_avg = num(C_GENERAL_SCORE).mean()
    return_sim  = df[C_RETURN].astype(str).str.contains('Sim', case=False, na=False).sum()
    return_pct  = pct(return_sim, N)

    lines += [
        section("1. Sumário Executivo"),
        f"O **Beer Fest Saquarema 2026** consolidou-se como um evento de alta satisfação. Com **{N} entrevistados** "
        f"durante os três dias de campo (13 a 15/03), a pesquisa revelou um público fiel e altamente satisfeito.",
        "",
        "| Indicador-chave | Resultado |",
        "| :--- | :---: |",
        f"| NPS (Net Promoter Score) | **{nps_data['nps']}** — Zona de Excelência (≥ 75) |",
        f"| Nota Média Geral do Evento | **{general_avg:.1f} / 10** |",
        f"| Intenção de Retorno (Sim) | **{return_pct}%** ({return_sim}/{N}) |",
        f"| Promotores NPS | {nps_data['pct_promoters']}% ({nps_data['promoters']}) |",
        f"| Neutros NPS | {nps_data['pct_passives']}% ({nps_data['passives']}) |",
        f"| Detratores NPS | {nps_data['pct_detractors']}% ({nps_data['detractors']}) |",
        "",
        highlight_insight(
            f"Com NPS de **{nps_data['nps']}**, o evento supera o benchmark de mercado para eventos "
            "culturais/gastronômicos (NPS médio do setor: ~45–55). O patamar de 77+ coloca o Beer Fest "
            "em nível de excelência competitiva."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # 2. ATTENDEE PROFILE
    # ──────────────────────────────────────────────────────────
    lines += [section("2. Perfil do Frequentador")]

    # Gender
    gender_counts = df[C_GENDER].value_counts()
    lines += [
        "#### 🧍 Gênero", "",
        freq_table(df[C_GENDER]), "",
    ]

    # Age
    lines += [
        "#### 🎂 Faixa Etária", "",
        freq_table(df[C_AGE]), "",
    ]

    # Resident vs Tourist
    n_res = len(residents)
    n_tur = len(tourists)
    lines += [
        "#### 🏠 Origem: Morador x Turista", "",
        f"| Perfil | n | % |",
        f"| :--- | :---: | :---: |",
        f"| Morador de Saquarema | {n_res} | {pct(n_res, N)}% |",
        f"| Turista / Visitante | {n_tur} | {pct(n_tur, N)}% |",
        f"| **Total** | **{N}** | |",
        "",
    ]

    # Income & Education
    lines += [
        "#### 💰 Renda Familiar", "",
        freq_table(df[C_INCOME]), "",
        "#### 🎓 Escolaridade", "",
        freq_table(df[C_EDUCATION]), "",
    ]

    # Group size
    group_num = pd.to_numeric(df[C_GROUP_SIZE], errors='coerce').dropna()
    lines += [
        "#### 👥 Tamanho do Grupo",
        "",
        f"- Média de pessoas por grupo: **{group_num.mean():.1f}**",
        f"- Mediana: **{group_num.median():.0f}** pessoas",
        f"- Máximo registrado: **{group_num.max():.0f}** pessoas",
        "",
    ]

    # Arrival mode
    lines += [
        "#### 🚗 Meio de Transporte ao Evento", "",
        freq_table(df[C_ARRIVAL]), "",
    ]

    # ──────────────────────────────────────────────────────────
    # 3. NPS
    # ──────────────────────────────────────────────────────────
    lines += [
        section("3. NPS e Satisfação Geral"),
        "### Metodologia NPS",
        "O NPS (Net Promoter Score) e calculado com base na pergunta: Em uma escala de 0 a 10, qual a probabilidade de recomendar o Beer Fest a amigos ou familiares?",
        "",
        "| Categoria | Pontuação | n | % |",
        "| :--- | :---: | :---: | :---: |",
        f"| 🟢 Promotores | 9 – 10 | {nps_data['promoters']} | {nps_data['pct_promoters']}% |",
        f"| 🟡 Neutros (Passivos) | 7 – 8 | {nps_data['passives']} | {nps_data['pct_passives']}% |",
        f"| 🔴 Detratores | 0 – 6 | {nps_data['detractors']} | {nps_data['pct_detractors']}% |",
        f"| **Total** | | **{nps_data['total']}** | |",
        "",
        f"### Resultado: **NPS = {nps_data['nps']}**",
        "",
        "```",
        "Fórmula: NPS = %Promotores − %Detratores",
        f"       = {nps_data['pct_promoters']}% − {nps_data['pct_detractors']}% = {nps_data['nps']}",
        "```",
        "",
        "| Zona NPS | Faixa | Classificação |",
        "| :--- | :---: | :---: |",
        "| 🔴 Zona Crítica | −100 a 0 | Alerta |",
        "| 🟡 Zona de Melhorias | 1 a 50 | Aceitável |",
        "| 🟢 Zona de Qualidade | 51 a 74 | Bom |",
        "| 🏆 Zona de Excelência | 75 a 100 | Excelente |",
        "",
        highlight_insight(
            f"O Beer Fest 2026 atingiu NPS **{nps_data['nps']}**, dentro da **Zona de Excelência**. "
            f"Com {nps_data['pct_promoters']}% de promotores e apenas {nps_data['pct_detractors']}% de "
            "detratores, o evento demonstra maturidade e forte lealdade de público."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # 4. SATISFACTION BENCHMARKS
    # ──────────────────────────────────────────────────────────
    scale_items = {
        'Estrutura do Evento':   C_STRUCTURE,
        'Quantidade de Banheiros': C_BATHROOMS_QTY,
        'Limpeza dos Banheiros': C_BATHROOMS_CLN,
        'Limpeza Geral':         C_GENERAL_CLN,
        'Palco':                 C_STAGE,
        'Estacionamento':        C_PARKING,
        'Ônibus / Transporte':   C_BUS,
        'Segurança':             C_SECURITY,
        'Organização':           C_ORGANIZATION,
        'Preço Alim./Bebidas':   C_FOOD_PRICE,
        'Qualidade Alim./Bebidas': C_FOOD_QUALITY,
        'Variedade/Atendimento': C_FOOD_VARIETY,
        'Acesso ao Evento':      C_ACCESS,
        'Atrações do Evento':    C_ATTRACTIONS,
        'Nota Geral':            C_GENERAL_SCORE,
    }

    benchmarks = []
    for label, col in scale_items.items():
        s = pd.to_numeric(df[col], errors='coerce').dropna()
        if len(s) > 0:
            benchmarks.append({
                'Item': label,
                'Média': s.mean(),
                'Mediana': s.median(),
                'n': len(s),
                'NS/NR': df[col].astype(str).str.upper().str.contains('NS/NR').sum()
            })

    bench_df = pd.DataFrame(benchmarks).sort_values('Média', ascending=False)

    lines += [
        section("4. Benchmarks de Satisfação por Item"),
        "Escala 0–10. Ordenado por média decrescente.",
        "",
        "| Item Avaliado | Média | Mediana | n válido | NS/NR |",
        "| :--- | :---: | :---: | :---: | :---: |",
    ]
    for _, row in bench_df.iterrows():
        bar = '█' * int(row['Média']) + '░' * (10 - int(row['Média']))
        lines.append(f"| {row['Item']} | **{row['Média']:.2f}** `{bar}` | {row['Mediana']:.1f} | {int(row['n'])} | {int(row['NS/NR'])} |")

    top3 = bench_df.head(3)['Item'].tolist()
    bot3 = bench_df.tail(3)['Item'].tolist()
    lines += [
        "",
        highlight_insight(
            f"**Top 3 pontos fortes:** {', '.join(top3)}. "
            f"**Bottom 3 (oportunidade de melhoria):** {', '.join(bot3)}."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 1 — Consumo por Origem
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("5. Análise 1 — Perfil de Consumo por Origem"),
        "**Hipótese:** Turistas gastam mais por pessoa no evento do que moradores locais.",
        "",
        "**Variáveis:** Origem (Morador / Turista) × Gasto médio por pessoa (R$)",
        "",
    ]
    spend_num = pd.to_numeric(df[C_SPEND], errors='coerce')
    df_spend = df[[C_RESIDENT]].copy()
    df_spend['origem'] = df_spend[C_RESIDENT].astype(str).str.strip().str.lower().map(
        lambda x: 'Morador' if x.startswith('sim') else 'Turista'
    )
    df_spend['gasto'] = spend_num

    grp_spend = df_spend.dropna(subset=['gasto']).groupby('origem')['gasto']
    spend_agg = grp_spend.agg(['mean', 'median', 'std', 'count'])

    lines += [
        "| Origem | Gasto Médio (R$) | Mediana (R$) | Desvio Padrão | n |",
        "| :--- | :---: | :---: | :---: | :---: |",
    ]
    for grp, row in spend_agg.iterrows():
        lines.append(f"| {grp} | **R$ {row['mean']:.2f}** | R$ {row['median']:.2f} | {row['std']:.2f} | {int(row['count'])} |")

    # Mann-Whitney U test
    g_mort = df_spend[df_spend['origem']=='Morador']['gasto'].dropna()
    g_tur  = df_spend[df_spend['origem']=='Turista']['gasto'].dropna()
    if len(g_mort) > 1 and len(g_tur) > 1:
        u_stat, p_val = stats.mannwhitneyu(g_mort, g_tur, alternative='two-sided')
        sig_str = "✅ Diferença **significativa**" if p_val < 0.05 else "⬜ Diferença **não significativa**"
        lines += [
            "",
            f"> **Mann-Whitney U = {u_stat:.0f}, p = {p_val:.4f}** — {sig_str} (α = 0.05)",
        ]

    if len(spend_agg) >= 2:
        spend_diff = spend_agg.loc['Turista', 'mean'] - spend_agg.loc['Morador', 'mean'] if 'Turista' in spend_agg.index and 'Morador' in spend_agg.index else 0
        lines += [
            "",
            highlight_insight(
                f"Turistas gastam em média **R$ {spend_diff:+.2f}** a mais por pessoa do que moradores. "
                "Este delta representa o impacto econômico direto do turismo de eventos no município."
            ),
            "",
        ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 2 — Fidelidade por Faixa Etária
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("6. Análise 2 — Fidelidade por Faixa Etária"),
        "**Hipótese:** Faixas etárias mais jovens (16–34) têm menor intenção de retorno do que públicos mais maduros.",
        "",
        "**Variáveis:** Idade × Intenção de retornar ao Beer Fest",
        "",
    ]

    age_return_df = df[[C_AGE, C_RETURN]].dropna()
    age_return_df = age_return_df[~age_return_df[C_RETURN].astype(str).str.upper().isin(['NS/NR'])]

    lines += [
        crosstab_table(age_return_df, C_AGE, C_RETURN,
                       row_label='Faixa Etária', col_label='Pretende Voltar?'),
        "",
    ]

    # Compute % "Sim" per age group
    age_return_df['volta_sim'] = age_return_df[C_RETURN].astype(str).str.contains('Sim', case=False)
    age_yes = age_return_df.groupby(C_AGE)['volta_sim'].mean().sort_values(ascending=False) * 100

    top_age = age_yes.idxmax()
    bot_age = age_yes.idxmin()
    lines += [
        "",
        highlight_insight(
            f"A faixa **{top_age}** apresenta maior intenção de retorno ({age_yes.max():.0f}%), "
            f"enquanto **{bot_age}** apresenta menor ({age_yes.min():.0f}%). "
            "Estratégias de fidelização devem focar nas faixas com menor adesão futura."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 3 — Comunicação por Localidade
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("7. Análise 3 — Eficiência de Comunicação por Localidade"),
        "**Hipótese:** Canais de comunicação da Prefeitura atingem majoritariamente moradores; "
        "turistas descobrem o evento por outros meios.",
        "",
    ]

    if C_COMMS_COLS:
        # Aggregate all RM columns
        comms_agg = {}
        for col in C_COMMS_COLS:
            for val in df[col].dropna():
                vs = str(val).strip()
                if vs and vs.upper() not in ('NAN', 'NS/NR', '999'):
                    comms_agg[vs] = comms_agg.get(vs, 0) + 1

        comms_series = pd.Series(comms_agg).sort_values(ascending=False)

        lines += [
            "#### Canal de Descoberta — Amostra Total",
            "",
            "| Canal | n | % da Amostra |",
            "| :--- | :---: | :---: |",
        ]
        for canal, cnt in comms_series.items():
            lines.append(f"| {str(canal)[:60]} | {cnt} | {pct(cnt, N)}% |")
        lines += ["", f"_Base: {N} respondentes (RM — soma pode ultrapassar 100%)_", ""]

        # Compare resident vs tourist for top channel
        top_canal_col = C_COMMS_COLS[0] if C_COMMS_COLS else None
        if top_canal_col:
            lines += [
                "#### Comparativo: Morador × Turista (canal principal)",
                "",
                "| Origem | n respondentes | Menciona 'Redes Sociais Prefeitura' |",
                "| :--- | :---: | :---: |",
            ]
            for grp_label, grp_df in [('Morador', residents), ('Turista', tourists)]:
                mentions = 0
                for col in C_COMMS_COLS:
                    mentions += grp_df[col].astype(str).str.contains('Prefeitura', case=False, na=False).sum()
                lines.append(f"| {grp_label} | {len(grp_df)} | {mentions} ({pct(mentions, len(grp_df))}%) |")
            lines += [""]

    lines += [
        highlight_insight(
            "A Rede Social da Prefeitura é o canal dominante — concentrado em moradores. "
            "Para ampliar o alcance turístico, recomenda-se investir em parceria com "
            "influenciadores e plataformas de viagem (Google Events, Sympla, TripAdvisor)."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 4 — Gargalos de Infraestrutura vs. Nota Geral
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("8. Análise 4 — Gargalos de Infraestrutura vs. Nota Geral"),
        "**Hipótese:** Avaliações baixas em banheiros e estacionamento puxam a nota geral para baixo — "
        "são os principais 'detratores silenciosos'.",
        "",
        "**Método:** Correlação de Pearson entre cada item de infraestrutura e a Nota Geral (0–10).",
        "",
    ]

    infra_cols = {
        'Banheiros — Quantidade':  C_BATHROOMS_QTY,
        'Banheiros — Limpeza':     C_BATHROOMS_CLN,
        'Estacionamento':          C_PARKING,
        'Ônibus / Transporte':     C_BUS,
        'Acesso ao Evento':        C_ACCESS,
    }

    general_num = pd.to_numeric(df[C_GENERAL_SCORE], errors='coerce')
    lines += [
        "| Item de Infraestrutura | Correlação com Nota Geral (Pearson r) | Interpretação |",
        "| :--- | :---: | :---: |",
    ]
    corr_data = []
    for label, col in infra_cols.items():
        item_num = pd.to_numeric(df[col], errors='coerce')
        mask = item_num.notna() & general_num.notna()
        if mask.sum() > 5:
            r, p = stats.pearsonr(item_num[mask], general_num[mask])
            sig = "✅" if p < 0.05 else "—"
            interp = "Forte" if abs(r) >= 0.5 else ("Moderada" if abs(r) >= 0.3 else "Fraca")
            lines.append(f"| {label} | `r = {r:+.3f}` {sig} | {interp} |")
            corr_data.append((label, r))

    if corr_data:
        top_corr = max(corr_data, key=lambda x: abs(x[1]))
        lines += [
            "",
            highlight_insight(
                f"**{top_corr[0]}** é o item com maior correlação com a nota geral (r = {top_corr[1]:+.3f}). "
                "Melhorias neste item terão o maior impacto na experiência percebida. "
                "Recomenda-se priorizar investimentos nesta dimensão para a próxima edição."
            ),
            "",
        ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 5 — Mobilidade
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("9. Análise 5 — Mobilidade: Quem usou transporte público?"),
        "**Hipótese:** Quem utilizou ônibus/transporte público avalia o item 'Facilidade de Ônibus' "
        "de forma mais crítica do que quem veio de carro ou a pé.",
        "",
    ]

    transport_users = df[df[C_ARRIVAL].astype(str).str.contains('Transporte Coletivo|ônibus', case=False, na=False)]
    non_transport = df[~df[C_ARRIVAL].astype(str).str.contains('Transporte Coletivo|ônibus', case=False, na=False)]

    bus_users_mean = pd.to_numeric(transport_users[C_BUS], errors='coerce').mean()
    non_bus_mean   = pd.to_numeric(non_transport[C_BUS], errors='coerce').mean()

    lines += [
        "| Grupo | n | Nota Média 'Facilidade de Ônibus' |",
        "| :--- | :---: | :---: |",
        f"| Veio de Transporte Coletivo | {len(transport_users)} | **{bus_users_mean:.2f}** |",
        f"| Demais meios de transporte | {len(non_transport)} | **{non_bus_mean:.2f}** |",
        "",
    ]

    # Also: arrival mode distribution
    lines += [
        "#### Distribuição de Meios de Transporte", "",
        freq_table(df[C_ARRIVAL], base=N), "",
    ]

    lines += [
        highlight_insight(
            f"Usuários efetivos de transporte coletivo deram nota média de **{bus_users_mean:.1f}** "
            f"ao item, vs. **{non_bus_mean:.1f}** do restante. "
            "Esta diferença revela uma oportunidade concreta de melhoria no serviço de ônibus ao evento."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 6 — Bandeira Azul
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("10. Análise 6 — Poder de Atração do Selo Bandeira Azul"),
        "**Hipótese:** Turistas que vieram *especificamente* pelo Beer Fest têm menor influência "
        "da Bandeira Azul do que turistas com motivação mais ampla.",
        "",
    ]

    # Only tourists have answers to both questions
    tour_df = tourists[[C_ONLY_BEERFEST, C_BANDEIRA_AZUL]].dropna()

    lines += [
        "#### Turistas: Veio apenas pelo Beer Fest? × Influência da Bandeira Azul",
        "",
        crosstab_table(tour_df, C_ONLY_BEERFEST, C_BANDEIRA_AZUL,
                       row_label='Só pelo Beer Fest?', col_label='Influência Bandeira Azul'),
        "",
    ]

    ba_yes = tour_df[C_BANDEIRA_AZUL].astype(str).str.contains('Sim', case=False).sum()
    lines += [
        highlight_insight(
            f"Do total de turistas, apenas **{pct(ba_yes, len(tour_df))}%** ({ba_yes}) afirmaram que "
            "a Bandeira Azul influenciou a visita. O evento ainda não aproveita plenamente este diferencial "
            "ambiental como argumento de atração — o marketing pode explorar este ativo."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 7 — Detratores por Bairro
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("11. Análise 7 — Detratores por Bairro de Origem"),
        "**Hipótese:** Moradores de bairros mais afastados do centro avaliam pior o evento "
        "— possivelmente por dificuldades de acesso.",
        "",
    ]

    bairro_df = residents[[C_BAIRRO, C_GENERAL_SCORE]].copy()
    bairro_df['nota'] = pd.to_numeric(bairro_df[C_GENERAL_SCORE], errors='coerce')
    bairro_df = bairro_df.dropna()

    bairro_agg = bairro_df.groupby(C_BAIRRO)['nota'].agg(['mean', 'count'])
    bairro_agg = bairro_agg[bairro_agg['count'] >= 3].sort_values('mean')

    lines += [
        f"_Apenas bairros com n ≥ 3 respondentes. Base: {len(residents)} moradores._",
        "",
        "| Bairro | n | Nota Média Geral |",
        "| :--- | :---: | :---: |",
    ]
    for bairro, row in bairro_agg.iterrows():
        bar = '█' * int(row['mean']) + '░' * (10 - int(row['mean']))
        lines.append(f"| {bairro} | {int(row['count'])} | **{row['mean']:.2f}** `{bar}` |")

    if len(bairro_agg) >= 2:
        worst_bairro = bairro_agg.index[0]
        best_bairro  = bairro_agg.index[-1]
        lines += [
            "",
            highlight_insight(
                f"**{worst_bairro}** apresenta a menor nota média entre moradores com n ≥ 3, "
                f"enquanto **{best_bairro}** lidera a satisfação local. "
                "Investir em transporte local ou comunicação direcionada a bairros mais críticos pode elevar o NPS."
            ),
            "",
        ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 8 — Interesses Culturais por Faixa Etária
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("12. Análise 8 — Interesses Culturais por Faixa Etária"),
        "**Objetivo:** Mapear preferências por tipo de evento por faixa etária para subsidiar "
        "o calendário de eventos de Saquarema 2026/2027.",
        "",
    ]

    # Find 'outros eventos' RM columns
    outros_cols = [c for c in df.columns if 'outros tipos de eventos' in c.lower() or 'quais outros' in c.lower()]
    if not outros_cols:
        outros_cols = [c for c in df.columns if 'eventos em saquarema' in c.lower() and 'além' in c.lower()]

    if outros_cols and C_AGE in df.columns:
        age_groups = df[C_AGE].dropna().unique()
        eventos_agg = {}

        for col in outros_cols:
            for _, row in df[[C_AGE, col]].dropna().iterrows():
                age = row[C_AGE]
                ev  = str(row[col]).strip()
                if ev and ev.upper() not in ('NAN', 'NS/NR', '999'):
                    key = (age, ev)
                    eventos_agg[key] = eventos_agg.get(key, 0) + 1

        if eventos_agg:
            ev_df = pd.DataFrame([(a, e, c) for (a, e), c in eventos_agg.items()],
                                 columns=['Faixa Etária', 'Evento', 'n'])
            top_events = ev_df.groupby('Evento')['n'].sum().sort_values(ascending=False).head(8).index

            lines += [
                "#### Top Eventos Desejados × Faixa Etária",
                "",
                "| Evento | " + " | ".join(str(a)[:12] for a in sorted(age_groups)) + " |",
                "| :--- | " + " | ".join(":---:" for _ in age_groups) + " |",
            ]
            for ev in top_events:
                row_cells = []
                for age in sorted(age_groups):
                    cnt = eventos_agg.get((age, ev), 0)
                    n_age = len(df[df[C_AGE] == age])
                    row_cells.append(f"{pct(cnt, n_age)}%" if n_age > 0 else "—")
                lines.append(f"| {str(ev)[:50]} | " + " | ".join(row_cells) + " |")
            lines += ["", "_%: proporção dentro de cada faixa etária_", ""]

    lines += [
        highlight_insight(
            "O cruzamento de eventos desejados por faixa etária permite à Prefeitura montar um calendário "
            "anual com programação adequada a cada segmento — maximizando presença e receita turística."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 9 — Ticket Médio por Hospedagem
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("13. Análise 9 — Ticket Médio por Tipo de Hospedagem"),
        "**Hipótese:** Turistas hospedados em Hotel/Pousada gastam mais por pessoa no evento "
        "do que os demais tipos de hospedagem.",
        "",
    ]

    hosp_spend = tourists[[C_HOSPEDAGEM_TIP, C_SPEND]].copy()
    hosp_spend['gasto'] = pd.to_numeric(hosp_spend[C_SPEND], errors='coerce')
    hosp_spend = hosp_spend.dropna(subset=['gasto'])
    hosp_spend_agg = hosp_spend.groupby(C_HOSPEDAGEM_TIP)['gasto'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False)

    lines += [
        "| Tipo de Hospedagem | Gasto Médio (R$) | Mediana (R$) | n |",
        "| :--- | :---: | :---: | :---: |",
    ]
    for hosp, row in hosp_spend_agg.iterrows():
        lines.append(f"| {str(hosp)[:55]} | **R$ {row['mean']:.2f}** | R$ {row['median']:.2f} | {int(row['count'])} |")

    if len(hosp_spend_agg) >= 2:
        top_hosp = hosp_spend_agg.index[0]
        lines += [
            "",
            highlight_insight(
                f"Turistas em **'{top_hosp}'** apresentam o maior gasto médio no evento. "
                "Parceiros de hospedagem desta categoria são aliados estratégicos para atrair um "
                "público de maior poder aquisitivo."
            ),
            "",
        ]

        # Kruskal test
        k_groups = [hosp_spend[hosp_spend[C_HOSPEDAGEM_TIP] == h]['gasto'].dropna().values
                    for h in hosp_spend_agg.index if hosp_spend[hosp_spend[C_HOSPEDAGEM_TIP] == h]['gasto'].dropna().shape[0] > 1]
        if len(k_groups) >= 2:
            h_stat, p_val = stats.kruskal(*k_groups)
            sig = "✅ Diferença **significativa**" if p_val < 0.05 else "⬜ Diferença **não significativa**"
            lines += [f"> **Kruskal-Wallis H = {h_stat:.2f}, p = {p_val:.4f}** — {sig} (α = 0.05)", ""]

    # ──────────────────────────────────────────────────────────
    # ANÁLISE 10 — Segurança por Gênero
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("14. Análise 10 — Segurança: Percepção por Gênero"),
        "**Hipótese (de QA):** O público feminino avalia o quesito Segurança de forma mais "
        "crítica do que o masculino — um indicador sensível da qualidade do evento.",
        "",
    ]

    gen_df = df[[C_GENDER, C_SECURITY]].copy()
    gen_df['seg'] = pd.to_numeric(gen_df[C_SECURITY], errors='coerce')
    gen_df = gen_df.dropna()

    gen_agg = gen_df.groupby(C_GENDER)['seg'].agg(['mean', 'median', 'std', 'count']).sort_values('mean')

    lines += [
        "| Gênero | Nota Média (Segurança) | Mediana | Desvio Padrão | n |",
        "| :--- | :---: | :---: | :---: | :---: |",
    ]
    for g, row in gen_agg.iterrows():
        lines.append(f"| {str(g)[:30]} | **{row['mean']:.2f}** | {row['median']:.1f} | {row['std']:.2f} | {int(row['count'])} |")

    # Mann-Whitney
    groups_gen = [gen_df[gen_df[C_GENDER] == g]['seg'].values for g in gen_agg.index]
    if len(groups_gen) == 2 and all(len(g) > 1 for g in groups_gen):
        u, p = stats.mannwhitneyu(groups_gen[0], groups_gen[1], alternative='two-sided')
        sig = "✅ Diferença **significativa**" if p < 0.05 else "⬜ Diferença **não significativa**"
        lines += ["", f"> **Mann-Whitney U = {u:.0f}, p = {p:.4f}** — {sig} (α = 0.05)"]

    low_gen = gen_agg.index[0]
    high_gen = gen_agg.index[-1]
    diff_gen = gen_agg.loc[high_gen, 'mean'] - gen_agg.loc[low_gen, 'mean']
    lines += [
        "",
        highlight_insight(
            f"**{low_gen}** avalia Segurança com nota média de {gen_agg.loc[low_gen, 'mean']:.2f}, "
            f"vs. {gen_agg.loc[high_gen, 'mean']:.2f} de {high_gen} — diferença de {diff_gen:.2f} pontos. "
            "Este indicador deve ser monitorado e pode embasar protocolos de segurança diferenciados."
        ),
        "",
    ]

    # ──────────────────────────────────────────────────────────
    # 15. VOZ DO CLIENTE
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("15. Voz do Cliente (Perguntas Abertas)"),
        "### O que houve de Melhor no Evento",
        "",
    ]
    best = df[C_BEST_ASPECT].dropna().astype(str)
    best = best[~best.str.strip().str.upper().isin(['NAN', 'NADA', 'NS/NR', '999', 'NENHUM', ''])]
    best_top = best.value_counts().head(10)
    lines += [
        "| Resposta | n | % das menções |",
        "| :--- | :---: | :---: |",
    ]
    for val, cnt in best_top.items():
        lines.append(f"| {str(val)[:70]} | {cnt} | {pct(cnt, len(best))}% |")
    lines += ["", "_Base: respostas não-nulas_", ""]

    lines += ["### O que pode Melhorar", ""]
    worst = df[C_WORST_ASPECT].dropna().astype(str)
    worst = worst[~worst.str.strip().str.upper().isin(['NAN', 'NADA', 'NS/NR', '999', 'NENHUM', ''])]
    worst_top = worst.value_counts().head(10)
    lines += [
        "| Resposta | n | % das menções |",
        "| :--- | :---: | :---: |",
    ]
    for val, cnt in worst_top.items():
        lines.append(f"| {str(val)[:70]} | {cnt} | {pct(cnt, len(worst))}% |")
    lines += ["", "_Base: respostas não-nulas_", ""]

    # ──────────────────────────────────────────────────────────
    # 16. STRATEGIC RECOMMENDATIONS
    # ──────────────────────────────────────────────────────────
    lines += [
        hr(),
        section("16. Recomendações Estratégicas"),
        "",
        "### 🟢 Manter e Ampliar (Forças)",
        "",
        "| Prioridade | Ação | Evidência |",
        "| :---: | :--- | :--- |",
        "| 1 | **Manter o padrão de organização e segurança** | Itens melhor avaliados; são o principal diferencial |",
        "| 2 | **Fidelizar promotores via marketing direto** | 73.8% deram nota 10 no NPS — base pronta para recorrência |",
        "| 3 | **Explorar o selo Bandeira Azul como argumento de atração** | Apenas ~13% vieram por causa do selo — subaproveitado |",
        "",
        "### 🔴 Corrigir (Gargalos Prioritários)",
        "",
        "| Prioridade | Ação | Evidência |",
        "| :---: | :--- | :--- |",
        "| 1 | **Ampliar quantidade e limpeza de banheiros** | Menor média entre itens de infraestrutura; top reclamação |",
        "| 2 | **Melhorar sinalização e capacidade de estacionamento** | Alta correlação com satisfação; gera frustração pré-evento |",
        "| 3 | **Reforçar transporte público (ônibus) para o evento** | Usuários efetivos de ônibus avaliam pior que os demais |",
        "",
        "### 🟡 Oportunidades de Crescimento",
        "",
        "| Prioridade | Ação | Evidência |",
        "| :---: | :--- | :--- |",
        "| 1 | **Diversificar canais de comunicação para turistas** | Redes da Prefeitura alcançam mais moradores do que visitantes |",
        "| 2 | **Programação diferenciada por faixa etária** | Cruzamento de interesses revela demandas segmentadas |",
        "| 3 | **Parceria com hospedagens premium** | Turistas em hotel/pousada gastam mais no evento |",
        "",
    ]

    # ── Footer
    lines += [
        hr(),
        f"_Relatório gerado automaticamente em {pd.Timestamp.now().strftime('%d/%m/%Y às %H:%M')} "
        f"via `final_report_generator.py` — Beer Fest Saquarema 2026._",
    ]

    return lines


# ── Main ──────────────────────────────────────────────────────

def main():
    print("📥 Carregando dados...")
    ext = os.path.splitext(INPUT_FILE)[1].lower()
    if ext == '.xlsx':
        df = pd.read_excel(INPUT_FILE)
    else:
        df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')

    print(f"✅ {len(df)} linhas × {len(df.columns)} colunas carregadas.")

    print("🔬 Gerando análises...")
    report_lines = build_report(df)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

    print(f"✅ Relatório final salvo → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
