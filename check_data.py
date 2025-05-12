import sqlite3
import pandas as pd

# Conectar ao banco de dados
conn = sqlite3.connect('base.sqlite')

# Consultar valores únicos de Rendimento
rendimento_query = "SELECT DISTINCT Rendimento FROM Planilha1"
rendimento_values = pd.read_sql(rendimento_query, conn)
print("Valores únicos de Rendimento:")
print(rendimento_values)
print("\n")

# Consultar valores únicos de Escolaridade
escolaridade_query = "SELECT DISTINCT Escolaridade FROM Planilha1"
escolaridade_values = pd.read_sql(escolaridade_query, conn)
print("Valores únicos de Escolaridade:")
print(escolaridade_values)

# Fechar a conexão
conn.close()
