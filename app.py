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
    suppress_callback_exceptions=True,  # Add this to suppress callback exceptions for components not in initial layout
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

# Removed add_data_tab definition

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

    # Dashboard content
    html.Div(dashboard_tab, style={'minHeight': '500px'}),

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

# Callback to refresh dashboard
@app.callback(
    [Output('familia-bar-chart', 'figure'),
     Output('fisica-bar-chart', 'figure'),
     Output('mental-bar-chart', 'figure'),
     Output('estado-bar-chart', 'figure')],
    [Input('refresh-button', 'n_clicks')]
)
def refresh_dashboard(_):
    # Connect to the SQLite database
    conn = sqlite3.connect('base.sqlite')

    # Load the data
    updated_df = pd.read_sql("SELECT * FROM Planilha1", conn)

    # Close the connection
    conn.close()

    # Recalcular KPIs (não afeta a interface diretamente, mas mantém os valores atualizados para próxima renderização)
    global df, total_respondentes, escala_6x1_count, escala_6x1_percent
    global homens_count, mulheres_count, homens_percent, mulheres_percent
    global familia_resposta_frequente, familia_resposta_count, familia_resposta_percent
    global fisica_resposta_frequente, fisica_resposta_count, fisica_resposta_percent
    global mental_resposta_frequente, mental_resposta_count, mental_resposta_percent

    # Atualizar o dataframe global
    df = updated_df

    # Recalcular todos os KPIs
    total_respondentes = len(df)
    escala_6x1_count = df[df['Escala6x1'] == 'Sim'].shape[0]
    escala_6x1_percent = round((escala_6x1_count / total_respondentes) * 100, 1)

    # Distribuição por sexo
    sexo_counts = df['Sexo'].value_counts()
    total_sexo = sexo_counts.sum()
    homens_count = sexo_counts.get('Masculino', 0)
    mulheres_count = sexo_counts.get('Feminino', 0)
    homens_percent = round((homens_count / total_sexo) * 100)
    mulheres_percent = round((mulheres_count / total_sexo) * 100)

    # Impacto na vida familiar
    familia_resposta_frequente = df['ImpactoVidaFamiliar'].value_counts().idxmax()
    familia_resposta_count = df['ImpactoVidaFamiliar'].value_counts().max()
    familia_resposta_percent = round((familia_resposta_count / total_respondentes) * 100)

    # Impacto na saúde física
    fisica_resposta_frequente = df['ImpactoSaudeFisica'].value_counts().idxmax()
    fisica_resposta_count = df['ImpactoSaudeFisica'].value_counts().max()
    fisica_resposta_percent = round((fisica_resposta_count / total_respondentes) * 100)

    # Impacto na saúde mental
    mental_resposta_frequente = df['ImpactoSaudeMental'].value_counts().idxmax()
    mental_resposta_count = df['ImpactoSaudeMental'].value_counts().max()
    mental_resposta_percent = round((mental_resposta_count / total_respondentes) * 100)

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

# Removed form submission callback

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
