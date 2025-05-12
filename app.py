import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import sqlite3
from dash.exceptions import PreventUpdate
from simple_nlp import get_impact_data_for_graph

# Definir cores e estilo - Nova paleta profissional
COLORS = {
    'background': '#f4f6f8',  # Cinza claro para fundo
    'text': '#2D3436',        # Cor de texto principal
    'title': '#34495E',       # Cor para títulos
    'primary': '#2C3E50',     # Azul escuro como cor primária
    'secondary': '#00C9A7',   # Ciano para destaques
    'accent': '#F39C12',      # Laranja para acentos
    'success': '#27AE60',     # Verde para sucesso
    'warning': '#F1C40F',     # Amarelo para avisos
    'danger': '#E74C3C',      # Vermelho para erros
    'chart1': '#3498DB',      # Azul para gráficos
    'chart2': '#2980B9',      # Azul mais escuro
    'chart3': '#1ABC9C',      # Verde-água
    'chart4': '#16A085'       # Verde-água mais escuro
}

# Estilo global
GLOBAL_STYLE = {
    'fontFamily': '"Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif',
    'backgroundColor': COLORS['background'],
    'color': COLORS['text'],
    'margin': '0px',
    'padding': '30px',
    'minHeight': '100vh',
}

CARD_STYLE = {
    'boxShadow': '0 4px 12px 0 rgba(0, 0, 0, 0.05)',
    'borderRadius': '12px',
    'backgroundColor': 'white',
    'padding': '25px',
    'marginBottom': '25px',
    'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
    'border': '1px solid rgba(0,0,0,0.05)',
}

HEADER_STYLE = {
    'color': COLORS['title'],
    'textAlign': 'center',
    'padding': '15px 0',
    'marginBottom': '30px',
    'borderBottom': f'2px solid {COLORS["primary"]}',
    'fontWeight': '600',
    'letterSpacing': '0.5px',
}

TAB_STYLE = {
    'padding': '12px 20px',
    'fontWeight': 'bold',
    'borderBottom': f'1px solid {COLORS["primary"]}',
    'backgroundColor': 'white',
    'borderRadius': '8px 8px 0 0',
    'marginRight': '5px',
    'transition': 'all 0.3s ease',
}

TAB_SELECTED_STYLE = {
    'backgroundColor': COLORS['primary'],
    'color': 'white',
    'padding': '12px 20px',
    'borderRadius': '8px 8px 0 0',
    'boxShadow': '0 -2px 10px rgba(0,0,0,0.1)',
    'border': 'none',
}

# Estilos para KPI cards
KPI_CARD_STYLE = {
    'boxShadow': '0 4px 8px rgba(0,0,0,0.05)',
    'borderRadius': '10px',
    'backgroundColor': 'white',
    'padding': '20px',
    'textAlign': 'center',
    'minHeight': '180px',  # Definindo uma altura mínima para acomodar o texto
    'height': 'auto',      # Permitindo que o card cresça conforme necessário
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'center',
    'border': f'1px solid {COLORS["background"]}',
}

KPI_VALUE_STYLE = {
    'fontSize': '28px',
    'fontWeight': 'bold',
    'color': COLORS['primary'],
    'margin': '10px 0',
}

KPI_LABEL_STYLE = {
    'fontSize': '14px',
    'color': COLORS['text'],
    'marginBottom': '5px',
}

KPI_ICON_STYLE = {
    'fontSize': '24px',
    'marginBottom': '10px',
    'color': COLORS['secondary'],
}

# Connect to the SQLite database
conn = sqlite3.connect('base.sqlite')

# Load the data
df = pd.read_sql("SELECT * FROM Planilha1", conn)

# Close the connection
conn.close()

# Print data info for debugging
print(f"Loaded {len(df)} rows with {len(df.columns)} columns")
print(f"Columns: {df.columns.tolist()}")

# Calcular KPIs
total_respondentes = len(df)
escala_6x1_count = df[df['Escala6x1'] == 'Sim'].shape[0]
escala_6x1_percent = round((escala_6x1_count / total_respondentes) * 100, 1)

# Calcular porcentagem de homens e mulheres
sexo_counts = df['Sexo'].value_counts()
total_sexo = sexo_counts.sum()
homens_count = sexo_counts.get('Masculino', 0)
mulheres_count = sexo_counts.get('Feminino', 0)
homens_percent = round((homens_count / total_sexo) * 100)
mulheres_percent = round((mulheres_count / total_sexo) * 100)

# Calcular resposta mais frequente para impacto na vida familiar
familia_resposta_frequente = df['ImpactoVidaFamiliar'].value_counts().idxmax()
familia_resposta_count = df['ImpactoVidaFamiliar'].value_counts().max()
familia_resposta_percent = round((familia_resposta_count / total_respondentes) * 100)

# Calcular resposta mais frequente para impacto na saúde física
fisica_resposta_frequente = df['ImpactoSaudeFisica'].value_counts().idxmax()
fisica_resposta_count = df['ImpactoSaudeFisica'].value_counts().max()
fisica_resposta_percent = round((fisica_resposta_count / total_respondentes) * 100)

# Calcular resposta mais frequente para impacto na saúde mental
mental_resposta_frequente = df['ImpactoSaudeMental'].value_counts().idxmax()
mental_resposta_count = df['ImpactoSaudeMental'].value_counts().max()
mental_resposta_percent = round((mental_resposta_count / total_respondentes) * 100)

# Define the order of responses for uso futuro
order = [ "Concordo totalmente" , "Concordo",  "Nem concordo nem discordo", "Discordo",  "Discordo totalmente" ]

# Removendo a criação dos gráficos que não são mais necessários
# Quando implementarmos os gráficos, criaremos novos gráficos para cada aba



# Initialize the Dash app
app = dash.Dash(
    __name__,
    title="Dashboard 6x1",
    suppress_callback_exceptions=True,  # Add this to suppress callback exceptions for components not in initial layout
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)



# Removendo a definição do dashboard_tab que não é mais necessária
# Agora estamos usando as novas abas tab1_content, tab2_content e tab3_content

