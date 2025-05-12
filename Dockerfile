FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de requisitos
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar spaCy e baixar o modelo em português
RUN pip install --no-cache-dir spacy && \
    python -m spacy download pt_core_news_sm

# Instalar NLTK e baixar recursos necessários
RUN pip install --no-cache-dir nltk && \
    python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Copiar o código-fonte
COPY . .

# Expor a porta que o Dash usa
EXPOSE 8050

# Comando para iniciar o aplicativo
CMD ["python", "app.py"]
