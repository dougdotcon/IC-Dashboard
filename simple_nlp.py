"""
Análise de Texto Simples com PLN para as respostas da coluna "Impactos"
Este script implementa uma abordagem simples de PLN para analisar e agrupar
semanticamente as respostas de texto livre da coluna "Impactos".
"""

import sqlite3
import pandas as pd
import re
import spacy
from collections import Counter
from nltk.corpus import stopwords
import nltk

# Garantir que os recursos do NLTK estejam disponíveis
try:
    stopwords.words('portuguese')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')

# Carregar o modelo em português do spaCy
nlp = spacy.load('pt_core_news_sm')

# Definir tópicos predefinidos que esperamos encontrar nas respostas
predefined_topics = {
    'saude_mental': [
        'ansiedade', 'depressão', 'burnout', 'estresse', 'mental', 'psicológico', 'psicológica',
        'emocional', 'psicologicamente', 'emocionalmente', 'ansioso', 'depressivo', 'estressado',
        'estressante', 'psiquiátrico', 'psiquiátrica', 'psicológicos', 'saúde mental',
        'bem-estar mental', 'bem estar mental', 'transtorno', 'transtornos', 'esgotamento',
        'esgotado', 'esgotada', 'nervoso', 'nervosa', 'irritado', 'irritada', 'irritação',
        'nervosismo', 'pânico', 'síndrome do pânico', 'tristeza', 'triste', 'desânimo',
        'desanimado', 'desanimada', 'frustração', 'frustrado', 'frustrada', 'angústia',
        'angustiado', 'angustiada', 'sofrimento', 'sofrendo', 'sofro', 'psicológicamente',
        'mentalmente', 'emocionalmente', 'paciência', 'sem paciência', 'irritabilidade',
        'instabilidade', 'instável', 'humor', 'alteração de humor', 'crise', 'crises',
        'desespero', 'desesperado', 'desesperada', 'medicamento', 'antidepressivo', 'terapia'
    ],
    'saude_fisica': [
        'dor', 'dores', 'crônica', 'crônicas', 'coluna', 'joelho', 'joelhos', 'pé', 'pés',
        'varizes', 'variz', 'tendinite', 'gastrite', 'infecção', 'infecções', 'urinária',
        'urinárias', 'pressão alta', 'hipertensão', 'circulação', 'LER', 'DORT', 'cansaço',
        'fadiga', 'exaustão', 'físico', 'física', 'saúde física', 'problema de saúde',
        'doença', 'doenças', 'problemas físicos', 'machucado', 'machucada', 'lesão', 'lesões',
        'desgaste', 'articulação', 'articulações', 'músculo', 'músculos', 'postura', 'ergonomia'
    ],
    'familia': [
        'família', 'filho', 'filhos', 'filha', 'filhas', 'pai', 'pais', 'mãe', 'mães',
        'cônjuge', 'marido', 'esposa', 'esposo', 'parente', 'parentes', 'famíliares',
        'evento familiar', 'aniversário', 'reunião escolar', 'data comemorativa', 'festa',
        'natal', 'ano novo', 'tempo com família', 'convívio familiar', 'ausência', 'ausente',
        'distanciamento', 'distante', 'culpa', 'culpado', 'culpada', 'presença', 'acompanhar',
        'criação dos filhos', 'educação dos filhos', 'perder momentos', 'momentos em família'
    ],
    'vida_social': [
        'amigo', 'amigos', 'amiga', 'amigas', 'social', 'socialização', 'isolamento',
        'isolado', 'isolada', 'sozinho', 'sozinha', 'solidão', 'perda de amigos',
        'afastamento', 'afastado', 'afastada', 'convívio social', 'sair', 'encontro',
        'eventos sociais', 'festa com amigos', 'relação social', 'relações sociais',
        'falta de tempo para amigos', 'sem tempo para socializar', 'recluso', 'reclusa'
    ],
    'autocuidado_e_lazer': [
        'lazer', 'hobby', 'hobbies', 'atividade física', 'exercício', 'exercícios', 'academia',
        'caminhada', 'esporte', 'esportes', 'viagem', 'viajar', 'férias', 'descanso',
        'relaxamento', 'relaxar', 'diversão', 'divertir', 'cinema', 'teatro', 'museu',
        'cultura', 'cultural', 'passatempo', 'prazer', 'bem-estar', 'bem estar',
        'autocuidado', 'cuidado pessoal', 'saúde pessoal', 'tempo para mim', 'tempo livre',
        'folga para lazer', 'abandonar hobbies', 'sem tempo para lazer'
    ],
    'jornada_e_carga_horaria': [
        'jornada', 'carga horária', 'folga', 'folgas', 'descanso insuficiente', 'hora extra',
        'horas extras', 'trabalhar demais', 'escala', 'escala 6x1', 'excesso de trabalho',
        'trabalho intenso', 'exhaustivo', 'exaustivo', 'exaustiva', 'cansativo', 'cansativa',
        'cansaço', 'fadiga', 'esgotamento', 'viver para trabalhar', 'sem tempo para descansar',
        'trabalhar muito', 'rotina pesada', 'rotina exaustiva', 'horário longo', 'turno longo'
    ],
    'ambiente_de_trabalho': [
        'assédio', 'assédio moral', 'pressão', 'meta', 'metas', 'liderança', 'líder',
        'chefe', 'tóxico', 'tóxica', 'ambiente hostil', 'hostilidade', 'desrespeito',
        'falta de reconhecimento', 'rotatividade', 'punição', 'punições', 'injustiça',
        'injusto', 'injusta', 'cobrança', 'cobranças', 'intimidação', 'humilhação',
        'desvalorização', 'desvalorizado', 'desvalorizada', 'clima ruim', 'ambiente ruim'
    ],
    'remuneracao_e_direitos': [
        'salário', 'salários', 'baixo', 'baixa', 'remuneração', 'pagamento', 'benefício',
        'benefícios', 'falta de benefícios', 'feriado', 'banco de horas', 'direito',
        'direitos', 'trabalhista', 'trabalhistas', 'atestado', 'folga remunerada',
        'insuficiente', 'salário insuficiente', 'exploração', 'explorado', 'explorada',
        'sem direitos', 'injustiça trabalhista'
    ],
    'tarefas_domesticas': [
        'tarefa', 'tarefas', 'doméstica', 'domésticas', 'casa', 'limpeza', 'limpar',
        'lavar', 'roupa', 'roupas', 'cozinhar', 'cozinha', 'afazeres', 'afazeres domésticos',
        'organização', 'organizar', 'acúmulo', 'acumular', 'folga para tarefas',
        'sem tempo para casa', 'casa bagunçada', 'manutenção da casa', 'cuidado com a casa'
    ],
    'logistica_e_transportes': [
        'transporte', 'transportes', 'deslocamento', 'trajeto', 'viagem', 'ônibus',
        'metrô', 'trânsito', 'tempo de deslocamento', 'longo trajeto', 'cansaço no transporte',
        'tempo perdido', 'distância', 'longe', 'chegar cansado', 'chegar cansada',
        'transporte público', 'dependência de transporte'
    ],
    'alimentacao_e_sono': [
        'alimentação', 'comida', 'refeição', 'refeições', 'irregular', 'ultraprocessado',
        'ultraprocessados', 'comer mal', 'pular refeição', 'pular refeições', 'fast food',
        'sono', 'insônia', 'dormir', 'sono irregular', 'sono insuficiente', 'noite mal dormida',
        'acordar cansado', 'acordar cansada', 'falta de sono', 'má alimentação',
        'problemas digestivos', 'gastrite'
    ],
    'dificuldade_em_estudar': [
        'estudo', 'estudos', 'estudar', 'faculdade', 'curso', 'cursos', 'escola',
        'educação', 'abandono', 'abandonar', 'trancar', 'desistir', 'sem tempo para estudar',
        'falta de tempo para estudo', 'cansaço para estudar', 'conciliar estudo',
        'dificuldade em estudar', 'atraso nos estudos', 'parar de estudar'
    ],
    'profissionalizacao': [
        'profissionalização', 'qualificação', 'carreira', 'mudar de carreira', 'progressão',
        'crescimento profissional', 'capacitação', 'curso profissionalizante', 'estagnação',
        'estagnado', 'estagnada', 'sem tempo para qualificação', 'falta de oportunidade',
        'preso no emprego', 'preso na escala', 'melhorar de vida'
    ],
    'desigualdade_de_genero': [
        'gênero', 'mulher', 'mulheres', 'mãe', 'mães', 'maternidade', 'dupla jornada',
        'jornada dupla', 'carga dupla', 'mãe solo', 'mãe solteira', 'cuidado com filhos',
        'responsabilidade', 'sobrecarga', 'desigualdade', 'machismo', 'sexismo',
        'discriminação', 'papel de gênero', 'tarefas femininas', 'carga doméstica'
    ],
    'precarizacao_financeira': [
        'financeiro', 'financeira', 'dinheiro', 'dívida', 'dívidas', 'conta', 'contas',
        'pagar', 'salário insuficiente', 'falta de dinheiro', 'pobreza', 'precarização',
        'precariedade', 'gastar', 'despesa', 'despesas', 'economia', 'crise financeira',
        'sem condições', 'falta de recursos', 'endividado', 'endividada'
    ],
    'acesso_a_servicos_publicos': [
        'serviço', 'serviços', 'público', 'públicos', 'banco', 'bancos', 'burocracia',
        'burocrático', 'SUS', 'consulta', 'exame', 'vacina', 'documento', 'documentos',
        'resolver', 'pendência', 'pendências', 'horário', 'incompatibilidade de horário',
        'fila', 'atendimento', 'acesso', 'dificuldade de acesso', 'sem tempo para resolver'
    ],
    'criticas_a_escala_6x1': [
        'escala', '6x1', 'escala 6x1', 'desumano', 'desumana', 'escravidão', 'escravo',
        'escrava', 'exploração', 'injusto', 'injusta', 'denúncia', 'crítica', 'reclamação',
        'mudar escala', '5x2', 'escala 5x2', '4x3', 'escala 4x3', 'reforma trabalhista',
        'trabalhista', 'sistema', 'sistema trabalhista', 'abolir 6x1', 'melhor escala'
    ],
    'grupos_vulneraveis': [
        'vulnerável', 'vulneráveis', 'mãe solo', 'mãe solteira', 'doença crônica',
        'doenças crônicas', 'deficiência', 'deficiente', 'idoso', 'idosa', 'minorias',
        'necessidades especiais', 'condição especial', 'doente', 'saúde frágil',
        'dependente', 'dependentes', 'carga extra', 'dificuldade extra', 'desafios adicionais'
    ]
}

