from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Vamos Poupar",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        --green: #177245;
        --green-dark: #0f5132;
        --green-soft: #eaf6ef;
        --ink: #173126;
        --muted: #66756e;
        --line: #dce8e1;
    }

    .stApp { background: #f7faf8; }
    .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }

    .hero {
        padding: 2rem;
        border-radius: 24px;
        color: white;
        background: linear-gradient(135deg, #0f5132 0%, #208b57 70%, #45aa72 100%);
        box-shadow: 0 18px 45px rgba(15, 81, 50, .18);
        margin-bottom: 1.4rem;
    }
    .hero-kicker { font-size: .78rem; font-weight: 800; letter-spacing: .12em; opacity: .8; }
    .hero h1 { color: white; font-size: clamp(1.8rem, 5vw, 3rem); margin: .35rem 0 .4rem; }
    .hero p { margin: 0; font-size: 1.05rem; opacity: .9; }

    .section-title { margin: 1.75rem 0 .2rem; color: var(--ink); font-size: 1.35rem; font-weight: 750; }
    .section-copy { color: var(--muted); margin: 0 0 1rem; }

    div[data-testid="stMetric"] {
        height: 100%;
        padding: 1rem 1.1rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: white;
        box-shadow: 0 6px 20px rgba(23, 49, 38, .05);
    }
    div[data-testid="stMetricLabel"] { color: var(--muted); }
    div[data-testid="stMetricValue"] { color: var(--ink); font-size: clamp(1.35rem, 3vw, 2rem); }

    div[data-testid="stSelectbox"] > label { font-weight: 700; color: var(--ink); }
    div[data-baseweb="select"] > div { border-radius: 12px; background: white; }

    .progress-copy { display: flex; justify-content: space-between; color: var(--muted); font-size: .9rem; }
    .contribution-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: .75rem;
    }
    .contribution-card {
        min-width: 0;
        padding: 1rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: white;
        box-shadow: 0 6px 20px rgba(23, 49, 38, .05);
    }
    .contribution-month {
        display: block;
        margin-bottom: .35rem;
        color: var(--muted);
        font-size: .88rem;
        font-weight: 650;
        white-space: nowrap;
    }
    .contribution-value {
        display: block;
        color: var(--ink);
        font-size: clamp(1.15rem, 2vw, 1.5rem);
        font-weight: 750;
        white-space: nowrap;
    }
    .contribution-card.current-month {
        border-color: #208b57;
        background: linear-gradient(135deg, #177245, #2c9b64);
        box-shadow: 0 10px 26px rgba(23, 114, 69, .22);
    }
    .contribution-card.current-month .contribution-month,
    .contribution-card.current-month .contribution-value { color: white; }
    .contribution-card.past-month {
        border-color: #e2e7e4;
        background: #f0f3f1;
        box-shadow: none;
        opacity: .58;
    }
    .contribution-card.past-month .contribution-month,
    .contribution-card.past-month .contribution-value { color: #68736d; }
    .current-month-badge {
        display: inline-block;
        margin-top: .55rem;
        padding: .16rem .45rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, .18);
        color: white;
        font-size: .68rem;
        font-weight: 750;
        letter-spacing: .04em;
        text-transform: uppercase;
    }
    .person-chip {
        display: inline-block; padding: .25rem .7rem; margin-bottom: .8rem;
        border-radius: 999px; color: var(--green-dark); background: var(--green-soft); font-weight: 700;
    }
    div[data-testid="stDataFrame"], div[data-testid="stPlotlyChart"] {
        border: 1px solid var(--line); border-radius: 18px; overflow: hidden; background: white;
    }
    hr { border-color: var(--line); }
    footer { visibility: hidden; }

    @media (max-width: 640px) {
        .block-container { padding: 1rem .85rem 2rem; }
        .hero { padding: 1.35rem; border-radius: 18px; }
        .hero p { font-size: .95rem; }
        div[data-testid="stHorizontalBlock"] { gap: .65rem; }
        div[data-testid="column"] { min-width: calc(50% - .4rem) !important; flex: 1 1 calc(50% - .4rem) !important; }
        div[data-testid="stMetric"] { padding: .85rem; border-radius: 14px; }
        div[data-testid="stMetricValue"] { font-size: 1.25rem; }
        .section-title { font-size: 1.2rem; }
        .contribution-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .6rem; }
        .contribution-card { padding: .85rem; border-radius: 14px; }
        .contribution-value { font-size: 1.12rem; }
    }
    @media (max-width: 360px) {
        .contribution-grid { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]
ARQUIVO_PAGAMENTOS = Path(__file__).with_name("pagamentos.csv")
ARQUIVO_SALDO = Path(__file__).with_name("saldo.csv")


def moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_dados() -> tuple[pd.DataFrame, pd.DataFrame]:
    mensal = pd.read_csv(ARQUIVO_PAGAMENTOS, encoding="utf-8-sig")
    colunas_obrigatorias = ["Nome", *MESES]
    colunas_ausentes = [coluna for coluna in colunas_obrigatorias if coluna not in mensal.columns]
    if colunas_ausentes:
        raise ValueError(f"Colunas ausentes no CSV: {', '.join(colunas_ausentes)}")

    mensal = mensal[colunas_obrigatorias].copy()
    mensal["Nome"] = mensal["Nome"].astype(str).str.strip()
    mensal[MESES] = mensal[MESES].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    longo = mensal.melt(id_vars="Nome", value_vars=MESES, var_name="Mês", value_name="Valor")
    longo["Status"] = np.where(longo["Valor"] > 0, "Pago", "Pendente")
    longo["Situação"] = np.where(longo["Valor"] > 0, "✅ Pago", "⏳ Pendente")
    return mensal, longo


def carregar_saldo() -> float:
    saldo_df = pd.read_csv(ARQUIVO_SALDO, encoding="utf-8-sig")
    if "SaldoAtual" not in saldo_df.columns or saldo_df.empty:
        raise ValueError("saldo.csv deve conter a coluna SaldoAtual")
    saldo = pd.to_numeric(saldo_df.loc[0, "SaldoAtual"], errors="coerce")
    if pd.isna(saldo) or saldo < 0:
        raise ValueError("o saldo atual deve ser um número maior ou igual a zero")
    return float(saldo)


try:
    df, df_long = carregar_dados()
    saldo_atual_mp = carregar_saldo()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as erro:
    st.error(f"Não foi possível carregar os arquivos de dados: {erro}")
    st.stop()

nomes = sorted(df["Nome"].dropna().unique().tolist())
hoje = datetime.now().date()
semana_atual = max(1, min(52, hoje.isocalendar().week))
progresso = semana_atual / 52

st.markdown(
    """
    <section class="hero">
        <div class="hero-kicker">DESAFIO DAS 52 SEMANAS</div>
        <h1>💰 Vamos Poupar</h1>
        <p>Pouquinho por semana, um resultado grande no final.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

filtro_pessoa = st.selectbox(
    "Visualizar movimentações de",
    ["Todos os integrantes"] + nomes,
    help="Selecione uma pessoa para ver seus aportes e pagamentos.",
)

df_filtrado = df_long if filtro_pessoa == "Todos os integrantes" else df_long[df_long["Nome"] == filtro_pessoa]
aporte_por_pessoa = df.assign(Aporte_Total=df[MESES].sum(axis=1))[["Nome", "Aporte_Total"]]
total_aportado = float(aporte_por_pessoa["Aporte_Total"].sum())
diferenca_saldo = saldo_atual_mp - total_aportado
rendimento = max(0.0, diferenca_saldo)

st.markdown('<div class="section-title">Visão geral do grupo</div>', unsafe_allow_html=True)
st.markdown('<p class="section-copy">Saldo, aportes e andamento do desafio em um só lugar.</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total aportado", moeda(total_aportado))
c2.metric("Saldo", moeda(saldo_atual_mp))
c3.metric("Rendimento", moeda(rendimento))
c4.metric("Semana atual", f"{semana_atual} de 52")

if diferenca_saldo < 0:
    st.warning(
        f"O saldo informado está {moeda(abs(diferenca_saldo))} abaixo dos pagamentos registrados. "
        "Atualize o valor em saldo.csv para calcular o rendimento corretamente."
    )

st.markdown('<div class="section-title">Progresso anual</div>', unsafe_allow_html=True)
st.progress(progresso)
st.markdown(
    f'<div class="progress-copy"><span>Semana {semana_atual}</span><strong>{progresso:.0%} concluído</strong></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Próximos aportes</div>', unsafe_allow_html=True)
st.markdown('<p class="section-copy">Valores planejados para manter o grupo no ritmo.</p>', unsafe_allow_html=True)
proximos_aportes = [
    ("Janeiro", 10),
    ("Fevereiro", 26),
    ("Março", 55),
    ("Abril", 82),
    ("Maio", 90),
    ("Junho", 120),
    ("Julho", 133),
    ("Agosto", 140),
    ("Setembro", 154),
    ("Outubro", 170),
    ("Novembro", 186),
    ("Dezembro", 202),
]
mes_atual = MESES[hoje.month - 1]
cards_aportes = "".join(
    f'<div class="contribution-card '
    f'{"current-month" if MESES.index(mes) == hoje.month - 1 else "past-month" if MESES.index(mes) < hoje.month - 1 else "future-month"}">'
    f'<span class="contribution-month">🗓️ {mes}</span>'
    f'<span class="contribution-value">{moeda(valor)}</span>'
    f'{"<span class=\"current-month-badge\">Mês atual</span>" if mes == mes_atual else ""}'
    "</div>"
    for mes, valor in proximos_aportes
)
st.markdown(f'<div class="contribution-grid">{cards_aportes}</div>', unsafe_allow_html=True)

st.divider()
if filtro_pessoa == "Todos os integrantes":
    titulo_detalhes = "Desempenho do grupo"
    subtitulo = "Acompanhe a arrecadação total em cada mês."
else:
    titulo_detalhes = f"Resumo de {filtro_pessoa}"
    subtitulo = "Confira os aportes realizados e o que ainda está pendente."

st.markdown(f'<div class="section-title">{titulo_detalhes}</div>', unsafe_allow_html=True)
st.markdown(f'<p class="section-copy">{subtitulo}</p>', unsafe_allow_html=True)

total_filtrado = float(df_filtrado["Valor"].sum())
pagos = int((df_filtrado["Status"] == "Pago").sum())
pendentes = int((df_filtrado["Status"] == "Pendente").sum())

if filtro_pessoa != "Todos os integrantes":
    r1, r2, r3 = st.columns(3)
    r1.metric("Total aportado", moeda(total_filtrado))
    r2.metric("Meses pagos", pagos)
    r3.metric("Meses pendentes", pendentes)

tab_grafico, tab_pagamentos = st.tabs(["📊 Arrecadação", "📋 Pagamentos"])

with tab_grafico:
    grafico_df = df_filtrado.groupby("Mês", as_index=False)["Valor"].sum()
    fig = px.bar(
        grafico_df,
        x="Mês",
        y="Valor",
        category_orders={"Mês": MESES},
        text_auto=".2s",
        color_discrete_sequence=["#208b57"],
    )
    fig.update_traces(marker_line_width=0, hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>")
    fig.update_layout(
        height=390,
        margin=dict(l=12, r=12, t=25, b=12),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title=None,
        yaxis_title="Valor (R$)",
        yaxis=dict(gridcolor="#edf2ef"),
        font=dict(color="#173126"),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

with tab_pagamentos:
    tabela = df_filtrado[["Nome", "Mês", "Valor", "Situação"]].copy()
    if filtro_pessoa != "Todos os integrantes":
        tabela = tabela[["Mês", "Valor", "Situação"]]
    st.dataframe(
        tabela,
        width="stretch",
        hide_index=True,
        column_config={"Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")},
    )

st.divider()
st.caption(f"Dados atualizados em {datetime.now():%d/%m/%Y às %H:%M} • Vamos Poupar")
