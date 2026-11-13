
# Data Pilot

Aplicação interativa para exploração e análise de dados de vendas. O projeto apresenta um painel construído com Streamlit e oferece duas formas de consultar os indicadores por linguagem natural, usando modelos disponibilizados pelo OpenRouter.

Faz parte do Boot Camp da DIO - Santander - Dados com Python e IA.

O Expert não compartilhou o repositorio e os scripts foram gerados a partir dos vídeos das aulas. Adequações foram implementadas para suprir ausência de informações.

## Funcionalidades

- Painel de vendas com filtro por categoria.
- Indicadores de receita, pedidos e ticket médio.
- Gráfico de receita mensal e rankings dos cinco principais clientes e produtos. Esse ranking faz parte da entrega ao que foi proposto como desafio.
- Chat com os dados, com respostas geradas a partir de indicadores calculados pelo projeto.
- Chat com uso de funções para consultar métricas de vendas.
- Pré-processamento do CSV de origem, com normalização de dados e geração de receita e mês da venda.

## Tecnologias

- **Python 3.15 ou superior**, conforme declarado em `pyproject.toml`.
- **Streamlit** para a interface web.
- **Pandas** para leitura, transformação e análise dos dados.
- **Plotly** para visualizações interativas.
- **OpenRouter** e os pacotes Python `openrouter` e `openai` para integração com modelos de linguagem.
- **python-dotenv** para carregar configurações locais do arquivo de ambiente.
- **uv** para gerenciar o ambiente e instalar as dependências definidas no projeto.
- **Tkinter** (biblioteca padrão do Python) para selecionar o CSV ao executar o pré-processamento.

## Pré-requisitos

- Python **3.15 ou superior**.
- [uv](https://docs.astral.sh/uv/).
- Uma chave de API do [OpenRouter](https://openrouter.ai/) para usar os recursos de chat. O painel e os indicadores locais não dependem dessa chave.

## Estrutura do projeto

```text
Data Pilot/
├── data/
│   └── sales.csv                  # Dados de origem
├── data_processed/
│   └── sales_clean.csv            # Dados tratados, usados pelo painel
├── src/
│   ├── app.py                     # Painel e páginas de chat
│   ├── llm.py                     # Integração com o OpenRouter
│   ├── metrics.py                 # Cálculo dos indicadores de vendas
│   ├── preprocess.py              # Limpeza e preparação do CSV
│   └── data_pilot/
│       └── __init__.py
├── .env.example                   # Modelo das variáveis de ambiente
├── main.py                        # Entrada da aplicação Streamlit
├── pyproject.toml                 # Metadados e dependências do projeto
├── uv.lock                        # Versões resolvidas das dependências
└── README.md
```

## Instalação e execução

Os comandos abaixo usam o PowerShell no Windows e devem ser executados a partir da pasta do projeto.

1. **Instale o Python e o uv**, caso ainda não estejam disponíveis. A versão do Python precisa atender ao requisito `>=3.15`.

2. **Abra a pasta do projeto** no terminal:

   ```powershell
   cd "C:\caminho\para\Data Pilot"
   ```

3. **Crie o ambiente virtual e instale as dependências** usando o arquivo de lock:

   ```powershell
   uv sync
   ```

4. **Configure o acesso ao OpenRouter.** Faça uma cópia do modelo de configuração:

   ```powershell
   Copy-Item .env.example .env
   ```

   Edite o arquivo `.env` recém-criado e substitua `YOUR_OPENROUTER_API_KEY` por sua chave. A variável `OPENROUTER_MODEL` já vem com o valor `openrouter/free`; altere-o somente se quiser selecionar outro modelo disponível na sua conta. Não compartilhe nem publique sua chave.

5. **Inicie a aplicação:**

   ```powershell
   uv run streamlit run main.py
   ```

6. Abra no navegador o endereço local exibido pelo Streamlit (normalmente `http://localhost:8501`).

## Dados e pré-processamento

O painel carrega `data_processed/sales_clean.csv`. Esse arquivo já está incluído no projeto. Se ele não existir, a aplicação tenta executar o pré-processamento, que abre uma janela para selecionar o CSV de origem. Selecione `data/sales.csv`. A janela para escolher o arquivo CSV de origem é uma melhoria em relação ao que foi apresentado pelo Expert, onde um arquivo pré-definido no código era utilizado.

O arquivo sales.csv também foi criado para a entrega do desafio da DIO, uma vez que aquele usado pelo Expert nas aulas não estava disponível. A estrutura dos dados é a mesma apresentada nos slides.

Também é possível executar o tratamento manualmente, a partir da raiz do projeto:

```powershell
uv run python src/preprocess.py
```

O script remove linhas duplicadas, normaliza o status dos pedidos, cria a coluna de mês e calcula a receita por linha. O resultado é gravado em `data_processed/sales_clean.csv`.

## Configuração da API

O arquivo `.env.example` documenta as variáveis esperadas:

| Variável | Descrição |
| --- | --- |
| `OPENROUTER_API_KEY` | Chave necessária para enviar perguntas aos recursos de chat. |
| `OPENROUTER_MODEL` | Identificador do modelo usado pelo OpenRouter. O padrão do exemplo é `openrouter/free`. |

Sem uma chave configurada, o painel de indicadores continua disponível, mas os recursos de chat não conseguem consultar o modelo.

## Telas da Aplicação
<img width="1906" height="902" alt="DataPilot_01" src="https://github.com/user-attachments/assets/09c90003-9e8c-4cf5-be38-bd945ecd559c" />

Após aplicar o filtro pela categoria "Utilidades", observamos que os valores exibidos são modificados de acordo com o filtro. Também é possível selecionar mais de uma categoria ao mesmo tempo.
<img width="1909" height="897" alt="DataPilot_02" src="https://github.com/user-attachments/assets/620cb27f-fbec-4a55-b5b4-3ce1bd60bdda" />

