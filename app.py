import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------
st.set_page_config(
    page_title="Vamos Poupar",
    layout="wide",
)

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

for month in df.loc[:, "Janeiro":"Dezembro"].columns:
    df[month] = pd.to_numeric(df[month], errors='coerce').fillna(0).astype(np.float64)

for month in df.loc[:, "Janeiro":"Dezembro"].columns:
    df["status_" + month] = df[month].apply(lambda x: "Pago" if x > 0 else "Pendente")

df["Status"] = df["status_Janeiro"]

# -----------------------------
# MÉTRICAS
# -----------------------------
total_integrantes = len(df)
pagos = (df["Status"] == "Pago").sum()
pendentes = (df["Status"] == "Pendente").sum()

total_arrecadado_mes = []
for month in df.loc[:, "Janeiro":"Dezembro"].columns:
    total_arrecadado_mes.append(df[month].sum())

total_arrecadado = np.sum(total_arrecadado_mes)

# Progresso do desafio (Janeiro pago = 4 semanas de 52)
progresso = 4 / 52

# -----------------------------
# TÍTULO
# -----------------------------
st.title("💰 Desafio das 52 Semanas – Vamos Poupar")
st.caption("Pouquinho por semana, resultado grande no final")

# -----------------------------
# CARDS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total acumulado", f"R$ {total_arrecadado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    st.metric("👥 Integrantes", total_integrantes)

with col3:
    st.metric("✅ Pagamentos em dia", pagos)

with col4:
    st.metric("⚠️ Pendentes", pendentes)

# -----------------------------
# PROGRESSO
# -----------------------------
st.subheader("📈 Progresso do desafio")
st.progress(progresso)
st.caption(f"{int(progresso * 100)}% concluído do desafio anual")

# -----------------------------
# FILTROS
# -----------------------------
st.subheader("📋 Controle de pagamentos")
filtro_status = st.selectbox("Filtrar por status", ["Todos", "Pago", "Pendente"])

if filtro_status != "Todos":
    df_filtrado = df[df["Status"] == filtro_status]
else:
    df_filtrado = df.copy()

# Ícones de status
def status_icon(status):
    return "✅ Pago" if status == "Pago" else "❌ Pendente"

df_filtrado["Status"] = df_filtrado["Status"].apply(status_icon)

st.dataframe(df_filtrado, use_container_width=True)

# -----------------------------
# GRÁFICO
# -----------------------------
st.subheader("📊 Arrecadação por mês (MVP)")

grafico_df = pd.DataFrame({
    "Mês": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
    "Valor": total_arrecadado_mes
})

st.bar_chart(grafico_df.set_index("Mês"))

# -----------------------------
# RODAPÉ
# -----------------------------
st.divider()
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