def preprocess_text(text):
    """
    Pré-processa o texto para análise.

    Args:
        text: Texto a ser processado

    Returns:
        list: Lista de tokens processados
    """
    if pd.isna(text) or text == '':
        return []

    # Converter para minúsculas e remover caracteres especiais
    text = re.sub(r'[^\w\s]', ' ', str(text).lower())

    # Processar com spaCy
    doc = nlp(text)

    # Remover stopwords e lematizar
    stop_words = set(stopwords.words('portuguese'))
    tokens = [token.lemma_ for token in doc
              if token.text.lower() not in stop_words
              and not token.is_punct
              and len(token.text) > 2]

    return tokens

def classify_response(text):
    """
    Classifica uma resposta nos tópicos predefinidos.

    Args:
        text: Texto da resposta

    Returns:
        dict: Dicionário com os tópicos encontrados e suas contagens
    """
    if pd.isna(text) or text == '':
        return {}

    # Pré-processar o texto
    tokens = preprocess_text(text)
    text_lower = text.lower()

    # Verificar cada tópico
    found_topics = {}

    for topic, keywords in predefined_topics.items():
        # Verificar se alguma palavra-chave está presente nos tokens
        if any(token in keywords for token in tokens):
            found_topics[topic] = 1
            continue

        # Verificar se alguma palavra-chave está presente no texto original
        # (para capturar frases compostas)
        if any(keyword in text_lower for keyword in keywords):
            found_topics[topic] = 1

    return found_topics

