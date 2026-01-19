import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------
st.set_page_config(page_title="Vamos Poupar", layout="wide")

# -----------------------------
# DADOS (MVP)
# -----------------------------
data = [
    {"Nome": "Davi", "Janeiro": 0, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Delzuita", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Edmundo", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Fabiana", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Marcos", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Kellianny", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Maria Socorro", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "Marisa", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
    {"Nome": "João Vitor", "Janeiro": 10, "Fevereiro": 0, "Março": 0, "Abril": 0, "Maio": 0, "Junho": 0, "Julho": 0, "Agosto": 0, "Setembro": 0, "Outubro": 0, "Novembro": 0, "Dezembro": 0},
]

df = pd.DataFrame(data)

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
st.title("💰 Desafio das 52 Semanas – Vamos Poupar")
st.caption("Pouquinho por semana, resultado grande no final")

# -----------------------------
# FILTROS (globais da página)
# -----------------------------
st.subheader("🔎 Filtros")
c1, c2 = st.columns(2)

with c1:
    filtro_pessoa = st.selectbox(
        "Filtrar por pessoa",
        options=["Todos"] + sorted(df_long["Nome"].unique().tolist())
    )

with c2:
    filtro_mes = st.selectbox(
        "Filtrar por mês",
        options=["Todos"] + meses
    )

df_f = df_long.copy()

if filtro_pessoa != "Todos":
    df_f = df_f[df_f["Nome"] == filtro_pessoa]

if filtro_mes != "Todos":
    df_f = df_f[df_f["Mês"] == filtro_mes]

# -----------------------------
# MÉTRICAS (baseadas no filtro)
# -----------------------------
total_integrantes = df_f["Nome"].nunique()
pagos = (df_f["Status"] == "Pago").sum()
pendentes = (df_f["Status"] == "Pendente").sum()
total_arrecadado = df_f["Valor"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total (filtro)", f"R$ {total_arrecadado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    st.metric("👥 Integrantes (filtro)", total_integrantes)

with col3:
    st.metric("✅ Pagos (filtro)", pagos)

with col4:
    st.metric("⚠️ Pendentes (filtro)", pendentes)

# -----------------------------
# PROGRESSO (mantive seu fixo)
# -----------------------------
progresso = 4 / 52
st.subheader("📈 Progresso do desafio")
st.progress(progresso)
st.caption(f"{int(progresso * 100)}% concluído do desafio anual")

# -----------------------------
# TABELA
# -----------------------------
st.subheader("📋 Controle de pagamentos (filtrado)")

tabela = df_f[["Nome", "Mês", "Valor", "StatusIcon"]].rename(columns={"StatusIcon": "Status"})
st.dataframe(tabela, use_container_width=True, hide_index=True)

# -----------------------------
# GRÁFICO (filtrado)
# -----------------------------
st.subheader("📊 Arrecadação por mês (filtrado)")

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
