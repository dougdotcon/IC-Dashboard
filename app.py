import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import sqlite3
from dash.exceptions import PreventUpdate

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
    'height': '100%',
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

# Calcular tempo médio na escala 6x1
tempo_mapping = {
    'Menos de 1 ano': 0.5,
    '1-2 anos': 1.5,
    '3-5 anos': 4,
    'Mais de 5 anos': 6
}

# Tentar converter os valores de tempo para numéricos
try:
    df['TempoNumerico'] = df['TempoEscala6x1'].map(tempo_mapping)
    tempo_medio = round(df['TempoNumerico'].mean(), 1)
except:
    tempo_medio = "N/A"

# Calcular percentuais de impacto
impacto_familia_positivo = df[df['ImpactoVidaFamiliar'].isin(['Concordo', 'Concordo totalmente'])].shape[0]
impacto_familia_percent = round((impacto_familia_positivo / total_respondentes) * 100, 1)

impacto_saude_fisica = df[df['ImpactoSaudeFisica'].isin(['Concordo', 'Concordo totalmente'])].shape[0]
impacto_saude_fisica_percent = round((impacto_saude_fisica / total_respondentes) * 100, 1)

impacto_saude_mental = df[df['ImpactoSaudeMental'].isin(['Concordo', 'Concordo totalmente'])].shape[0]
impacto_saude_mental_percent = round((impacto_saude_mental / total_respondentes) * 100, 1)

# Define the order of responses
order = ["Discordo totalmente", "Discordo", "Neutro", "Concordo", "Concordo totalmente"]

# Create figures with improved styling
# 1. Impacto na Vida Familiar - Gráfico de barras horizontais
familia_counts = df['ImpactoVidaFamiliar'].value_counts().reset_index()
familia_counts.columns = ['resposta', 'contagem']
familia_counts['resposta'] = pd.Categorical(familia_counts['resposta'], categories=order, ordered=True)
familia_counts = familia_counts.sort_values('resposta')

familia_bar = px.bar(
    familia_counts,
    y='resposta',  # Agora no eixo y para barras horizontais
    x='contagem',  # Agora no eixo x
    title="Impacto na Vida Familiar",
    color_discrete_sequence=[COLORS['chart1']],
    orientation='h',  # Horizontal
    text='contagem',  # Mostrar valores nas barras
    labels={'resposta': '', 'contagem': 'Quantidade de Respostas'},
    height=350,
)
familia_bar.update_layout(
    title_font=dict(size=18, family="Segoe UI", color=COLORS['title']),
    font=dict(family="Segoe UI"),
    xaxis_title="Quantidade",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=40, b=10),
    yaxis=dict(autorange="reversed"),  # Inverte a ordem para ter "Concordo totalmente" no topo
)
familia_bar.update_traces(
    marker_color=COLORS['chart1'],
    marker_line_color='rgba(0,0,0,0)',
    opacity=0.8,
    texttemplate='%{x}',
    textposition='outside',
)

# 2. Impacto na Saúde Física - Gráfico de barras horizontais
fisica_counts = df['ImpactoSaudeFisica'].value_counts().reset_index()
fisica_counts.columns = ['resposta', 'contagem']
fisica_counts['resposta'] = pd.Categorical(fisica_counts['resposta'], categories=order, ordered=True)
fisica_counts = fisica_counts.sort_values('resposta')

fisica_bar = px.bar(
    fisica_counts,
    y='resposta',
    x='contagem',
    title="Impacto na Saúde Física",
    color_discrete_sequence=[COLORS['chart3']],
    orientation='h',
    text='contagem',
    labels={'resposta': '', 'contagem': 'Quantidade de Respostas'},
    height=350,
)
fisica_bar.update_layout(
    title_font=dict(size=18, family="Segoe UI", color=COLORS['title']),
    font=dict(family="Segoe UI"),
    xaxis_title="Quantidade",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=40, b=10),
    yaxis=dict(autorange="reversed"),
)
fisica_bar.update_traces(
    marker_color=COLORS['chart3'],
    marker_line_color='rgba(0,0,0,0)',
    opacity=0.8,
    texttemplate='%{x}',
    textposition='outside',
)

# 3. Impacto na Saúde Mental - Gráfico de barras horizontais
mental_counts = df['ImpactoSaudeMental'].value_counts().reset_index()
mental_counts.columns = ['resposta', 'contagem']
mental_counts['resposta'] = pd.Categorical(mental_counts['resposta'], categories=order, ordered=True)
mental_counts = mental_counts.sort_values('resposta')

