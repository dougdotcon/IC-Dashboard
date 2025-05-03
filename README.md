# Dashboard de Análise da Escala 6x1

Um dashboard interativo para análise dos impactos da escala de trabalho 6x1 na vida dos trabalhadores.

![Dashboard Preview](https://via.placeholder.com/800x450?text=Dashboard+Preview)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🔍 Visão Geral

Este dashboard foi desenvolvido para visualizar e analisar dados sobre os impactos da escala de trabalho 6x1 na vida dos trabalhadores. A aplicação permite visualizar estatísticas, gráficos e também adicionar novos dados à base.

## ✨ Funcionalidades

- **Visualização de Dados**: Gráficos interativos mostrando os impactos da escala 6x1 na vida familiar, saúde física e mental dos trabalhadores.
- **KPIs**: Indicadores-chave de desempenho mostrando estatísticas importantes.
- **Filtros**: Possibilidade de filtrar os dados por diferentes critérios.
- **Adição de Dados**: Interface para adicionar novos dados à base.
- **Design Responsivo**: Interface adaptável a diferentes tamanhos de tela.

## 📋 Requisitos

- Python 3.7 ou superior
- Pip (gerenciador de pacotes do Python)
- Bibliotecas Python: dash, pandas, plotly, sqlite3

## 🚀 Instalação

1. Clone o repositório ou baixe os arquivos do projeto:

```bash
git clone https://github.com/seu-usuario/dashboard-escala-6x1.git
cd dashboard-escala-6x1
```

2. Instale as dependências necessárias:

```bash
pip install pandas openpyxl dash plotly
```

3. Converta o arquivo Excel para SQLite (se ainda não tiver feito):

```bash
python excel_to_sqlite.py
```

4. Execute o aplicativo:

```bash
python app.py
```

5. Acesse o dashboard no navegador:

```
http://127.0.0.1:8050/
```

## 🖥️ Como Usar

### Dashboard

1. Ao abrir o aplicativo, você verá a aba "Dashboard" com os seguintes elementos:
   - **KPIs**: Indicadores-chave no topo mostrando estatísticas gerais.
   - **Gráficos de Impacto**: Visualizações dos impactos na vida familiar, saúde física e mental.
   - **Distribuição por Estado**: Gráfico mostrando a distribuição dos respondentes por estado.

2. Para atualizar os dados após adicionar novas entradas, clique no botão "Atualizar Dashboard" no canto superior direito.

### Adicionar Novos Dados

1. Clique na aba "Adicionar Dados" para acessar o formulário de entrada de dados.

2. Preencha os campos do formulário:
   - **Informações de Trabalho**: Escala 6x1, tempo na escala, contrato, horas, ocupação e estado.
   - **Informações Pessoais**: Sexo, escolaridade e rendimento.
   - **Avaliação de Impactos**: Impacto na vida familiar, saúde física e mental.
   - **Descrição dos Impactos**: Campo de texto para descrever os impactos em detalhes.

3. Clique no botão "Adicionar Dados" para salvar as informações na base de dados.

4. Volte para a aba "Dashboard" e clique em "Atualizar Dashboard" para ver os novos dados refletidos nos gráficos.

## 📁 Estrutura do Projeto

- `app.py`: Arquivo principal contendo o código do dashboard.
- `excel_to_sqlite.py`: Script para converter o arquivo Excel para SQLite.
- `base.xlsx`: Arquivo Excel com os dados originais.
- `base.sqlite`: Banco de dados SQLite contendo os dados convertidos.
- `README.md`: Documentação do projeto.

## 🛠️ Tecnologias Utilizadas

- **Dash**: Framework para criação de aplicativos web analíticos em Python.
- **Plotly**: Biblioteca para criação de gráficos interativos.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **SQLite**: Sistema de gerenciamento de banco de dados relacional.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

1. Faça um fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido com ❤️ usando Dash e Plotly.
