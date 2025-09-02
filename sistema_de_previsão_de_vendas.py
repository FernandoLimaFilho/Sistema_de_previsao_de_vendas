# app_previsao_vendas.py

import streamlit as st
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------
# Configuração do Streamlit
# ---------------------------
st.set_page_config(
    page_title="Previsão de Vendas",
    page_icon="📈",
    layout="wide",
)

st.title("📊 Sistema de Previsão de Vendas")
st.markdown(
    "Aplicativo interativo para previsão de vendas com base em séries históricas e médias móveis."
)

# ---------------------------
# Conexão com Google Sheets via st.secrets
# ---------------------------
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scopes
)
client = gspread.authorize(creds)
spreadsheet = client.open("Series temporais de vendas")

# ---------------------------
# Seleção do Produto
# ---------------------------
abas = [ws.title for ws in spreadsheet.worksheets()]
produto = st.selectbox("Escolha o produto:", [""] + abas)  # "" evita seleção inicial

if produto:  # só executa depois que o usuário escolheu o produto
    # Carregar dados
    worksheet = spreadsheet.worksheet(produto)
    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)
    df["Data"] = pd.to_datetime(df["Data"])
    df["MM2"] = df["Qtd vendida"].rolling(2).mean()

    # Criando colunas de ano e mês
    df["Ano"] = df["Data"].dt.year
    df["Mes"] = df["Data"].dt.month

    # ---------------------------
    # Gráfico interativo
    # ---------------------------
    fig = px.line(
        df,
        x="Data",
        y=["Qtd vendida", "MM2"],
        title=f"Série Temporal de Vendas - {produto}",
        markers=True,
        template="plotly_white"
    )
    fig.update_traces(selector=dict(name="Qtd vendida"), line=dict(color="gold", width=3))
    fig.update_traces(selector=dict(name="MM2"), line=dict(color="black", width=3, dash="dash"))
    fig.update_layout(
        title_font=dict(size=22, family="Arial", color="black"),
        xaxis_title="Período (mês/ano)",
        yaxis_title="Quantidade Vendida",
        xaxis=dict(showgrid=True, tickformat="%b %Y"),
        yaxis=dict(showgrid=True),
        hovermode="x unified",
        legend_title="Legenda"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # Seleção do mês para previsão
    # ---------------------------
    mes_previsto = st.date_input("Selecione o mês para previsão:")

    if mes_previsto:  # só calcula depois que o usuário escolheu a data
        # Meses de referência
        ano_anterior = mes_previsto - relativedelta(years=1)
        mes1 = mes_previsto - relativedelta(months=1)
        mes2 = mes_previsto - relativedelta(months=2)

        # ---------------------------
        # Vendas do mesmo mês do ano anterior
        # ---------------------------
        venda_ano_anterior = df[
            (df["Ano"] == ano_anterior.year) & (df["Mes"] == ano_anterior.month)
        ]["Qtd vendida"].sum()

        # ---------------------------
        # Média dos 2 meses anteriores
        # ---------------------------
        media_2meses = df[
            ((df["Ano"] == mes1.year) & (df["Mes"] == mes1.month)) |
            ((df["Ano"] == mes2.year) & (df["Mes"] == mes2.month))
        ]["Qtd vendida"].mean()

        if pd.isna(media_2meses):
            st.warning("⚠️ Base de dados incompleta! Alimente as vendas dos meses anteriores.")
        else:
            st.write(f"📊 Vendas {ano_anterior.strftime('%m/%Y')}: {venda_ano_anterior}")
            st.write(f"📊 Média 2 meses anteriores: {media_2meses:.2f}")

            limite = 0.2
            discrepante = abs(venda_ano_anterior - media_2meses) > limite * media_2meses

            # ---------------------------
            # Fator externo
            # ---------------------------
            impacto_externo = st.radio(
                "Houve algum fator relevante que impacta as vendas?",
                ("Não", "Sim")
            )

            previsao = None
            if not discrepante:
                if impacto_externo == "Não":
                    previsao = venda_ano_anterior
                else:
                    ajuste = st.number_input("Digite o ajuste manual:", value=0)
                    previsao = venda_ano_anterior + ajuste
            else:
                if impacto_externo == "Sim":
                    ajuste = st.number_input("Digite o ajuste manual:", value=0)
                    previsao = media_2meses + ajuste
                else:
                    st.info("⚠️ Base discrepante. Analise os dados antes de definir a previsão manualmente.")

            if previsao is not None:
                st.success(
                    f"✅ Previsão de vendas para {produto} em {mes_previsto.strftime('%m/%Y')}: {previsao:.2f}"
                )
