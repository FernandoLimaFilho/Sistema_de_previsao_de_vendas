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
# Seleção do produto
# ---------------------------
abas = [ws.title for ws in spreadsheet.worksheets()]

# ---------------------------
# Formulário interativo
# ---------------------------
with st.form("form_previsao"):
    produto = st.selectbox("Escolha o produto:", [""] + abas)
    mes_previsto = st.date_input("Selecione o mês para previsão:")
    impacto_externo = st.radio(
        "Houve algum fator relevante que impacta as vendas?",
        ("Não", "Sim")
    )
    calcular = st.form_submit_button("Calcular previsão")

# ---------------------------
# Processamento após submissão
# ---------------------------
if calcular:
    if not produto:
        st.warning("⚠️ Por favor, selecione um produto.")
    elif not mes_previsto:
        st.warning("⚠️ Por favor, selecione o mês para previsão.")
    else:
        # Carregar dados do produto selecionado
        worksheet = spreadsheet.worksheet(produto)
        dados = worksheet.get_all_records()
        df = pd.DataFrame(dados)
        df["Data"] = pd.to_datetime(df["Data"])
        df["MM2"] = df["Qtd vendida"].rolling(2).mean()

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
        # Cálculo da previsão
        # ---------------------------
        ano_anterior = mes_previsto - relativedelta(years=1)
        mes1 = mes_previsto - relativedelta(months=1)
        mes2 = mes_previsto - relativedelta(months=2)

        venda_ano_anterior = df[df["Data"] == ano_anterior]["Qtd vendida"].sum()
        media_2meses = df[df["Data"].isin([mes1, mes2])]["Qtd vendida"].mean()

        if pd.isna(media_2meses):
            st.warning("⚠️ Base de dados incompleta! Alimente as vendas dos meses anteriores.")
        else:
            st.write(f"📊 Vendas {ano_anterior.strftime('%m/%Y')}: {venda_ano_anterior}")
            st.write(f"📊 Média 2 meses anteriores: {media_2meses}")

            limite = 0.2
            discrepante = abs(venda_ano_anterior - media_2meses) > limite * media_2meses

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
                    f"✅ Previsão de vendas para {produto} em {mes_previsto.strftime('%m/%Y')}: {previsao}"
                )