mental_bar = px.bar(
    mental_counts,
    y='resposta',
    x='contagem',
    title="Impacto na Saúde Mental",
    color_discrete_sequence=[COLORS['chart2']],
    orientation='h',
    text='contagem',
    labels={'resposta': '', 'contagem': 'Quantidade de Respostas'},
    height=350,
)
mental_bar.update_layout(
    title_font=dict(size=18, family="Segoe UI", color=COLORS['title']),
    font=dict(family="Segoe UI"),
    xaxis_title="Quantidade",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=40, b=10),
    yaxis=dict(autorange="reversed"),
)
mental_bar.update_traces(
    marker_color=COLORS['chart2'],
    marker_line_color='rgba(0,0,0,0)',
    opacity=0.8,
    texttemplate='%{x}',
    textposition='outside',
)

# 4. Distribuição por Estado - Gráfico de barras
estado_counts = df['EstadoTrabalho'].value_counts().reset_index()
estado_counts.columns = ['estado', 'contagem']
estado_counts = estado_counts.sort_values('contagem', ascending=False).head(10)  # Top 10 estados

estado_bar = px.bar(
    estado_counts,
    x='estado',
    y='contagem',
    title="Top Estados",
    color_discrete_sequence=[COLORS['chart4']],
    text='contagem',
    labels={'estado': 'Estado', 'contagem': 'Quantidade'},
    height=350,
)
estado_bar.update_layout(
    title_font=dict(size=18, family="Segoe UI", color=COLORS['title']),
    font=dict(family="Segoe UI"),
    xaxis_title="Estado",
    yaxis_title="Quantidade",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=40, b=10),
)
estado_bar.update_traces(
    marker_color=COLORS['chart4'],
    marker_line_color='rgba(0,0,0,0)',
    opacity=0.8,
    texttemplate='%{y}',
    textposition='outside',
)

