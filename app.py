from datetime import datetime
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


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


def gerar_relatorio_pdf(
    dados: pd.DataFrame,
    titulo: str,
    total_grupo: float,
    saldo_atual: float,
    rendimento_atual: float,
    semana: int,
) -> bytes:
    buffer = BytesIO()
    documento = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
        title=titulo,
        author="Vamos Poupar",
    )
    estilos = getSampleStyleSheet()
    titulo_estilo = ParagraphStyle(
        "TituloRelatorio",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F5132"),
        fontSize=20,
        spaceAfter=8,
    )
    elementos = [
        Paragraph("Vamos Poupar — Relatório de pagamentos", titulo_estilo),
        Paragraph(
            f"Gerado em {datetime.now():%d/%m/%Y às %H:%M}",
            estilos["BodyText"],
        ),
        Spacer(1, 0.5 * cm),
        Paragraph("Visão geral do grupo", estilos["Heading2"]),
    ]

    resumo_geral = Table(
        [
            ["Total aportado", "Saldo no Mercado Pago", "Rendimento", "Semana atual"],
            [moeda(total_grupo), moeda(saldo_atual), moeda(rendimento_atual), f"{semana} de 52"],
        ],
        colWidths=[6 * cm] * 4,
    )
    resumo_geral.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF6EF")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#66756E")),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#173126")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTSIZE", (0, 1), (-1, 1), 14),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#DCE8E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DCE8E1")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    elementos.extend([
        resumo_geral,
        Spacer(1, 0.25 * cm),
        Paragraph(f"Progresso anual: <b>{semana / 52:.0%} concluído</b>", estilos["BodyText"]),
        Spacer(1, 0.45 * cm),
        Paragraph(titulo, estilos["Heading2"]),
    ])

    total_selecao = float(dados["Valor"].sum())
    pagos_selecao = int(dados["Situação"].astype(str).str.contains("Pago").sum())
    pendentes_selecao = len(dados) - pagos_selecao
    resumo_selecao = Table(
        [["Total aportado", "Meses pagos", "Meses pendentes"], [moeda(total_selecao), pagos_selecao, pendentes_selecao]],
        colWidths=[8 * cm] * 3,
    )
    resumo_selecao.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF6EF")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DCE8E1")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos.extend([resumo_selecao, Spacer(1, 0.4 * cm)])

    mensal_pdf = dados.groupby("Mês", as_index=False)["Valor"].sum().set_index("Mês").reindex(MESES, fill_value=0)
    meses_coluna_esquerda = MESES[:7]
    meses_coluna_direita = MESES[7:]

    def tabela_periodo(meses_periodo: list[str]) -> Table:
        linhas_periodo = [["Mês", "Valor"]] + [
            [mes, moeda(float(mensal_pdf.loc[mes, "Valor"]))]
            for mes in meses_periodo
        ]
        tabela = Table(linhas_periodo, colWidths=[5.5 * cm, 5.5 * cm])
        tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#177245")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EAF6EF")]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DCE8E1")),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return tabela

    tabela_mensal = Table(
        [[tabela_periodo(meses_coluna_esquerda), tabela_periodo(meses_coluna_direita)]],
        colWidths=[11.7 * cm, 11.7 * cm],
        hAlign="CENTER",
    )
    tabela_mensal.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elementos.extend([
        Spacer(1, 0.3 * cm),
        KeepTogether([
            Paragraph("Arrecadação por mês", estilos["Heading2"]),
            tabela_mensal,
        ]),
        PageBreak(),
    ])

    elementos.extend([Paragraph("Controle de pagamentos", estilos["Heading2"]), Spacer(1, 0.2 * cm)])

    cabecalho = list(dados.columns)
    linhas = [cabecalho]
    for _, registro in dados.iterrows():
        linhas.append([
            moeda(float(valor)) if coluna == "Valor" else str(valor).replace("✅ ", "").replace("⏳ ", "")
            for coluna, valor in registro.items()
        ])

    larguras = [6.2 * cm, 4.2 * cm, 4.2 * cm, 5.2 * cm] if "Nome" in cabecalho else [7 * cm, 6 * cm, 7 * cm]
    tabela_pdf = Table(linhas, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    tabela_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#177245")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EAF6EF")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DCE8E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabela_pdf)

    def desenhar_rodape(canvas_pdf, documento_pdf) -> None:
        canvas_pdf.saveState()
        canvas_pdf.setStrokeColor(colors.HexColor("#DCE8E1"))
        canvas_pdf.line(1.2 * cm, 0.8 * cm, landscape(A4)[0] - 1.2 * cm, 0.8 * cm)
        canvas_pdf.setFont("Helvetica", 8)
        canvas_pdf.setFillColor(colors.HexColor("#66756E"))
        canvas_pdf.drawString(1.2 * cm, 0.45 * cm, "Vamos Poupar")
        canvas_pdf.drawRightString(
            landscape(A4)[0] - 1.2 * cm,
            0.45 * cm,
            f"Página {documento_pdf.page}",
        )
        canvas_pdf.restoreState()

    documento.build(elementos, onFirstPage=desenhar_rodape, onLaterPages=desenhar_rodape)
    return buffer.getvalue()


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

coluna_filtro, coluna_relatorio = st.columns([2, 1], vertical_alignment="bottom")
with coluna_filtro:
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

titulo_detalhes = (
    "Desempenho do grupo"
    if filtro_pessoa == "Todos os integrantes"
    else f"Resumo de {filtro_pessoa}"
)
tabela = df_filtrado[["Nome", "Mês", "Valor", "Situação"]].copy()
if filtro_pessoa != "Todos os integrantes":
    tabela = tabela[["Mês", "Valor", "Situação"]]
nome_arquivo = (
    "relatorio-todos-os-integrantes.pdf"
    if filtro_pessoa == "Todos os integrantes"
    else f"relatorio-{filtro_pessoa.lower().replace(' ', '-')}.pdf"
)

with coluna_relatorio:
    st.download_button(
        "Baixar relatório em PDF",
        data=gerar_relatorio_pdf(
            tabela,
            titulo_detalhes,
            total_aportado,
            saldo_atual_mp,
            rendimento,
            semana_atual,
        ),
        file_name=nome_arquivo,
        mime="application/pdf",
        type="primary",
        icon=":material/download:",
        width="stretch",
        help="Baixa um relatório completo da visualização selecionada.",
    )

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
    subtitulo = "Acompanhe a arrecadação total em cada mês."
else:
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
    st.dataframe(
        tabela,
        width="stretch",
        hide_index=True,
        column_config={"Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")},
    )

st.divider()
st.caption(f"Dados atualizados em {datetime.now():%d/%m/%Y às %H:%M} • Vamos Poupar")