# Removed add_data_tab definition

# Criando conteúdo para as abas
# Aba 1 - Dados Ocupacionais
tab1_content = html.Div([
    html.Div([


        html.H3("Dados Ocupacionais", style={'color': COLORS['title'], 'marginBottom': '20px', 'textAlign': 'center'}),

        # Div para TempoEscala6x1
        html.Div([
            html.Div([
                html.H4("Tempo na Escala 6x1", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='tempo-escala-6x1-container', style={'height': '350px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '20px'}),

        # Div para ContratoTrabalho
        html.Div([
            html.Div([
                html.H4("Tipo de Contrato de Trabalho", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='contrato-trabalho-container', style={'height': '350px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),

        # Div para HorasTrabalho
        html.Div([
            html.Div([
                html.H4("Horas de Trabalho", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='horas-trabalho-container', style={'height': '350px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '20px'}),

        # Div para Occupation
        html.Div([
            html.Div([
                html.H4("Ocupações", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='occupation-container', style={'height': '400px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),

        # Div para CnaeDivision_Respostas
        html.Div([
            html.Div([
                html.H4("CNAE", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='cnae-container', style={'height': '400px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '20px'}),

        # Div para EstadoTrabalho
        html.Div([
            html.Div([
                html.H4("Estado de Trabalho", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='estado-trabalho-container', style={'height': '350px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),

        # Informações sobre os dados
        html.Div([
            html.Div([
                html.H4("Sobre os Dados", style={'color': COLORS['title'], 'marginBottom': '10px'}),
                html.P([
                    f"Total de {total_respondentes} respondentes. ",
                    f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}"
                ], style={'fontSize': '14px', 'color': COLORS['text']}),
            ], style={'padding': '15px'})
        ], style={**CARD_STYLE, 'marginTop': '25px', 'backgroundColor': COLORS['background']}),
    ])
])

# Aba 2 - Dados Pessoais
tab2_content = html.Div([
    html.Div([


        html.H3("Dados Pessoais", style={'color': COLORS['title'], 'marginBottom': '20px', 'textAlign': 'center'}),

        # Div para DataNascimento
        html.Div([
            html.Div([
                html.H4("Idade", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='data-nascimento-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '20px'}),

        # Div para Sexo
        html.Div([
            html.Div([
                html.H4("Sexo", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='sexo-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),

        # Div para CorRaca
        html.Div([
            html.Div([
                html.H4("Cor/Raça", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='cor-raca-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '20px'}),

        # Div para EstadoCivil
        html.Div([
            html.Div([
                html.H4("Estado Civil", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='estado-civil-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),

        # Div para TemFilhos
        html.Div([
            html.Div([
                html.H4("Tem Filhos", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='tem-filhos-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '20px'}),

        # Div para Rendimento
        html.Div([
            html.Div([
                html.H4("Rendimento", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='rendimento-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),

        # Div para Escolaridade
        html.Div([
            html.Div([
                html.H4("Escolaridade", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='escolaridade-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '100%', 'marginBottom': '20px'}),

        # Informações sobre os dados
        html.Div([
            html.Div([
                html.H4("Sobre os Dados", style={'color': COLORS['title'], 'marginBottom': '10px'}),
                html.P([
                    f"Total de {total_respondentes} respondentes. ",
                    f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}"
                ], style={'fontSize': '14px', 'color': COLORS['text']}),
            ], style={'padding': '15px'})
        ], style={**CARD_STYLE, 'marginTop': '25px', 'backgroundColor': COLORS['background']}),
    ])
])

# Aba 3 - Percepção de Impacto
tab3_content = html.Div([
    html.Div([


        html.H3("Percepção de Impacto", style={'color': COLORS['title'], 'marginBottom': '20px', 'textAlign': 'center'}),

        # Div para ImpactoVidaFamiliar
        html.Div([
            html.Div([
                html.H4("Impacto na Vida Familiar", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='impacto-vida-familiar-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '20px'}),

        # Div para ImpactoSaudeFisica
        html.Div([
            html.Div([
                html.H4("Impacto na Saúde Física", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='impacto-saude-fisica-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),

        # Div para ImpactoSaudeMental
        html.Div([
            html.Div([
                html.H4("Impacto na Saúde Mental", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='impacto-saude-mental-container', style={'height': '300px'})
            ], style=CARD_STYLE)
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '20px'}),

        # Div para Impactos
        html.Div([
            html.Div([
                html.H4("Análise de Tópicos nas Respostas", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div(id='impactos-container', style={'height': '500px'})
            ], style=CARD_STYLE)
        ], style={'width': '100%', 'marginBottom': '20px'}),

        # Informações sobre os dados
        html.Div([
            html.Div([
                html.H4("Sobre os Dados", style={'color': COLORS['title'], 'marginBottom': '10px'}),
                html.P([
                    f"Total de {total_respondentes} respondentes. ",
                    f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}"
                ], style={'fontSize': '14px', 'color': COLORS['text']}),
            ], style={'padding': '15px'})
        ], style={**CARD_STYLE, 'marginTop': '25px', 'backgroundColor': COLORS['background']}),
    ])
])

# Define the layout with tabs
app.layout = html.Div(style=GLOBAL_STYLE, children=[
    # Header with logo and title
    html.Div([
        html.Div([
            html.Div([
                html.H1("Dashboard de Análise da Escala 6x1", style=HEADER_STYLE),
                html.P("Análise dos impactos na vida dos trabalhadores",
                       style={'textAlign': 'center', 'marginBottom': '5px', 'fontSize': '18px', 'color': COLORS['text']}),
                html.P(f"Total de {total_respondentes} respondentes • Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y')}",
                       style={'textAlign': 'center', 'fontSize': '14px', 'color': COLORS['text'], 'opacity': '0.7'}),
            ], style={'width': '100%', 'textAlign': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '20px'})
    ], style={'padding': '20px 0', 'backgroundColor': 'white', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
             'marginBottom': '30px', 'borderRadius': '0 0 10px 10px'}),

    # Botão de atualização
    html.Div([
        html.Button(
            '↻ Atualizar Dashboard',
            id='refresh-button',
            n_clicks=0,
            style={
                'backgroundColor': COLORS['success'],
                'color': 'white',
                'border': 'none',
                'padding': '10px 20px',
                'borderRadius': '5px',
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': 'bold',
                'marginBottom': '20px',
                'float': 'right',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'transition': 'all 0.3s ease',
            }
        ),
        html.Div(style={'clear': 'both'})
    ]),

    # KPI Cards Row
    html.Div([
        # KPI 1 - Trabalhadores na escala 6x1
        html.Div([
            html.Div([
                html.Div("👥", style=KPI_ICON_STYLE),
                html.Div("Trabalhadores na Escala 6x1", style=KPI_LABEL_STYLE),
                html.Div(f"{escala_6x1_percent}%", style=KPI_VALUE_STYLE),
                html.Div(f"{escala_6x1_count} de {total_respondentes} respondentes",
                         style={'fontSize': '12px', 'color': COLORS['text'], 'opacity': '0.7'})
            ], style=KPI_CARD_STYLE)
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),

        # KPI 2 - Distribuição por sexo
        html.Div([
            html.Div([
                html.Div("👫", style=KPI_ICON_STYLE),
                html.Div("Distribuição por Sexo", style=KPI_LABEL_STYLE),
                html.Div([
                    html.Span(f"H: {homens_percent}%", style={'marginRight': '10px'}),
                    html.Span(f"M: {mulheres_percent}%")
                ], style=KPI_VALUE_STYLE),
                html.Div(f"{homens_count} homens, {mulheres_count} mulheres",
                         style={'fontSize': '12px', 'color': COLORS['text'], 'opacity': '0.7', 'whiteSpace': 'nowrap'})
            ], style={**KPI_CARD_STYLE, 'whiteSpace': 'nowrap'})
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),

        # KPI 3 - Impacto na vida familiar
        html.Div([
            html.Div([
                html.Div("👪", style=KPI_ICON_STYLE),
                html.Div("Impacto na Vida Familiar", style=KPI_LABEL_STYLE),
                html.Div(f"{familia_resposta_percent}%", style=KPI_VALUE_STYLE),
                html.Div(f"Resposta mais frequente: {familia_resposta_frequente}",
                         style={'fontSize': '12px', 'color': COLORS['text'], 'opacity': '0.7',
                                'wordWrap': 'break-word', 'width': '100%'})
            ], style=KPI_CARD_STYLE)
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),

        # KPI 4 - Impacto na saúde física
        html.Div([
            html.Div([
                html.Div("💪", style=KPI_ICON_STYLE),
                html.Div("Impacto na Saúde Física", style=KPI_LABEL_STYLE),
                html.Div(f"{fisica_resposta_percent}%", style=KPI_VALUE_STYLE),
                html.Div(f"Resposta mais frequente: {fisica_resposta_frequente}",
                         style={'fontSize': '12px', 'color': COLORS['text'], 'opacity': '0.7',
                                'wordWrap': 'break-word', 'width': '100%'})
            ], style=KPI_CARD_STYLE)
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),

        # KPI 5 - Impacto na saúde mental
        html.Div([
            html.Div([
                html.Div("🧠", style=KPI_ICON_STYLE),
                html.Div("Impacto na Saúde Mental", style=KPI_LABEL_STYLE),
                html.Div(f"{mental_resposta_percent}%", style=KPI_VALUE_STYLE),
                html.Div(f"Resposta mais frequente: {mental_resposta_frequente}",
                         style={'fontSize': '12px', 'color': COLORS['text'], 'opacity': '0.7',
                                'wordWrap': 'break-word', 'width': '100%'})
            ], style=KPI_CARD_STYLE)
        ], style={'width': '19%', 'display': 'inline-block'}),
    ], style={'marginBottom': '25px'}),

    # Tabs para as diferentes seções de dados
    html.Div([
        dcc.Tabs(id='tabs-dashboard', value='tab-1', children=[
            dcc.Tab(label='Dados Ocupacionais', value='tab-1', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label='Dados Pessoais', value='tab-2', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label='Percepção de Impacto', value='tab-3', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
        ]),
        html.Div(id='tabs-content')
    ], style={'marginTop': '20px'}),

    # Footer
    html.Div([
        html.Hr(style={'margin': '30px 0 20px 0', 'opacity': '0.2'}),
        html.Div([
            html.P("Dashboard de Análise da Escala 6x1 © 2023",
                  style={'textAlign': 'center', 'color': COLORS['text'], 'fontSize': '14px'}),
            html.P("Desenvolvido com Dash e Plotly",
                  style={'textAlign': 'center', 'color': COLORS['text'], 'fontSize': '12px', 'opacity': '0.7'}),
        ])
    ], style={'marginTop': '30px', 'paddingBottom': '20px'})
])

# Removed tab content callback

# Callback para alternar entre as abas
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs-dashboard', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return tab1_content
    elif tab == 'tab-2':
        return tab2_content
    elif tab == 'tab-3':
        return tab3_content
    return html.Div([html.H3("Conteúdo não encontrado")])

# Função para criar os gráficos da aba Dados Ocupacionais
def create_ocupacionais_graphs(df):
    graphs = {}

    # Gráfico 1: Tempo na Escala 6x1 - Barras verticais ordenadas
    # Definir a ordem correta para TempoEscala6x1
    tempo_order = [
        'menos de um ano',
        'entre um e dois anos',
        'entre dois e três anos',
        'entre três e quatro anos',
        'entre quatro e cinco anos',
        'mais de cinco anos'
    ]

    tempo_counts = df['TempoEscala6x1'].value_counts().reset_index()
    tempo_counts.columns = ['tempo', 'contagem']
    tempo_counts['tempo'] = pd.Categorical(tempo_counts['tempo'], categories=tempo_order, ordered=True)
    tempo_counts = tempo_counts.sort_values('tempo')

    tempo_fig = px.bar(
        tempo_counts,
        x='tempo',
        y='contagem',
        title="Tempo na Escala 6x1",
        color_discrete_sequence=[COLORS['chart1']],
        text='contagem',
        labels={'tempo': 'Tempo', 'contagem': 'Quantidade'},
        height=300,
    )
    tempo_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Tempo",
        yaxis_title="Quantidade",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=50),
        xaxis=dict(tickangle=45),  # Rotacionar os rótulos para melhor visualização
    )
    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = tempo_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in tempo_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    tempo_fig.update_traces(
        marker_color=COLORS['chart1'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{y}',
        textposition=text_positions,  # Lista de posições específicas
        textfont=dict(color=text_colors),  # Lista de cores específicas
    )
    graphs['tempo_escala_6x1'] = tempo_fig

    # Gráfico 2: Tipo de Contrato de Trabalho - Barras horizontais
    contrato_counts = df['ContratoTrabalho'].value_counts().reset_index()
    contrato_counts.columns = ['contrato', 'contagem']
    contrato_counts = contrato_counts.sort_values('contagem', ascending=True)  # Ascendente para barras horizontais

    contrato_fig = px.bar(
        contrato_counts,
        y='contrato',
        x='contagem',
        title="Tipo de Contrato de Trabalho",
        color_discrete_sequence=[COLORS['chart2']],
        orientation='h',  # Horizontal
        text='contagem',
        labels={'contrato': 'Tipo de Contrato', 'contagem': 'Quantidade'},
        height=300,
    )
    contrato_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
    )
    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = contrato_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in contrato_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    contrato_fig.update_traces(
        marker_color=COLORS['chart2'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,  # Lista de posições específicas
        textfont=dict(color=text_colors),  # Lista de cores específicas
    )
    graphs['contrato_trabalho'] = contrato_fig

    # Gráfico 3: Horas de Trabalho - Barras verticais ordenadas
    # Definir a ordem correta para HorasTrabalho
    horas_order = [
        'Menos de 6 horas',
        '6 horas até menos de 7 horas',
        '7 horas até menos de 8 horas',
        '8 horas até menos de 9 horas',
        '9 horas até menos de 10 horas',
        '10 horas ou mais'
    ]

    horas_counts = df['HorasTrabalho'].value_counts().reset_index()
    horas_counts.columns = ['horas', 'contagem']
    horas_counts['horas'] = pd.Categorical(horas_counts['horas'], categories=horas_order, ordered=True)
    horas_counts = horas_counts.sort_values('horas')

    horas_fig = px.bar(
        horas_counts,
        x='horas',
        y='contagem',
        title="Horas de Trabalho",
        color_discrete_sequence=[COLORS['chart3']],
        text='contagem',
        labels={'horas': 'Horas', 'contagem': 'Quantidade'},
        height=300,
    )
    horas_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Horas",
        yaxis_title="Quantidade",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(tickangle=45),  # Rotacionar os rótulos para melhor visualização
    )
    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = horas_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in horas_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    horas_fig.update_traces(
        marker_color=COLORS['chart3'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{y}',
        textposition=text_positions,  # Lista de posições específicas
        textfont=dict(color=text_colors),  # Lista de cores específicas
    )
    graphs['horas_trabalho'] = horas_fig

    # Gráfico 4: Ocupações - Top 10 com barra de rolagem
    occupation_counts = df['Occupation_Respostas'].value_counts().reset_index()
    occupation_counts.columns = ['ocupacao', 'contagem']
    # Armazenar todos os dados para a barra de rolagem
    occupation_all = occupation_counts.sort_values('contagem', ascending=False).copy()
    # Pegar os top 10 para o gráfico inicial
    occupation_counts = occupation_counts.sort_values('contagem', ascending=False).head(10)

    # Ordenar por contagem para barras horizontais (ascendente)
    occupation_counts = occupation_counts.sort_values('contagem', ascending=True)

    occupation_fig = px.bar(
        occupation_counts,
        y='ocupacao',
        x='contagem',
        title="Top 10 Ocupações",
        color_discrete_sequence=[COLORS['chart4']],
        orientation='h',  # Horizontal
        text='contagem',
        labels={'ocupacao': 'Ocupação', 'contagem': 'Quantidade'},
        height=350,
    )
    occupation_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        # Truncar textos longos
        yaxis=dict(
            tickmode='array',
            tickvals=occupation_counts['ocupacao'],
            ticktext=[f"{x[:30]}..." if len(x) > 30 else x for x in occupation_counts['ocupacao']]
        ),
        height=400  # Aumentar a altura para acomodar mais itens
    )
    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = occupation_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in occupation_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    occupation_fig.update_traces(
        marker_color=COLORS['chart4'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,  # Lista de posições específicas
        textfont=dict(color=text_colors),  # Lista de cores específicas
    )
    graphs['occupation'] = occupation_fig

    # Gráfico 5: CNAE - Top 10 com barra de rolagem e barras horizontais
    cnae_counts = df['CnaeDivision_Respostas'].value_counts().reset_index()
    cnae_counts.columns = ['cnae', 'contagem']
    # Armazenar todos os dados para a barra de rolagem
    cnae_all = cnae_counts.sort_values('contagem', ascending=False).copy()
    # Pegar os top 10 para o gráfico inicial
    cnae_counts = cnae_counts.sort_values('contagem', ascending=True).tail(10)  # Pegando os 10 maiores em ordem ascendente

    cnae_fig = px.bar(
        cnae_counts,
        y='cnae',
        x='contagem',
        title="Top 10 CNAEs",
        color_discrete_sequence=[COLORS['chart1']],
        orientation='h',  # Horizontal
        text='contagem',
        labels={'cnae': 'CNAE', 'contagem': 'Quantidade'},
        height=300,
    )
    cnae_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        # Truncar textos longos
        yaxis=dict(
            tickmode='array',
            tickvals=cnae_counts['cnae'],
            ticktext=[f"{x[:30]}..." if len(x) > 30 else x for x in cnae_counts['cnae']]
        ),
        height=400  # Aumentar a altura para acomodar mais itens
    )
    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = cnae_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in cnae_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    cnae_fig.update_traces(
        marker_color=COLORS['chart1'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,  # Lista de posições específicas
        textfont=dict(color=text_colors),  # Lista de cores específicas
    )
    graphs['cnae'] = cnae_fig

    # Gráfico 6: Estado de Trabalho - Top 10 com barra de rolagem
    estado_counts = df['EstadoTrabalho'].value_counts().reset_index()
    estado_counts.columns = ['estado', 'contagem']
    # Armazenar todos os dados para a barra de rolagem
    estado_all = estado_counts.sort_values('contagem', ascending=False).copy()
    # Pegar os top 10 para o gráfico inicial
    estado_counts = estado_counts.sort_values('contagem', ascending=False).head(10)

    estado_fig = px.bar(
        estado_counts,
        x='estado',
        y='contagem',
        title="Top 10 Estados",
        color_discrete_sequence=[COLORS['chart2']],
        text='contagem',
        labels={'estado': 'Estado', 'contagem': 'Quantidade'},
        height=300,
    )
    estado_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Estado",
        yaxis_title="Quantidade",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
    )
    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = estado_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in estado_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    estado_fig.update_traces(
        marker_color=COLORS['chart2'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{y}',
        textposition=text_positions,  # Lista de posições específicas
        textfont=dict(color=text_colors),  # Lista de cores específicas
    )
    graphs['estado_trabalho'] = estado_fig

    return graphs

# Função para criar os gráficos da aba Dados Pessoais
def create_pessoais_graphs(df):
    graphs = {}

    # Gráfico 1: Sexo - Gráfico de Pizza
    sexo_counts = df['Sexo'].value_counts().reset_index()
    sexo_counts.columns = ['sexo', 'contagem']

    sexo_fig = px.pie(
        sexo_counts,
        values='contagem',
        names='sexo',
        title="Distribuição por Sexo",
        color_discrete_sequence=[COLORS['chart1'], COLORS['chart2'], COLORS['chart3']],
    )
    sexo_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.05,
            font=dict(size=12)  # Fonte menor para a legenda
        ),
        height=300,
        width=400,   # Largura aumentada para 400px
    )

    # Calcular percentuais para determinar posição dos rótulos
    total = sexo_counts['contagem'].sum()
    sexo_counts['percentual'] = sexo_counts['contagem'] / total * 100

    # Criar lista para posições dos rótulos
    text_positions = []

    # Determinar posição do texto para cada fatia
    for percentual in sexo_counts['percentual']:
        if percentual < 10:  # Valores pequenos (menos de 5%)
            text_positions.append('outside')
        else:  # Valores maiores
            text_positions.append('inside')

    sexo_fig.update_traces(
        textinfo='percent+label',  # Usar uma única string para todos
        textposition=text_positions,
        insidetextfont=dict(color='white'),
        outsidetextfont=dict(color='black'),
        pull=[0.05 if p < 5 else 0 for p in sexo_counts['percentual']],  # Destacar fatias pequenas
    )
    graphs['sexo'] = sexo_fig

    # Gráfico 2: Idade - Cálculo e agrupamento de 10 em 10 anos
    # Converter a coluna de data de nascimento para datetime
    df['DataNascimento'] = pd.to_datetime(df['DataNascimento'], errors='coerce')

    # Calcular a idade
    hoje = pd.Timestamp.now()
    # Criar uma cópia do dataframe para evitar warnings
    df_idade = df.copy()
    # Calcular a idade apenas para datas válidas
    df_idade['Idade'] = df_idade['DataNascimento'].apply(
        lambda x: int((hoje - x).days / 365.25) if pd.notna(x) else None
    )

    # Criar faixas etárias de 10 em 10 anos até 60 anos
    bins = [0, 20, 30, 40, 50, 60, 150]  # Último bin vai até 150 para capturar todas as idades

    # Criar rótulos para as faixas etárias
    labels = [
        'Até 19 anos',
        'Entre 20 e 29 anos',
        'Entre 30 e 39 anos',
        'Entre 40 e 49 anos',
        'Entre 50 e 59 anos',
        'Acima de 60 anos'
    ]

    # Aplicar o corte apenas para idades válidas (não nulas)
    # Remover linhas com idade nula para evitar erros
    df_idade = df_idade.dropna(subset=['Idade'])
    df_idade['FaixaEtaria'] = pd.cut(df_idade['Idade'], bins=bins, labels=labels, right=False)

    # Contar por faixa etária
    idade_counts = df_idade['FaixaEtaria'].value_counts().reset_index()
    idade_counts.columns = ['faixa', 'contagem']

    # Criar uma coluna para ordenação personalizada
    ordem_faixas = {faixa: i for i, faixa in enumerate(labels)}
    idade_counts['ordem'] = idade_counts['faixa'].map(ordem_faixas)

    # Ordenar em ordem inversa (menores idades primeiro)
    idade_counts = idade_counts.sort_values('ordem', ascending=False)

    idade_fig = px.bar(
        idade_counts,
        x='contagem',
        y='faixa',
        title="Distribuição por Faixa Etária",
        color_discrete_sequence=[COLORS['chart2']],
        orientation='h',
        text='contagem',
        labels={'faixa': 'Faixa Etária', 'contagem': 'Quantidade'},
        height=350,
    )
    idade_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
    )

    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = idade_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in idade_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    idade_fig.update_traces(
        marker_color=COLORS['chart2'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,
        textfont=dict(color=text_colors),
    )
    graphs['idade'] = idade_fig

    # Gráfico 3: Cor/Raça - Gráfico de Pizza
    cor_raca_counts = df['CorRaca'].value_counts().reset_index()
    cor_raca_counts.columns = ['cor_raca', 'contagem']

    cor_raca_fig = px.pie(
        cor_raca_counts,
        values='contagem',
        names='cor_raca',
        title="Distribuição por Cor/Raça",
        color_discrete_sequence=[COLORS['chart1'], COLORS['chart2'], COLORS['chart3'], COLORS['chart4'], COLORS['success']],
    )
    cor_raca_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.05,
            font=dict(size=12)  # Fonte menor para a legenda
        ),
        height=300,
        width=400,   # Largura aumentada para 400px
    )

    # Calcular percentuais para determinar posição dos rótulos
    total = cor_raca_counts['contagem'].sum()
    cor_raca_counts['percentual'] = cor_raca_counts['contagem'] / total * 100

    # Criar lista para posições dos rótulos
    text_positions = []

    # Determinar posição do texto para cada fatia
    for percentual in cor_raca_counts['percentual']:
        if percentual < 10:  # Valores pequenos (menos de 5%)
            text_positions.append('outside')
        else:  # Valores maiores
            text_positions.append('inside')

    cor_raca_fig.update_traces(
        textinfo='percent+label',  # Usar uma única string para todos
        textposition=text_positions,
        insidetextfont=dict(color='white'),
        outsidetextfont=dict(color='black'),
        pull=[0.05 if p < 5 else 0 for p in cor_raca_counts['percentual']],  # Destacar fatias pequenas
    )
    graphs['cor_raca'] = cor_raca_fig

    # Gráfico 4: Escolaridade - Gráfico de barras horizontais ordenadas
    # Definir a ordem de escolaridade com base nos valores reais do banco de dados
    escolaridade_order = [
        'Ensino Fundamental Incompleto',
        'Ensino Fundamental Completo',
        'Ensino Médio Incompleto',
        'Ensino Médio Completo',
        'Ensino Superior Incompleto',
        'Ensino Superior Completo',
        'Pós-Graduação Incompleto',
        'Pós-Graduação'  # Mantido para compatibilidade com dados existentes
    ]

    escolaridade_counts = df['Escolaridade'].value_counts().reset_index()
    escolaridade_counts.columns = ['escolaridade', 'contagem']

    # Criar uma coluna para ordenação
    escolaridade_counts['ordem'] = escolaridade_counts['escolaridade'].apply(
        lambda x: escolaridade_order.index(x) if x in escolaridade_order else 999
    )
    # Ordenar em ordem inversa (menor escolaridade no topo)
    escolaridade_counts = escolaridade_counts.sort_values('ordem', ascending=False)

    escolaridade_fig = px.bar(
        escolaridade_counts,
        y='escolaridade',
        x='contagem',
        title="Distribuição por Escolaridade",
        color_discrete_sequence=[COLORS['chart3']],
        orientation='h',
        text='contagem',
        labels={'escolaridade': 'Escolaridade', 'contagem': 'Quantidade'},
        height=350,
    )
    escolaridade_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
    )

    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = escolaridade_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in escolaridade_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    escolaridade_fig.update_traces(
        marker_color=COLORS['chart3'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,
        textfont=dict(color=text_colors),
    )
    graphs['escolaridade'] = escolaridade_fig

    # Gráfico 5: Rendimento - Gráfico de barras horizontais ordenadas
    # Definir a ordem de rendimento com base nos valores reais do banco de dados
    rendimento_order = [
        '1,00 A 500,00',
        '501,00 A 1.000,00',
        '1.001,00 A 2.000,00',
        '2.001,00 A 3.000,00',
        '3.001,00 A 5.000,00',
        '5.001,00 A 10.000,00',
        '10.001,00 OU MAIS'
    ]

    rendimento_counts = df['Rendimento'].value_counts().reset_index()
    rendimento_counts.columns = ['rendimento', 'contagem']

    # Criar uma coluna para ordenação
    rendimento_counts['ordem'] = rendimento_counts['rendimento'].apply(
        lambda x: rendimento_order.index(x) if x in rendimento_order else 999
    )
    # Ordenar em ordem inversa (menores rendimentos primeiro)
    rendimento_counts = rendimento_counts.sort_values('ordem', ascending=False)

    rendimento_fig = px.bar(
        rendimento_counts,
        y='rendimento',
        x='contagem',
        title="Distribuição por Rendimento",
        color_discrete_sequence=[COLORS['chart4']],
        orientation='h',
        text='contagem',
        labels={'rendimento': 'Rendimento', 'contagem': 'Quantidade'},
        height=350,
    )
    rendimento_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
    )

    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = rendimento_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in rendimento_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    rendimento_fig.update_traces(
        marker_color=COLORS['chart4'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,
        textfont=dict(color=text_colors),
    )
    graphs['rendimento'] = rendimento_fig

    # Gráfico 6: Estado Civil - Gráfico de pizza
    estado_civil_counts = df['EstadoCivil'].value_counts().reset_index()
    estado_civil_counts.columns = ['estado_civil', 'contagem']

    estado_civil_fig = px.pie(
        estado_civil_counts,
        values='contagem',
        names='estado_civil',
        title="Distribuição por Estado Civil",
        color_discrete_sequence=[COLORS['chart1'], COLORS['chart2'], COLORS['chart3'], COLORS['chart4']],
    )
    estado_civil_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            font=dict(size=9)
        ),
        height=300,
        width=430,  # Largura aumentada para 400px
    )

    # Calcular percentuais para determinar posição dos rótulos
    total = estado_civil_counts['contagem'].sum()
    estado_civil_counts['percentual'] = estado_civil_counts['contagem'] / total * 100

    # Criar lista para posições dos rótulos
    text_positions = []

    # Determinar posição do texto para cada fatia
    for percentual in estado_civil_counts['percentual']:
        if percentual < 10:  # Valores pequenos (menos de 5%)
            text_positions.append('outside')
        else:  # Valores maiores
            text_positions.append('inside')

    estado_civil_fig.update_traces(
        textinfo='percent+label',  # Usar uma única string para todos
        textposition=text_positions,
        insidetextfont=dict(color='white'),
        outsidetextfont=dict(color='black'),
        pull=[0.05 if p < 5 else 0 for p in estado_civil_counts['percentual']],  # Destacar fatias pequenas
    )
    graphs['estado_civil'] = estado_civil_fig

    # Gráfico 7: Tem Filhos - Gráfico de pizza
    tem_filhos_counts = df['TemFilhos'].value_counts().reset_index()
    tem_filhos_counts.columns = ['tem_filhos', 'contagem']

    tem_filhos_fig = px.pie(
        tem_filhos_counts,
        values='contagem',
        names='tem_filhos',
        title="Distribuição por Tem Filhos",
        color_discrete_sequence=[COLORS['chart2'], COLORS['chart3']],
    )
    tem_filhos_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.05,
            font=dict(size=10)  # Fonte menor para a legenda
        ),
        height=300,
        width=400,   # Largura aumentada para 400px
    )

    # Calcular percentuais para determinar posição dos rótulos
    total = tem_filhos_counts['contagem'].sum()
    tem_filhos_counts['percentual'] = tem_filhos_counts['contagem'] / total * 100

    # Criar lista para posições dos rótulos
    text_positions = []

    # Determinar posição do texto para cada fatia
    for percentual in tem_filhos_counts['percentual']:
        if percentual < 10:  # Valores pequenos (menos de 5%)
            text_positions.append('outside')
        else:  # Valores maiores
            text_positions.append('inside')

    tem_filhos_fig.update_traces(
        textinfo='percent+label',  # Usar uma única string para todos
        textposition=text_positions,
        insidetextfont=dict(color='white'),
        outsidetextfont=dict(color='black'),
        pull=[0.05 if p < 5 else 0 for p in tem_filhos_counts['percentual']],  # Destacar fatias pequenas
    )
    graphs['tem_filhos'] = tem_filhos_fig

    return graphs

# Callback para atualizar os gráficos da aba Dados Ocupacionais
@app.callback(
    [Output('tempo-escala-6x1-container', 'children'),
     Output('contrato-trabalho-container', 'children'),
     Output('horas-trabalho-container', 'children'),
     Output('occupation-container', 'children'),
     Output('cnae-container', 'children'),
     Output('estado-trabalho-container', 'children')],
    [Input('refresh-button', 'n_clicks'),
     Input('tabs-dashboard', 'value')]
)
def update_ocupacionais_graphs(n_clicks, tab):
    # Só atualiza se estiver na aba de Dados Ocupacionais
    if tab != 'tab-1':
        raise PreventUpdate

    # Conectar ao banco de dados
    conn = sqlite3.connect('base.sqlite')

    # Carregar os dados
    updated_df = pd.read_sql("SELECT * FROM Planilha1", conn)

    # Fechar a conexão
    conn.close()

    # Criar os gráficos
    graphs = create_ocupacionais_graphs(updated_df)

    # Retornar os gráficos como componentes Dash
    return [
        dcc.Graph(figure=graphs['tempo_escala_6x1'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['contrato_trabalho'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['horas_trabalho'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['occupation'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['cnae'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['estado_trabalho'], config={'displayModeBar': False})
    ]

# Função para criar os gráficos da aba Percepção de Impacto
def create_impacto_graphs(df):
    graphs = {}

    # Definir a ordem das respostas para os gráficos de impacto na saúde (física e mental)
    # Ordem invertida conforme solicitado
    impacto_saude_order = [
        'Discordo totalmente',
        'Discordo',
        'Nem concordo nem discordo',
        'Concordo',
        'Concordo totalmente'
    ]

    # Gráfico 1: Impacto na Vida Familiar
    impacto_familia_counts = df['ImpactoVidaFamiliar'].value_counts().reset_index()
    impacto_familia_counts.columns = ['resposta', 'contagem']

    # Ordenar por contagem (decrescente) para que os maiores valores apareçam em cima
    # Usando ascending=True porque no gráfico horizontal, a primeira linha é a de baixo
    impacto_familia_counts = impacto_familia_counts.sort_values('contagem', ascending=True)

    impacto_familia_fig = px.bar(
        impacto_familia_counts,
        y='resposta',
        x='contagem',
        title="Impacto na Vida Familiar",
        color_discrete_sequence=[COLORS['chart1']],
        orientation='h',
        text='contagem',
        labels={'resposta': 'Resposta', 'contagem': 'Quantidade'},
        height=300,
    )
    impacto_familia_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Quantidade",
        yaxis_title="",
    )

    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = impacto_familia_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in impacto_familia_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    impacto_familia_fig.update_traces(
        marker_color=COLORS['chart1'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,
        textfont=dict(color=text_colors),
    )
    graphs['impacto_familia'] = impacto_familia_fig

    # Gráfico 2: Impacto na Saúde Física
    impacto_fisica_counts = df['ImpactoSaudeFisica'].value_counts().reset_index()
    impacto_fisica_counts.columns = ['resposta', 'contagem']

    # Criar uma coluna para ordenação com a nova ordem solicitada
    impacto_fisica_counts['ordem'] = impacto_fisica_counts['resposta'].apply(
        lambda x: impacto_saude_order.index(x) if x in impacto_saude_order else 999
    )
    impacto_fisica_counts = impacto_fisica_counts.sort_values('ordem')

    impacto_fisica_fig = px.bar(
        impacto_fisica_counts,
        y='resposta',
        x='contagem',
        title="Impacto na Saúde Física",
        color_discrete_sequence=[COLORS['chart2']],
        orientation='h',
        text='contagem',
        labels={'resposta': 'Resposta', 'contagem': 'Quantidade'},
        height=300,
    )
    impacto_fisica_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Quantidade",
        yaxis_title="",
    )

    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = impacto_fisica_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in impacto_fisica_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    impacto_fisica_fig.update_traces(
        marker_color=COLORS['chart2'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,
        textfont=dict(color=text_colors),
    )
    graphs['impacto_fisica'] = impacto_fisica_fig

    # Gráfico 3: Impacto na Saúde Mental
    impacto_mental_counts = df['ImpactoSaudeMental'].value_counts().reset_index()
    impacto_mental_counts.columns = ['resposta', 'contagem']

    # Criar uma coluna para ordenação com a nova ordem solicitada
    impacto_mental_counts['ordem'] = impacto_mental_counts['resposta'].apply(
        lambda x: impacto_saude_order.index(x) if x in impacto_saude_order else 999
    )
    impacto_mental_counts = impacto_mental_counts.sort_values('ordem')

    impacto_mental_fig = px.bar(
        impacto_mental_counts,
        y='resposta',
        x='contagem',
        title="Impacto na Saúde Mental",
        color_discrete_sequence=[COLORS['chart3']],
        orientation='h',
        text='contagem',
        labels={'resposta': 'Resposta', 'contagem': 'Quantidade'},
        height=300,
    )
    impacto_mental_fig.update_layout(
        title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Quantidade",
        yaxis_title="",
    )

    # Definir limites para posicionamento interno/externo baseado no valor
    max_value = impacto_mental_counts['contagem'].max()
    threshold = max_value * 0.8  # 80% do valor máximo como limite

    # Criar uma lista para armazenar as posições dos textos
    text_positions = []
    text_colors = []

    # Determinar a posição e cor para cada barra
    for value in impacto_mental_counts['contagem']:
        if value > threshold:
            text_positions.append('inside')
            text_colors.append('white')
        else:
            text_positions.append('outside')
            text_colors.append('black')

    impacto_mental_fig.update_traces(
        marker_color=COLORS['chart3'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition=text_positions,
        textfont=dict(color=text_colors),
    )
    graphs['impacto_mental'] = impacto_mental_fig

    return graphs

# Callback para atualizar os gráficos da aba Dados Pessoais
@app.callback(
    [Output('data-nascimento-container', 'children'),
     Output('sexo-container', 'children'),
     Output('cor-raca-container', 'children'),
     Output('estado-civil-container', 'children'),
     Output('tem-filhos-container', 'children'),
     Output('rendimento-container', 'children'),
     Output('escolaridade-container', 'children')],
    [Input('refresh-button', 'n_clicks'),
     Input('tabs-dashboard', 'value')]
)
def update_pessoais_graphs(n_clicks, tab):
    # Só atualiza se estiver na aba de Dados Pessoais
    if tab != 'tab-2':
        raise PreventUpdate

    # Conectar ao banco de dados
    conn = sqlite3.connect('base.sqlite')

    # Carregar os dados
    updated_df = pd.read_sql("SELECT * FROM Planilha1", conn)

    # Fechar a conexão
    conn.close()

    # Criar os gráficos
    graphs = create_pessoais_graphs(updated_df)

    # Retornar os gráficos como componentes Dash
    return [
        dcc.Graph(figure=graphs['idade'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['sexo'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['cor_raca'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['estado_civil'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['tem_filhos'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['rendimento'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['escolaridade'], config={'displayModeBar': False})
    ]

# Callback para atualizar os gráficos da aba Percepção de Impacto
@app.callback(
    [Output('impacto-vida-familiar-container', 'children'),
     Output('impacto-saude-fisica-container', 'children'),
     Output('impacto-saude-mental-container', 'children'),
     Output('impactos-container', 'children')],
    [Input('refresh-button', 'n_clicks'),
     Input('tabs-dashboard', 'value')]
)
def update_impacto_graphs(n_clicks, tab):
    # Só atualiza se estiver na aba de Percepção de Impacto
    if tab != 'tab-3':
        raise PreventUpdate

    # Conectar ao banco de dados
    conn = sqlite3.connect('base.sqlite')

    # Carregar os dados
    updated_df = pd.read_sql("SELECT * FROM Planilha1", conn)

    # Fechar a conexão
    conn.close()

    # Criar os gráficos
    graphs = create_impacto_graphs(updated_df)

    # Obter os dados para o gráfico de análise de PLN
    topics, counts = get_impact_data_for_graph(updated_df)

    # Criar DataFrame para o gráfico
    nlp_df = pd.DataFrame({
        'Tópico': topics,
        'Contagem': counts
    })

    # Ordenar o DataFrame para que os maiores valores apareçam no topo
    # Para gráficos de barras horizontais, a primeira linha (índice 0) aparece na parte inferior
    # Então, para ter os maiores valores no topo, ordenamos em ordem decrescente
    nlp_df = nlp_df.sort_values('Contagem', ascending=False)

    # Criar o gráfico de barras horizontais
    if len(nlp_df) > 0:
        nlp_fig = px.bar(
            nlp_df,
            y='Tópico',
            x='Contagem',
            title="Análise de Tópicos nas Respostas",
            color_discrete_sequence=[COLORS['success']],  # Verde
            orientation='h',
            text='Contagem',
            labels={'Tópico': 'Tópico Identificado', 'Contagem': 'Número de Ocorrências'},
            height=450,
        )

        # Configurar o layout
        nlp_fig.update_layout(
            title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
            font=dict(family="Segoe UI"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis_title="Número de Ocorrências",
            yaxis_title="",
        )

        # Definir limites para posicionamento interno/externo baseado no valor
        max_value = nlp_df['Contagem'].max() if len(nlp_df) > 0 else 0
        threshold = max_value * 0.8  # 80% do valor máximo como limite

        # Criar uma lista para armazenar as posições dos textos
        text_positions = []
        text_colors = []

        # Determinar a posição e cor para cada barra
        for value in nlp_df['Contagem']:
            if value > threshold:
                text_positions.append('inside')
                text_colors.append('white')
            else:
                text_positions.append('outside')
                text_colors.append('black')

        # Atualizar as barras
        nlp_fig.update_traces(
            marker_color=COLORS['success'],
            marker_line_color='rgba(0,0,0,0)',
            opacity=0.8,
            texttemplate='%{x}',
            textposition=text_positions,
            textfont=dict(color=text_colors),
        )
    else:
        # Se não houver dados, criar um gráfico vazio
        nlp_fig = px.bar(x=[0], y=[0], title="Análise de Tópicos nas Respostas")
        nlp_fig.update_layout(
            title_font=dict(size=16, family="Segoe UI", color=COLORS['title']),
            font=dict(family="Segoe UI"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text="Sem dados disponíveis",
                showarrow=False,
                font=dict(size=16, color=COLORS['text']),
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )

    # Retornar os gráficos como componentes Dash
    return [
        dcc.Graph(figure=graphs['impacto_familia'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['impacto_fisica'], config={'displayModeBar': False}),
        dcc.Graph(figure=graphs['impacto_mental'], config={'displayModeBar': False}),
        dcc.Graph(figure=nlp_fig, config={'displayModeBar': False})
    ]

# Run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
