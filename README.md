# 📊 Sistema de Previsão de Vendas

Este repositório contém um **aplicativo Streamlit** para previsão de vendas, baseado em séries temporais de dados históricos. O app conecta-se ao **Google Sheets** para obter os dados e realiza cálculos de médias móveis, comparação com o ano anterior e ajustes manuais para previsão.

O objetivo é fornecer uma **interface interativa** para análise e projeção de vendas de diferentes produtos, facilitando a tomada de decisão.

---

## 🔹 Funcionalidades

- Conexão segura com Google Sheets via `st.secrets`.
- Seleção de produtos disponíveis na planilha.
- Gráficos interativos de vendas históricas com Plotly.
- Cálculo de **média móvel 2 meses**.
- Comparação das vendas do mesmo mês do **ano anterior**.
- Ajuste manual de previsão considerando fatores externos.
- Fluxo sequencial que evita cálculos automáticos antes da interação do usuário.
