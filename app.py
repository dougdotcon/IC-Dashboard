import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3

# Definir cores e estilo
COLORS = {
    'background': '#f8f9fa',
    'text': '#343a40',
    'primary': '#6c5ce7',
    'secondary': '#a29bfe',
    'accent': '#74b9ff',
    'success': '#00b894',
    'warning': '#fdcb6e',
    'danger': '#e17055'
}

# Estilo global
GLOBAL_STYLE = {
    'font-family': 'Arial, sans-serif',
    'backgroundColor': COLORS['background'],
    'color': COLORS['text'],
    'margin': '0px',
    'padding': '20px',
}

CARD_STYLE = {
    'boxShadow': '0 4px 6px 0 rgba(0, 0, 0, 0.1)',
    'borderRadius': '8px',
    'backgroundColor': 'white',
    'padding': '20px',
    'marginBottom': '20px',
}

HEADER_STYLE = {
    'color': COLORS['primary'],
    'textAlign': 'center',
    'padding': '10px',
    'marginBottom': '20px',
    'borderBottom': f'2px solid {COLORS["primary"]}',
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

# Create figures directly with improved styling
# 1. Escala 6x1 distribution
escala_counts = df['Escala6x1'].value_counts()
escala_pie = px.pie(
    names=escala_counts.index,
    values=escala_counts.values,
    title="Distribuição de Trabalhadores na Escala 6x1",
    color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent']],
    hole=0.4,
)
escala_pie.update_layout(
    title_font_size=18,
    title_font_family="Arial",
    title_font_color=COLORS['text'],
    legend_title_font_color=COLORS['text'],
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

# 2. Impacto na Vida Familiar
familia_counts = df['ImpactoVidaFamiliar'].value_counts().reset_index()
familia_counts.columns = ['resposta', 'contagem']
# Define the order of responses
order = ["Discordo totalmente", "Discordo", "Neutro", "Concordo", "Concordo totalmente"]
familia_counts['resposta'] = pd.Categorical(familia_counts['resposta'], categories=order, ordered=True)
familia_counts = familia_counts.sort_values('resposta')
familia_bar = px.bar(
    familia_counts,
    x='resposta',
    y='contagem',
    title="Impacto na Vida Familiar",
    color_discrete_sequence=[COLORS['primary']],
)
familia_bar.update_layout(
    title_font_size=18,
    title_font_family="Arial",
    title_font_color=COLORS['text'],
    xaxis_title="",
    yaxis_title="Quantidade",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

# 3. Impacto na Saúde Física
fisica_counts = df['ImpactoSaudeFisica'].value_counts().reset_index()
fisica_counts.columns = ['resposta', 'contagem']
fisica_counts['resposta'] = pd.Categorical(fisica_counts['resposta'], categories=order, ordered=True)
fisica_counts = fisica_counts.sort_values('resposta')
fisica_bar = px.bar(
    fisica_counts,
    x='resposta',
    y='contagem',
    title="Impacto na Saúde Física",
    color_discrete_sequence=[COLORS['accent']],
)
fisica_bar.update_layout(
    title_font_size=18,
    title_font_family="Arial",
    title_font_color=COLORS['text'],
    xaxis_title="",
    yaxis_title="Quantidade",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

# 4. Impacto na Saúde Mental
mental_counts = df['ImpactoSaudeMental'].value_counts().reset_index()
mental_counts.columns = ['resposta', 'contagem']
mental_counts['resposta'] = pd.Categorical(mental_counts['resposta'], categories=order, ordered=True)
mental_counts = mental_counts.sort_values('resposta')
mental_bar = px.bar(
    mental_counts,
    x='resposta',
    y='contagem',
    title="Impacto na Saúde Mental",
    color_discrete_sequence=[COLORS['secondary']],
)
mental_bar.update_layout(
    title_font_size=18,
    title_font_family="Arial",
    title_font_color=COLORS['text'],
    xaxis_title="",
    yaxis_title="Quantidade",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

# Initialize the Dash app
app = dash.Dash(
    __name__,
    title="Dashboard 6x1",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Define the layout with pre-created figures
app.layout = html.Div(style=GLOBAL_STYLE, children=[
    # Header
    html.Div([
        html.H1("Dashboard de Análise da Escala 6x1", style=HEADER_STYLE),
        html.P("Análise dos impactos da escala 6x1 na vida dos trabalhadores",
               style={'textAlign': 'center', 'marginBottom': '30px', 'fontSize': '18px'}),
    ]),

    # First row - Basic stats
    html.Div([
        html.Div([
            html.Div([
                html.H3("Distribuição da Escala 6x1", style={'color': COLORS['primary']}),
                dcc.Graph(figure=escala_pie),
            ], style=CARD_STYLE),
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            html.Div([
                html.H3("Impactos na Vida Familiar", style={'color': COLORS['primary']}),
                dcc.Graph(figure=familia_bar),
            ], style=CARD_STYLE),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    # Second row - Health impacts
    html.Div([
        html.Div([
            html.Div([
                html.H3("Impactos na Saúde Física", style={'color': COLORS['primary']}),
                dcc.Graph(figure=fisica_bar),
            ], style=CARD_STYLE),
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            html.Div([
                html.H3("Impactos na Saúde Mental", style={'color': COLORS['primary']}),
                dcc.Graph(figure=mental_bar),
            ], style=CARD_STYLE),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    # Footer
    html.Div([
        html.Hr(),
        html.P("Dashboard de Análise da Escala 6x1 © 2023", style={'textAlign': 'center'}),
    ], style={'marginTop': '30px'})
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
