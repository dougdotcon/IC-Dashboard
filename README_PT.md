# IC Dashboard

Um dashboard interativo desenvolvido para analisar os impactos da escala de trabalho 6x1 (6 dias trabalhados, 1 dia de folga) na vida dos trabalhadores. A aplicação permite visualizar estatísticas e gráficos interativos baseados em um banco de dados SQLite, organizados em três abas principais: Dados Ocupacionais, Dados Pessoais e Percepção de Impacto.

![Prévia do Dashboard](https://via.placeholder.com/800x450?text=Dashboard+Preview)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
  - [Instalação Local](#instalação-local)
  - [Instalação com Docker](#instalação-com-docker)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🔍 Visão Geral

Este dashboard foi criado para visualizar e analisar dados sobre os impactos da escala de trabalho 6x1 na vida dos trabalhadores. A aplicação exibe estatísticas e gráficos interativos baseados em dados armazenados em um banco de dados SQLite, divididos em três seções principais para facilitar a análise detalhada das tendências ocupacionais, demografia pessoal e os impactos percebidos na saúde física e mental.

## ✨ Funcionalidades

- **Visualização de Dados Ocupacionais**: Gráficos interativos mostrando informações sobre tempo na escala 6x1, tipo de contrato, horas de trabalho, ocupações, CNAE e estado de trabalho.
- **Visualização de Dados Pessoais**: Gráficos interativos mostrando distribuição por idade, sexo, cor/raça, estado civil, filhos, rendimento e escolaridade.
- **Visualização de Percepção de Impacto**: Gráficos interativos mostrando os impactos da escala 6x1 na vida familiar e na saúde física e mental dos trabalhadores.
- **KPIs (Indicadores-Chave de Desempenho)**: Métricas cruciais destacando estatísticas importantes, como o percentual de trabalhadores na escala 6x1, distribuição por sexo e impactos mais frequentes.
- **Atualização de Dados**: Funcionalidade para atualizar os gráficos com dados novos diretamente do banco de dados.
- **Design Responsivo**: Interface profissional, organizada com esquema de cores coeso e layout adaptável para diferentes tamanhos de tela.

## 📋 Requisitos

### Instalação Local
- Python 3.9 ou superior
- Pip (gerenciador de pacotes do Python)
- Bibliotecas Python: dash, pandas, plotly, spacy, nltk

### Instalação com Docker
- Docker
- Docker Compose

## 🚀 Instalação

### Instalação Local

1. Clone o repositório ou baixe os arquivos do projeto:

bash
git clone https://github.com/seu-usuario/ic-dashboard.git
cd ic-dashboard


2. Instale as dependências:

bash
pip install -r requirements.txt


3. Baixe os modelos e recursos necessários:

bash
python -m spacy download pt_core_news_sm
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"


4. Converta o arquivo Excel para SQLite (se ainda não tiver feito):

bash
python excel_to_sqlite.py


5. Execute o aplicativo:

bash
python app.py


6. Acesse o dashboard no navegador:


http://127.0.0.1:8050/


### Instalação com Docker

1. Clone o repositório ou baixe os arquivos do projeto.

2. Certifique-se de que o Docker e o Docker Compose estão instalados e em execução.

3. Construa e inicie os containers:

bash
docker-compose up --build


4. Acesse o dashboard no navegador:


http://localhost:8050


## 📂 Estrutura do Projeto


ic-dashboard/
├── app.py                 # Arquivo principal da aplicação (Lógica do Dash)
├── excel_to_sqlite.py     # Script para converter dados do Excel para SQLite
├── requirements.txt       # Dependências do Python
├── docker-compose.yml     # Configuração do Docker Compose
├── Dockerfile             # Definição da imagem Docker
├── data/
│   ├── source_data.xlsx   # Dados brutos em Excel (Entrada)
│   └── database.db        # Banco de dados SQLite gerado a partir do Excel
└── assets/
    └── style.css          # Folhas de estilo customizadas


## 🛠 Tecnologias Utilizadas

- **Framework**: Dash (Python)
- **Processamento de Dados**: Pandas
- **Visualização**: Plotly
- **NLP (PLN)**: SpaCy, NLTK (para análise de texto)
- **Banco de Dados**: SQLite
- **Containerização**: Docker

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar um Pull Request.

1. Faça um fork do projeto
2. Crie sua branch de funcionalidade (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFuncionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a Licença MIT. Veja o arquivo `LICENSE` para mais informações.