# Initialize the Dash app
app = dash.Dash(
    __name__,
    title="Dashboard 6x1",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Create the dashboard tab content
dashboard_tab = html.Div([
    # Refresh button
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
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),

        # KPI 2 - Tempo médio na escala
        html.Div([
            html.Div([
                html.Div("⏱️", style=KPI_ICON_STYLE),
                html.Div("Tempo Médio na Escala", style=KPI_LABEL_STYLE),
                html.Div(f"{tempo_medio} anos", style=KPI_VALUE_STYLE),
                html.Div("Média entre respondentes",
                         style={'fontSize': '12px', 'color': COLORS['text'], 'opacity': '0.7'})
            ], style=KPI_CARD_STYLE)
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),

        # KPI 3 - Impacto na vida familiar
        html.Div([
            html.Div([
                html.Div("👪", style=KPI_ICON_STYLE),
                html.Div("Impacto na Vida Familiar", style=KPI_LABEL_STYLE),
                html.Div(f"{impacto_familia_percent}%", style=KPI_VALUE_STYLE),
                html.Div("Concordam com impacto negativo",
                         style={'fontSize': '12px', 'color': COLORS['text'], 'opacity': '0.7'})
            ], style=KPI_CARD_STYLE)
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),

        # KPI 4 - Impacto na saúde
        html.Div([
            html.Div([
                html.Div("🩺", style=KPI_ICON_STYLE),
                html.Div("Impacto na Saúde", style=KPI_LABEL_STYLE),
                html.Div(f"{impacto_saude_mental_percent}%", style=KPI_VALUE_STYLE),
                html.Div("Relatam impacto na saúde mental",
                         style={'fontSize': '12px', 'color': COLORS['text'], 'opacity': '0.7'})
            ], style=KPI_CARD_STYLE)
        ], style={'width': '24%', 'display': 'inline-block'}),
    ], style={'marginBottom': '25px'}),

    # First row - Impact charts
    html.Div([
        html.Div([
            html.Div([
                html.H3("Impacto na Vida Familiar", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div("👪", style={'position': 'absolute', 'right': '25px', 'top': '25px', 'fontSize': '24px'}),
                dcc.Graph(id='familia-bar-chart', figure=familia_bar, config={'displayModeBar': False}),
            ], style={**CARD_STYLE, 'position': 'relative'}),
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            html.Div([
                html.H3("Impacto na Saúde Física", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div("💪", style={'position': 'absolute', 'right': '25px', 'top': '25px', 'fontSize': '24px'}),
                dcc.Graph(id='fisica-bar-chart', figure=fisica_bar, config={'displayModeBar': False}),
            ], style={**CARD_STYLE, 'position': 'relative'}),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    # Second row - Mental health and states
    html.Div([
        html.Div([
            html.Div([
                html.H3("Impacto na Saúde Mental", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div("🧠", style={'position': 'absolute', 'right': '25px', 'top': '25px', 'fontSize': '24px'}),
                dcc.Graph(id='mental-bar-chart', figure=mental_bar, config={'displayModeBar': False}),
            ], style={**CARD_STYLE, 'position': 'relative'}),
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            html.Div([
                html.H3("Distribuição por Estado", style={'color': COLORS['title'], 'marginBottom': '15px'}),
                html.Div("🗺️", style={'position': 'absolute', 'right': '25px', 'top': '25px', 'fontSize': '24px'}),
                dcc.Graph(id='estado-bar-chart', figure=estado_bar, config={'displayModeBar': False}),
            ], style={**CARD_STYLE, 'position': 'relative'}),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    # Data info
    html.Div([
        html.Div([
            html.Div([
                html.H4("Sobre os Dados", style={'color': COLORS['title'], 'marginBottom': '10px'}),
                html.P([
                    f"Total de {total_respondentes} respondentes. ",
                    f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}"
                ], style={'fontSize': '14px', 'color': COLORS['text']}),
            ], style={'padding': '15px'})
        ], style={**CARD_STYLE, 'marginTop': '25px', 'backgroundColor': COLORS['background']})
    ]),
])

# Create the add data tab content with form
add_data_tab = html.Div([
    html.Div([
        html.Div([
            html.H3("Adicionar Novos Dados", style={'color': COLORS['title'], 'textAlign': 'center', 'marginBottom': '10px'}),
            html.P("Preencha o formulário abaixo para adicionar novos dados à pesquisa sobre a escala 6x1.",
                   style={'textAlign': 'center', 'marginBottom': '30px', 'color': COLORS['text'], 'fontSize': '16px'}),
        ], style={'borderBottom': f'1px solid {COLORS["background"]}', 'paddingBottom': '15px', 'marginBottom': '20px'}),

        # Form
        html.Form([
            # Form sections
            html.Div([
                # Left column - Work info
                html.Div([
                    html.Div([
                        html.H4("Informações de Trabalho",
                               style={'color': COLORS['title'], 'marginBottom': '20px', 'fontSize': '18px',
                                     'borderBottom': f'2px solid {COLORS["secondary"]}', 'paddingBottom': '10px'}),

                        # Escala 6x1
                        html.Div([
                            html.Label("Escala 6x1", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.RadioItems(
                                id='input-escala6x1',
                                options=[
                                    {'label': ' Sim', 'value': 'Sim'},
                                    {'label': ' Não', 'value': 'Não'}
                                ],
                                value='Sim',
                                style={'marginBottom': '20px'},
                                inputStyle={"marginRight": "5px"},
                                labelStyle={'marginRight': '15px', 'display': 'inline-block'}
                            ),
                        ], style={'marginBottom': '15px'}),

                        # Tempo na Escala
                        html.Div([
                            html.Label("Tempo na Escala 6x1", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.Dropdown(
                                id='input-tempo-escala',
                                options=[
                                    {'label': 'Menos de 1 ano', 'value': 'Menos de 1 ano'},
                                    {'label': '1-2 anos', 'value': '1-2 anos'},
                                    {'label': '3-5 anos', 'value': '3-5 anos'},
                                    {'label': 'Mais de 5 anos', 'value': 'Mais de 5 anos'}
                                ],
                                placeholder="Selecione o tempo",
                                style={'marginBottom': '20px', 'color': COLORS['text']}
                            ),
                        ]),

                        # Contrato
                        html.Div([
                            html.Label("Contrato de Trabalho", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.Dropdown(
                                id='input-contrato',
                                options=[
                                    {'label': 'CLT', 'value': 'CLT'},
                                    {'label': 'PJ', 'value': 'PJ'},
                                    {'label': 'Temporário', 'value': 'Temporário'},
                                    {'label': 'Outro', 'value': 'Outro'}
                                ],
                                placeholder="Selecione o contrato",
                                style={'marginBottom': '20px', 'color': COLORS['text']}
                            ),
                        ]),

                        # Horas
                        html.Div([
                            html.Label("Horas de Trabalho", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.Dropdown(
                                id='input-horas',
                                options=[
                                    {'label': 'Até 30h semanais', 'value': 'Até 30h semanais'},
                                    {'label': '30-40h semanais', 'value': '30-40h semanais'},
                                    {'label': '40-44h semanais', 'value': '40-44h semanais'},
                                    {'label': 'Mais de 44h semanais', 'value': 'Mais de 44h semanais'}
                                ],
                                placeholder="Selecione as horas",
                                style={'marginBottom': '20px', 'color': COLORS['text']}
                            ),
                        ]),

                        # Ocupação e Estado
                        html.Div([
                            html.Label("Ocupação", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.Input(
                                id='input-ocupacao',
                                type='text',
                                placeholder="Digite a ocupação",
                                style={'width': '100%', 'padding': '10px', 'marginBottom': '20px', 'borderRadius': '5px',
                                      'border': f'1px solid {COLORS["background"]}'}
                            ),
                        ]),

                        html.Div([
                            html.Label("Estado", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.Dropdown(
                                id='input-estado',
                                options=[
                                    {'label': estado, 'value': estado} for estado in sorted(df['EstadoTrabalho'].unique())
                                ],
                                placeholder="Selecione o estado",
                                style={'marginBottom': '20px', 'color': COLORS['text']}
                            ),
                        ]),
                    ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px',
                             'boxShadow': '0 2px 5px rgba(0,0,0,0.05)', 'height': '100%'})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),

                # Right column - Personal info and impacts
                html.Div([
                    # Personal info
                    html.Div([
                        html.H4("Informações Pessoais",
                               style={'color': COLORS['title'], 'marginBottom': '20px', 'fontSize': '18px',
                                     'borderBottom': f'2px solid {COLORS["accent"]}', 'paddingBottom': '10px'}),

                        # Sexo
                        html.Div([
                            html.Label("Sexo", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.RadioItems(
                                id='input-sexo',
                                options=[
                                    {'label': ' Masculino', 'value': 'Masculino'},
                                    {'label': ' Feminino', 'value': 'Feminino'},
                                    {'label': ' Outro', 'value': 'Outro'}
                                ],
                                style={'marginBottom': '20px'},
                                inputStyle={"marginRight": "5px"},
                                labelStyle={'marginRight': '15px', 'display': 'inline-block'}
                            ),
                        ]),

                        # Escolaridade
                        html.Div([
                            html.Label("Escolaridade", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.Dropdown(
                                id='input-escolaridade',
                                options=[
                                    {'label': 'Ensino Fundamental', 'value': 'Ensino Fundamental'},
                                    {'label': 'Ensino Médio', 'value': 'Ensino Médio'},
                                    {'label': 'Ensino Superior', 'value': 'Ensino Superior'},
                                    {'label': 'Pós-graduação', 'value': 'Pós-graduação'}
                                ],
                                placeholder="Selecione a escolaridade",
                                style={'marginBottom': '20px', 'color': COLORS['text']}
                            ),
                        ]),

                        # Rendimento
                        html.Div([
                            html.Label("Rendimento", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                            dcc.Dropdown(
                                id='input-rendimento',
                                options=[
                                    {'label': 'Até 1 salário mínimo', 'value': 'Até 1 salário mínimo'},
                                    {'label': '1-3 salários mínimos', 'value': '1-3 salários mínimos'},
                                    {'label': '3-5 salários mínimos', 'value': '3-5 salários mínimos'},
                                    {'label': 'Mais de 5 salários mínimos', 'value': 'Mais de 5 salários mínimos'}
                                ],
                                placeholder="Selecione o rendimento",
                                style={'marginBottom': '20px', 'color': COLORS['text']}
                            ),
                        ]),

                        # Impactos
                        html.H4("Avaliação de Impactos",
                               style={'color': COLORS['title'], 'marginTop': '30px', 'marginBottom': '20px', 'fontSize': '18px',
                                     'borderBottom': f'2px solid {COLORS["accent"]}', 'paddingBottom': '10px'}),

                        # Impacto Família
                        html.Div([
                            html.Div([
                                html.Label("Impacto na Vida Familiar", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                                html.Div("👪", style={'position': 'absolute', 'right': '10px', 'top': '0px', 'fontSize': '20px'}),
                            ], style={'position': 'relative'}),
                            dcc.RadioItems(
                                id='input-impacto-familia',
                                options=[
                                    {'label': ' Discordo totalmente', 'value': 'Discordo totalmente'},
                                    {'label': ' Discordo', 'value': 'Discordo'},
                                    {'label': ' Neutro', 'value': 'Neutro'},
                                    {'label': ' Concordo', 'value': 'Concordo'},
                                    {'label': ' Concordo totalmente', 'value': 'Concordo totalmente'}
                                ],
                                style={'marginBottom': '20px'},
                                inputStyle={"marginRight": "5px"},
                                labelStyle={'display': 'block', 'marginBottom': '5px'}
                            ),
                        ], style={'marginBottom': '15px'}),

                        # Impacto Saúde Física
                        html.Div([
                            html.Div([
                                html.Label("Impacto na Saúde Física", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                                html.Div("💪", style={'position': 'absolute', 'right': '10px', 'top': '0px', 'fontSize': '20px'}),
                            ], style={'position': 'relative'}),
                            dcc.RadioItems(
                                id='input-impacto-fisica',
                                options=[
                                    {'label': ' Discordo totalmente', 'value': 'Discordo totalmente'},
                                    {'label': ' Discordo', 'value': 'Discordo'},
                                    {'label': ' Neutro', 'value': 'Neutro'},
                                    {'label': ' Concordo', 'value': 'Concordo'},
                                    {'label': ' Concordo totalmente', 'value': 'Concordo totalmente'}
                                ],
                                style={'marginBottom': '20px'},
                                inputStyle={"marginRight": "5px"},
                                labelStyle={'display': 'block', 'marginBottom': '5px'}
                            ),
                        ], style={'marginBottom': '15px'}),

                        # Impacto Saúde Mental
                        html.Div([
                            html.Div([
                                html.Label("Impacto na Saúde Mental", style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '8px'}),
                                html.Div("🧠", style={'position': 'absolute', 'right': '10px', 'top': '0px', 'fontSize': '20px'}),
                            ], style={'position': 'relative'}),
                            dcc.RadioItems(
                                id='input-impacto-mental',
                                options=[
                                    {'label': ' Discordo totalmente', 'value': 'Discordo totalmente'},
                                    {'label': ' Discordo', 'value': 'Discordo'},
                                    {'label': ' Neutro', 'value': 'Neutro'},
                                    {'label': ' Concordo', 'value': 'Concordo'},
                                    {'label': ' Concordo totalmente', 'value': 'Concordo totalmente'}
                                ],
                                style={'marginBottom': '20px'},
                                inputStyle={"marginRight": "5px"},
                                labelStyle={'display': 'block', 'marginBottom': '5px'}
                            ),
                        ], style={'marginBottom': '15px'}),
                    ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px',
                             'boxShadow': '0 2px 5px rgba(0,0,0,0.05)', 'height': '100%'})
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            ], style={'marginBottom': '25px'}),

            # Textarea for impacts description
            html.Div([
                html.Div([
                    html.Label("Descreva os impactos da escala 6x1 na sua vida",
                              style={'fontWeight': 'bold', 'color': COLORS['title'], 'display': 'block', 'marginBottom': '10px'}),
                    dcc.Textarea(
                        id='input-impactos-texto',
                        placeholder="Descreva aqui como a escala 6x1 impacta sua vida pessoal, familiar, saúde física e mental...",
                        style={'width': '100%', 'height': '120px', 'padding': '15px', 'marginBottom': '20px',
                              'borderRadius': '8px', 'border': f'1px solid {COLORS["background"]}',
                              'fontSize': '14px'}
                    ),
                ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px',
                         'boxShadow': '0 2px 5px rgba(0,0,0,0.05)'})
            ], style={'marginBottom': '25px'}),

            # Submit button
            html.Div([
                html.Button(
                    '💾 Adicionar Dados',
                    id='submit-button',
                    n_clicks=0,
                    style={
                        'backgroundColor': COLORS['primary'],
                        'color': 'white',
                        'border': 'none',
                        'padding': '12px 30px',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'fontSize': '16px',
                        'fontWeight': 'bold',
                        'boxShadow': '0 2px 5px rgba(0,0,0,0.1)',
                        'transition': 'all 0.3s ease',
                    }
                ),
                html.Div(id='submit-output', style={'marginTop': '20px', 'padding': '10px', 'borderRadius': '5px'})
            ], style={'textAlign': 'center', 'marginTop': '10px'})
        ])
    ], style=CARD_STYLE),
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

    # Tabs with modern styling
    html.Div([
        dcc.Tabs(
            id="tabs",
            value='tab-dashboard',
            children=[
                dcc.Tab(
                    label='📊 Dashboard',
                    value='tab-dashboard',
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE
                ),
                dcc.Tab(
                    label='➕ Adicionar Dados',
                    value='tab-add-data',
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE
                ),
            ],
            style={'marginBottom': '20px'}
        ),
    ], style={'marginBottom': '20px'}),

    # Tab content
    html.Div(id='tabs-content', style={'minHeight': '500px'}),

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

# Callback to update tab content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-dashboard':
        return dashboard_tab
    elif tab == 'tab-add-data':
        return add_data_tab

# Callback to refresh dashboard
@app.callback(
    [Output('familia-bar-chart', 'figure'),
     Output('fisica-bar-chart', 'figure'),
     Output('mental-bar-chart', 'figure'),
     Output('estado-bar-chart', 'figure')],
    [Input('refresh-button', 'n_clicks'),
     Input('tabs', 'value')]  # Adicionar tabs como input para atualizar quando mudar de aba
)
def refresh_dashboard(_, tab_value):
    # Prevenir atualização se não estiver na aba do dashboard
    if tab_value != 'tab-dashboard':
        raise PreventUpdate

    # Connect to the SQLite database
    conn = sqlite3.connect('base.sqlite')

    # Load the data
    updated_df = pd.read_sql("SELECT * FROM Planilha1", conn)

    # Close the connection
    conn.close()

    # Define the order of responses
    order = ["Discordo totalmente", "Discordo", "Neutro", "Concordo", "Concordo totalmente"]

    # 1. Impacto na Vida Familiar - Gráfico de barras horizontais
    familia_counts = updated_df['ImpactoVidaFamiliar'].value_counts().reset_index()
    familia_counts.columns = ['resposta', 'contagem']
    familia_counts['resposta'] = pd.Categorical(familia_counts['resposta'], categories=order, ordered=True)
    familia_counts = familia_counts.sort_values('resposta')

    updated_familia_bar = px.bar(
        familia_counts,
        y='resposta',  # Agora no eixo y para barras horizontais
        x='contagem',  # Agora no eixo x
        title="Impacto na Vida Familiar",
        color_discrete_sequence=[COLORS['chart1']],
        orientation='h',  # Horizontal
        text='contagem',  # Mostrar valores nas barras
        labels={'resposta': '', 'contagem': 'Quantidade de Respostas'},
        height=350,
    )
    updated_familia_bar.update_layout(
        title_font=dict(size=18, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(autorange="reversed"),  # Inverte a ordem para ter "Concordo totalmente" no topo
    )
    updated_familia_bar.update_traces(
        marker_color=COLORS['chart1'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition='outside',
    )

    # 2. Impacto na Saúde Física - Gráfico de barras horizontais
    fisica_counts = updated_df['ImpactoSaudeFisica'].value_counts().reset_index()
    fisica_counts.columns = ['resposta', 'contagem']
    fisica_counts['resposta'] = pd.Categorical(fisica_counts['resposta'], categories=order, ordered=True)
    fisica_counts = fisica_counts.sort_values('resposta')

    updated_fisica_bar = px.bar(
        fisica_counts,
        y='resposta',
        x='contagem',
        title="Impacto na Saúde Física",
        color_discrete_sequence=[COLORS['chart3']],
        orientation='h',
        text='contagem',
        labels={'resposta': '', 'contagem': 'Quantidade de Respostas'},
        height=350,
    )
    updated_fisica_bar.update_layout(
        title_font=dict(size=18, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(autorange="reversed"),
    )
    updated_fisica_bar.update_traces(
        marker_color=COLORS['chart3'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition='outside',
    )

    # 3. Impacto na Saúde Mental - Gráfico de barras horizontais
    mental_counts = updated_df['ImpactoSaudeMental'].value_counts().reset_index()
    mental_counts.columns = ['resposta', 'contagem']
    mental_counts['resposta'] = pd.Categorical(mental_counts['resposta'], categories=order, ordered=True)
    mental_counts = mental_counts.sort_values('resposta')

    updated_mental_bar = px.bar(
        mental_counts,
        y='resposta',
        x='contagem',
        title="Impacto na Saúde Mental",
        color_discrete_sequence=[COLORS['chart2']],
        orientation='h',
        text='contagem',
        labels={'resposta': '', 'contagem': 'Quantidade de Respostas'},
        height=350,
    )
    updated_mental_bar.update_layout(
        title_font=dict(size=18, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Quantidade",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(autorange="reversed"),
    )
    updated_mental_bar.update_traces(
        marker_color=COLORS['chart2'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{x}',
        textposition='outside',
    )

    # 4. Distribuição por Estado - Gráfico de barras
    estado_counts = updated_df['EstadoTrabalho'].value_counts().reset_index()
    estado_counts.columns = ['estado', 'contagem']
    estado_counts = estado_counts.sort_values('contagem', ascending=False).head(10)  # Top 10 estados

    updated_estado_bar = px.bar(
        estado_counts,
        x='estado',
        y='contagem',
        title="Top Estados",
        color_discrete_sequence=[COLORS['chart4']],
        text='contagem',
        labels={'estado': 'Estado', 'contagem': 'Quantidade'},
        height=350,
    )
    updated_estado_bar.update_layout(
        title_font=dict(size=18, family="Segoe UI", color=COLORS['title']),
        font=dict(family="Segoe UI"),
        xaxis_title="Estado",
        yaxis_title="Quantidade",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
    )
    updated_estado_bar.update_traces(
        marker_color=COLORS['chart4'],
        marker_line_color='rgba(0,0,0,0)',
        opacity=0.8,
        texttemplate='%{y}',
        textposition='outside',
    )

    return updated_familia_bar, updated_fisica_bar, updated_mental_bar, updated_estado_bar

# Callback to handle form submission
@app.callback(
    Output('submit-output', 'children'),
    Input('submit-button', 'n_clicks'),
    [State('input-escala6x1', 'value'),
     State('input-tempo-escala', 'value'),
     State('input-contrato', 'value'),
     State('input-horas', 'value'),
     State('input-ocupacao', 'value'),
     State('input-estado', 'value'),
     State('input-sexo', 'value'),
     State('input-escolaridade', 'value'),
     State('input-rendimento', 'value'),
     State('input-impacto-familia', 'value'),
     State('input-impacto-fisica', 'value'),
     State('input-impacto-mental', 'value'),
     State('input-impactos-texto', 'value')]
)
def submit_form(n_clicks, escala6x1, tempo_escala, contrato, horas, ocupacao, estado,
                sexo, escolaridade, rendimento, impacto_familia, impacto_fisica,
                impacto_mental, impactos_texto):
    if n_clicks == 0:
        # Initial load, don't do anything
        raise PreventUpdate

    # Check if required fields are filled
    required_fields = [escala6x1, tempo_escala, contrato, horas, estado, sexo,
                      escolaridade, impacto_familia, impacto_fisica, impacto_mental]

    if None in required_fields or '' in required_fields:
        return html.Div([
            html.P("Por favor, preencha todos os campos obrigatórios.",
                  style={'color': COLORS['danger'], 'fontWeight': 'bold'})
        ])

    try:
        # Connect to the database
        conn = sqlite3.connect('base.sqlite')
        cursor = conn.cursor()

        # Insert the new data
        cursor.execute('''
            INSERT INTO Planilha1 (
                Confirmacao, Escala6x1, TempoEscala6x1, ContratoTrabalho, HorasTrabalho,
                Occupation_Respostas, EstadoTrabalho, Sexo, Escolaridade, Rendimento,
                ImpactoVidaFamiliar, ImpactoSaudeFisica, ImpactoSaudeMental, Impactos
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Sim', escala6x1, tempo_escala, contrato, horas,
            ocupacao, estado, sexo, escolaridade, rendimento,
            impacto_familia, impacto_fisica, impacto_mental, impactos_texto
        ))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Return success message
        return html.Div([
            html.P("Dados adicionados com sucesso!",
                  style={'color': COLORS['success'], 'fontWeight': 'bold'})
        ])

    except Exception as e:
        # Return error message
        return html.Div([
            html.P(f"Erro ao adicionar dados: {str(e)}",
                  style={'color': COLORS['danger'], 'fontWeight': 'bold'})
        ])

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
