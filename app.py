import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime



# -----------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------
st.set_page_config(page_title="Vamos Poupar", layout="wide")

st.markdown("""
<style>
/* empurra o conteúdo pra baixo por causa da barra fixa */
.block-container { padding-top: 5.2rem; }

/* Top bar fixa */
.topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    padding: 0.75rem 1.25rem;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(49, 51, 63, 0.12);
}

/* Conteúdo da topbar */
.topbar-inner {
    max-width: 1200px;
    margin: 0 auto;
}

/* Título da topbar */
.topbar-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 0.35rem;
}

/* Ajustes de selectbox dentro da topbar */
.topbar div[data-testid="stSelectbox"] * {
    font-size: 16px !important;
}
.topbar div[data-testid="stSelectbox"] div[role="combobox"]{
    border-radius: 14px !important;
    padding: 8px 10px !important;
    border: 1px solid rgba(49, 51, 63, 0.20) !important;
    background: rgba(255, 255, 255, 0.70) !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06) !important;
}

/* Barra horizontal rolável */
.people-bar {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 6px 2px 10px 2px;
  scrollbar-width: thin;
}
.people-bar::-webkit-scrollbar { height: 8px; }
.people-bar::-webkit-scrollbar-thumb { border-radius: 999px; }

/* Botões estilo "pill" + não quebra linha */
.people-bar button {
  border-radius: 999px !important;
  padding: 6px 14px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border: 1px solid rgba(49, 51, 63, 0.25) !important;
  background-color: white !important;
  color: #222 !important;
  white-space: nowrap !important;      /* <-- NÃO QUEBRA */
  min-width: max-content !important;   /* <-- AJUSTA AO TEXTO */
}

/* Hover */
.people-bar button:hover {
  border-color: #2E7D32 !important;
  color: #2E7D32 !important;
}

/* Ativo */
.people-bar .active button {
  background-color: #2E7D32 !important;
  color: white !important;
  border-color: #2E7D32 !important;
}

</style>
""", unsafe_allow_html=True)