def analyze_impacts(df):
    """
    Analisa as respostas da coluna "Impactos" e retorna a contagem de tópicos.

    Args:
        df: DataFrame com a coluna 'Impactos'

    Returns:
        dict: Dicionário com os tópicos e suas contagens
    """
    # Filtrar apenas as respostas não vazias
    df_impacts = df[df['Impactos'].notna() & (df['Impactos'] != '')]

    # Se não houver respostas, retornar um dicionário vazio
    if len(df_impacts) == 0:
        return {}

    # Classificar cada resposta
    all_topics = {}

    for _, row in df_impacts.iterrows():
        topics = classify_response(row['Impactos'])
        for topic in topics:
            all_topics[topic] = all_topics.get(topic, 0) + 1

    # Ordenar por contagem (decrescente)
    sorted_topics = {k: v for k, v in sorted(all_topics.items(), key=lambda item: item[1], reverse=True)}

    # Formatar os nomes dos tópicos para exibição
    formatted_topics = {}
    topic_names = {
        'saude_mental': 'Saúde Mental',
        'saude_fisica': 'Saúde Física',
        'familia': 'Família',
        'vida_social': 'Vida Social',
        'autocuidado_e_lazer': 'Autocuidado e Lazer',
        'jornada_e_carga_horaria': 'Jornada e Carga Horária',
        'ambiente_de_trabalho': 'Ambiente de Trabalho',
        'remuneracao_e_direitos': 'Remuneração e Direitos',
        'tarefas_domesticas': 'Tarefas Domésticas',
        'logistica_e_transportes': 'Logística e Transportes',
        'alimentacao_e_sono': 'Alimentação e Sono',
        'dificuldade_em_estudar': 'Dificuldade em Estudar',
        'profissionalizacao': 'Profissionalização',
        'desigualdade_de_genero': 'Desigualdade de Gênero',
        'precarizacao_financeira': 'Precarização Financeira',
        'acesso_a_servicos_publicos': 'Acesso a Serviços Públicos',
        'criticas_a_escala_6x1': 'Críticas à Escala 6x1',
        'grupos_vulneraveis': 'Grupos Vulneráveis'
    }

    for topic, count in sorted_topics.items():
        formatted_name = topic_names.get(topic, topic.replace('_', ' ').title())
        formatted_topics[formatted_name] = count

    return formatted_topics

def get_impact_data_for_graph(df):
    """
    Prepara os dados para o gráfico de barras.

    Args:
        df: DataFrame com a coluna 'Impactos'

    Returns:
        tuple: (topics, counts) para criar o gráfico
    """
    topic_counts = analyze_impacts(df)

    # Preparar listas para o gráfico
    topics = list(topic_counts.keys())
    counts = list(topic_counts.values())

    return topics, counts

# Função para teste
if __name__ == "__main__":
    # Conectar ao banco de dados
    conn = sqlite3.connect('base.sqlite')
    df = pd.read_sql("SELECT * FROM Planilha1", conn)
    conn.close()

    # Analisar os impactos
    topic_counts = analyze_impacts(df)

    # Imprimir os resultados
    print("\nContagem de tópicos encontrados:")
    for topic, count in topic_counts.items():
        print(f"{topic}: {count}")
