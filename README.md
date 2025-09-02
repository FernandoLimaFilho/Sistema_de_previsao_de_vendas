# 📊 Sistema de Previsão de Vendas

Este repositório contém um **aplicativo Streamlit** para previsão de vendas, baseado em séries temporais de dados históricos.  
O app conecta-se ao **Google Sheets** para obter os dados e realiza cálculos de médias móveis, comparação com o ano anterior e ajustes manuais para previsão.

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

---

## 🔑 Configuração de Credenciais (Google Sheets)

Para que o app funcione, é necessário criar uma conta de serviço no Google Cloud e configurar as credenciais:

1. **Criar credenciais no Google Cloud**
   - Acesse [Google Cloud Console](https://console.cloud.google.com/).
   - Crie um projeto (ou use um já existente).
   - Vá em **APIs e Serviços > Credenciais**.
   - Clique em **Criar credenciais > Conta de serviço**.
   - Gere a chave no formato **JSON** e baixe o arquivo.

2. **Compartilhar a planilha**
   - Abra sua planilha no Google Sheets.
   - Copie o e-mail da conta de serviço (algo como `meu-projeto@meu-id.iam.gserviceaccount.com`).
   - Compartilhe a planilha com esse e-mail, dando permissão de **Leitura/Editor**.

3. **Configurar no Streamlit**
   - No seu projeto, crie a pasta `.streamlit` na raiz.
   - Dentro dela, crie o arquivo `secrets.toml`.
   - Copie o conteúdo do JSON de credenciais e adicione em `secrets.toml` no seguinte formato:

```toml
[gcp_service_account]
type = "service_account"
project_id = "seu-project-id"
private_key_id = "sua-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nSEU-PRIVATE-KEY\n-----END PRIVATE KEY-----\n"
client_email = "seu-email-de-servico@seu-projeto.iam.gserviceaccount.com"
client_id = "seu-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/seu-email-de-servico%40seu-projeto.iam.gserviceaccount.com"