# -----------------------------
# DADOS (MVP)
# -----------------------------
data = [
    {"Nome": "Davi", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Delzuita", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Edmundo", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Fabiana", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Marcos", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Kellianny", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Maria Socorro", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Marisa", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "João Vitor", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Katarine", "Janeiro": 10, "Fevereiro": 26, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
]

df = pd.DataFrame(data)
# st.write("Dados carregados com sucesso.")
# st.write(df)
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

# Garantir numérico
for m in meses:
    df[m] = pd.to_numeric(df[m], errors="coerce").fillna(0).astype(float)

# -----------------------------
# TRANSFORMA EM FORMATO LONGO (melhor p/ filtro)
# -----------------------------
df_long = df.melt(
    id_vars=["Nome"],
    value_vars=meses,
    var_name="Mês",
    value_name="Valor",
)

df_long["Status"] = np.where(df_long["Valor"] > 0, "Pago", "Pendente")
df_long["StatusIcon"] = np.where(df_long["Status"] == "Pago", "✅ Pago", "❌ Pendente")

# -----------------------------
# TÍTULO
# -----------------------------
st.title("💰 Vamos Poupar – Desafio das 52 Semanas")
st.caption("Pouquinho por semana, resultado grande no final")


if "filtro_pessoa" not in st.session_state:
    st.session_state.filtro_pessoa = "Todos"



# -----------------------------
# TOP BAR – BOTÕES DE PESSOA
# -----------------------------
st.markdown('<div class="topbar"><div class="topbar-inner">', unsafe_allow_html=True)
st.markdown('<div class="topbar-title">👥 Integrantes</div>', unsafe_allow_html=True)

nomes = ["Todos"] + sorted(df_long["Nome"].unique().tolist())

cols = st.columns(len(nomes))

for col, nome in zip(cols, nomes):
    with col:
        classe = "person-btn-active" if st.session_state.filtro_pessoa == nome else "person-btn"
        with st.container():
            st.markdown(f'<div class="{classe}">', unsafe_allow_html=True)
            if st.button(nome, key=f"btn_{nome}"):
                st.session_state.filtro_pessoa = nome
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Usa o valor selecionado
filtro_pessoa = st.session_state.filtro_pessoa



# -----------------------------
# SALDO MERCADO PAGO (MANUAL) + RENDIMENTO (GERAL DO GRUPO)
# Opção A: proporcional ao total aportado de cada pessoa
# -----------------------------
st.subheader("💳 Mercado Pago – Saldo e rendimento (geral do grupo)")

c_mp1, c_mp2 = st.columns([1, 2])

# with c_mp1:
#     saldo_atual_mp = st.number_input(
#         "Saldo atual no Mercado Pago (R$)",
#         min_value=0.0,
#         value=0.0,
#         step=10.0,
#         help="Digite o valor atual que aparece na sua conta Mercado Pago.",
#     )
saldo_atual_mp = 334.66
# Total aportado por pessoa e geral (NÃO depende dos filtros)
aporte_por_pessoa = df[["Nome"] + meses].copy()
aporte_por_pessoa["Aporte_Total"] = aporte_por_pessoa[meses].sum(axis=1)

total_aportado_geral = float(aporte_por_pessoa["Aporte_Total"].sum())

st.write(f"Total aportado pelo grupo até agora: R$ {total_aportado_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


# Rendimento total (geral)
rendimento_total = saldo_atual_mp - total_aportado_geral
# Se estiver negativo (saldo ainda não bate com aportes), zera para não confundir
rendimento_total = max(0.0, rendimento_total)

# Distribuição do rendimento por pessoa (Opção A: proporcional ao aporte)
if total_aportado_geral > 0 and rendimento_total > 0:
    aporte_por_pessoa["Rendimento"] = (aporte_por_pessoa["Aporte_Total"] / total_aportado_geral) * rendimento_total
else:
    aporte_por_pessoa["Rendimento"] = 0.0

aporte_por_pessoa["Saldo (Aporte+Rend)"] = aporte_por_pessoa["Aporte_Total"] + aporte_por_pessoa["Rendimento"]

# Cards (gerais do grupo)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(
        "💰 Total aportado (geral)",
        f"R$ {total_aportado_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
with c2:
    st.metric(
        "💳 Saldo atual (MP)",
        f"R$ {saldo_atual_mp:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
with c3:
    st.metric(
        "📈 Rendimento total (geral)",
        f"R$ {rendimento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

st.divider()
# -----------------------------
# FILTROS (globais da página)
# -----------------------------

c1, c2 = st.columns([1, 2])

with c1:
    pass




df_f = df_long.copy()

if filtro_pessoa != "Todos":
    escondeInfo = False
    df_f = df_f[df_f["Nome"] == filtro_pessoa]
else:
    escondeInfo = True
    pass


# -----------------------------
# MÉTRICAS (baseadas no filtro)
# -----------------------------
total_integrantes = df_f["Nome"].nunique()
pagos = (df_f["Status"] == "Pago").sum()
pendentes = (df_f["Status"] == "Pendente").sum()
total_arrecadado = df_f["Valor"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    if filtro_pessoa == "Todos":
        st.metric("💰 Total geral", f"R$ {total_arrecadado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") )
    else:
        st.metric("💰 Total (filtro)", f"R$ {total_arrecadado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    if filtro_pessoa == "Todos":
        st.metric("👥 Integrantes", total_integrantes)    
    else:
        st.metric("👥 Integrantes (filtro)", total_integrantes)

with col3:
        if filtro_pessoa == "Todos":
            pass
           # st.metric("✅ Pagos", pagos)
        else:
            st.metric("✅ Total Meses Pagos (filtro)", pagos)

with col4:
        if filtro_pessoa == "Todos":
            pass
          #  st.metric("⚠️ Pendentes", pendentes)
        else:
            st.metric("⚠️ Total Meses Pendentes (filtro)", pendentes)

# -----------------------------
# PROGRESSO (mantive seu fixo)
# -----------------------------
# -----------------------------
# PROGRESSO BASEADO NA DATA ATUAL (52 semanas)
# -----------------------------
hoje = datetime.now().date()

# Semana ISO do ano (pode chegar a 53 em alguns anos)
semana_atual = hoje.isocalendar().week

# Garantir que o progresso fique entre 1 e 52
semana_atual = max(1, min(52, semana_atual))

progresso = semana_atual / 52



st.subheader("📈 Progresso do desafio ")
st.progress(progresso)
st.caption(f"Estamos na semana {semana_atual} e {int(progresso * 100)} % concluído do desafio anual")

st.divider()
st.subheader("Aporte para os meses seguintes")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🗓️ Janeiro", "R$ 10,00")
with col2:
    st.metric("🗓️ Fevereiro", "R$ 26,00")
with col3:
    st.metric("🗓️ Março", "R$ 55,00")
with col4:
    st.metric("🗓️ Abril", "R$ 62,00")
    
    
# with col1:
#     st.metric("🗓️ Maio", "R$ 90,00")
# with col2:
#     st.metric("🗓️ Junho", "R$ 106,00")
# with col3:
#     st.metric("🗓️ Julho", "R$ 122,00")
# with col4:
#     st.metric("🗓️ Agosto", "R$ 138,00")
    
    
# with col1:
#     st.metric("🗓️ Setembro", "R$ 154,00")
# with col2:
#     st.metric("🗓️ Outubro", "R$ 170,00")
# with col3:
#     st.metric("🗓️ Novembro", "R$ 186,00")
# with col4:
#     st.metric("🗓️ Dezembro", "R$ 202,00")

# colocar o PIX aqui
st.subheader("💳 PIX para os meses seguintes")
st.write("Chave PIX: (47)99618-1477)")
st.write("Nome: Marcos Aurélio Araujo Costa")


st.divider()
# -----------------------------
# TABELA
# -----------------------------
st.subheader("📋 Controle de pagamentos (filtrado)")

tabela = df_f[["Nome", "Mês", "Valor", "StatusIcon"]].rename(columns={"StatusIcon": "Status"})

if filtro_pessoa != "Todos" and "Nome" in tabela.columns.to_list():
    tabela = tabela[["Mês", "Valor", "Status"]]


if filtro_pessoa != "Todos":
    st.dataframe(tabela, use_container_width=True, hide_index=True)

# -----------------------------
# GRÁFICO (filtrado)
# -----------------------------
if filtro_pessoa == "Todos": 
    st.subheader("📊 Arrecadação por mês")
else:
    st.subheader(f"📊 Arrecadação por mês (filtrado)")

import plotly.express as px

grafico_df = (
    df_f.groupby("Mês", as_index=False)["Valor"].sum()
)

fig = px.bar(
    grafico_df,
    x="Mês",
    y="Valor",
    category_orders={"Mês": meses},
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# RODAPÉ
# -----------------------------
st.divider()
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
