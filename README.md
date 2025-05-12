# Dashboard de Análise da Escala 6x1

Um dashboard interativo para análise dos impactos da escala de trabalho 6x1 na vida dos trabalhadores, com visualizações organizadas em três abas principais: Dados Ocupacionais, Dados Pessoais e Percepção de Impacto.

![Dashboard Preview](https://via.placeholder.com/800x450?text=Dashboard+Preview)

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

Este dashboard foi desenvolvido para visualizar e analisar dados sobre os impactos da escala de trabalho 6x1 na vida dos trabalhadores. A aplicação permite visualizar estatísticas e gráficos interativos baseados nos dados armazenados em um banco de dados SQLite, organizados em três abas principais: Dados Ocupacionais, Dados Pessoais e Percepção de Impacto.

## ✨ Funcionalidades

- **Visualização de Dados Ocupacionais**: Gráficos interativos mostrando informações sobre tempo na escala 6x1, tipo de contrato, horas de trabalho, ocupações, CNAE e estado de trabalho.
- **Visualização de Dados Pessoais**: Gráficos interativos mostrando distribuição por idade, sexo, cor/raça, estado civil, filhos, rendimento e escolaridade.
- **Visualização de Percepção de Impacto**: Gráficos interativos mostrando os impactos da escala 6x1 na vida familiar, saúde física e mental dos trabalhadores.
- **KPIs**: Indicadores-chave de desempenho mostrando estatísticas importantes como percentual de trabalhadores na escala 6x1, distribuição por sexo e impactos mais frequentes.
- **Atualização de Dados**: Possibilidade de atualizar os gráficos com novos dados do banco de dados.
- **Design Responsivo**: Interface adaptável com layout organizado e cores profissionais.

## 📋 Requisitos

### Para Instalação Local
- Python 3.9 ou superior
- Pip (gerenciador de pacotes do Python)
- Bibliotecas Python: dash, pandas, plotly, spacy, nltk

### Para Instalação com Docker
- Docker
- Docker Compose

## 🚀 Instalação

### Instalação Local

1. Clone o repositório ou baixe os arquivos do projeto:

```bash
git clone https://github.com/seu-usuario/dashboard-escala-6x1.git
cd dashboard-escala-6x1
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Baixe os modelos e recursos necessários:

```bash
python -m spacy download pt_core_news_sm
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

4. Converta o arquivo Excel para SQLite (se ainda não tiver feito):

```bash
python excel_to_sqlite.py
```

5. Execute o aplicativo:

```bash
python app.py
```

6. Acesse o dashboard no navegador:

```
http://127.0.0.1:8050/
```

### Instalação com Docker

1. Clone o repositório ou baixe os arquivos do projeto:

```bash
git clone https://github.com/seu-usuario/dashboard-escala-6x1.git
cd dashboard-escala-6x1
```

2. Construa e inicie o contêiner Docker:

```bash
docker-compose up -d
```

> **Nota**: Se você encontrar um aviso sobre o atributo `version` estar obsoleto, edite o arquivo `docker-compose.yml` e remova a linha `version: '3'`.

3. Acesse o dashboard no navegador:

```
http://127.0.0.1:8050/
```

4. Para parar o contêiner:

```bash
docker-compose down
```

## 🖥️ Como Usar

### Dashboard

1. Ao abrir o aplicativo, você verá o dashboard com os seguintes elementos:
   - **KPIs**: Indicadores-chave no topo mostrando estatísticas gerais.
   - **Gráficos de Impacto**: Visualizações dos impactos na vida familiar, saúde física e mental.
   - **Distribuição por Estado**: Gráfico mostrando a distribuição dos respondentes por estado.

2. Para atualizar os dados após modificar a planilha base, clique no botão "Atualizar Dashboard" no canto superior direito.

### Atualização de Dados

1. Para atualizar os dados do dashboard, modifique o arquivo Excel base e execute o script de conversão para SQLite:

```bash
python excel_to_sqlite.py
```

2. Em seguida, reinicie o aplicativo ou clique no botão "Atualizar Dashboard" para ver os novos dados refletidos nos gráficos.

## 📁 Estrutura do Projeto

### Arquivos Necessários
- `app.py`: Arquivo principal contendo o código do dashboard, incluindo a definição do layout, callbacks e funções para criação de gráficos.
- `simple_nlp.py`: Módulo para análise de texto usando processamento de linguagem natural.
- `base.sqlite`: Banco de dados SQLite contendo os dados convertidos.
- `README.md`: Documentação do projeto.

### Arquivos de Configuração Docker
- `Dockerfile`: Configuração para construir a imagem Docker.
- `docker-compose.yml`: Configuração para orquestrar o contêiner Docker.
- `requirements.txt`: Lista de dependências Python necessárias.
- `.dockerignore`: Lista de arquivos a serem ignorados pelo Docker.

## 🛠️ Tecnologias Utilizadas

### Tecnologias de Desenvolvimento
- **Dash**: Framework para criação de aplicativos web analíticos em Python.
- **Plotly**: Biblioteca para criação de gráficos interativos.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **SQLite**: Sistema de gerenciamento de banco de dados relacional.
- **spaCy**: Biblioteca de código aberto para processamento de linguagem natural.
- **NLTK**: Natural Language Toolkit, biblioteca para processamento de linguagem natural.

### Tecnologias de Implantação
- **Docker**: Plataforma para desenvolvimento, envio e execução de aplicativos em contêineres.
- **Docker Compose**: Ferramenta para definir e executar aplicativos Docker multi-contêiner.

## ❓ Solução de Problemas

### Problemas com Docker

1. **Aviso sobre atributo `version` obsoleto**:
   - **Problema**: Ao executar `docker-compose up -d`, você recebe um aviso sobre o atributo `version` estar obsoleto.
   - **Solução**: Edite o arquivo `docker-compose.yml` e remova a linha `version: '3'`.

2. **Erro de permissão ao acessar o volume**:
   - **Problema**: O contêiner Docker não consegue acessar os arquivos no volume montado.
   - **Solução**: Verifique as permissões dos arquivos e diretórios. Em sistemas Windows, pode ser necessário ajustar as configurações de compartilhamento de arquivos no Docker Desktop.

3. **Porta 8050 já em uso**:
   - **Problema**: Ao iniciar o contêiner, você recebe um erro indicando que a porta 8050 já está em uso.
   - **Solução**: Pare qualquer aplicativo que esteja usando a porta 8050 ou altere a porta no arquivo `docker-compose.yml` (por exemplo, de `"8050:8050"` para `"8051:8050"`).

### Problemas com o Dashboard

1. **Erro ao carregar os dados**:
   - **Problema**: O dashboard não consegue carregar os dados do banco de dados SQLite.
   - **Solução**: Verifique se o arquivo `base.sqlite` existe e está no diretório correto. Se necessário, execute novamente o script `excel_to_sqlite.py`.

2. **Gráficos não aparecem**:
   - **Problema**: Os gráficos não são exibidos no dashboard.
   - **Solução**: Verifique se há dados suficientes para gerar os gráficos. Alguns gráficos podem não ser exibidos se não houver dados suficientes.

## 🎯 Conclusão

O Dashboard de Análise da Escala 6x1 é uma ferramenta completa para visualização e análise dos impactos da escala de trabalho 6x1 na vida dos trabalhadores. O projeto está finalizado e pronto para uso, oferecendo:

1. **Visualização Abrangente**: Três abas principais (Dados Ocupacionais, Dados Pessoais e Percepção de Impacto) que fornecem uma visão completa dos dados.

2. **Análise de Texto**: Implementação de processamento de linguagem natural para analisar as respostas de texto livre, identificando os principais tópicos mencionados pelos trabalhadores.

3. **Interface Intuitiva**: Design limpo e profissional com gráficos interativos e KPIs claros.

4. **Implantação Flexível**: Opções para execução local ou via Docker, facilitando a implantação em diferentes ambientes.

Este dashboard pode ser uma ferramenta valiosa para pesquisadores, gestores e formuladores de políticas interessados em entender os impactos da escala 6x1 na vida dos trabalhadores e desenvolver estratégias para mitigar seus efeitos negativos.

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
