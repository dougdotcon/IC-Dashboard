import sqlite3
import pandas as pd

# Conectar ao banco de dados
conn = sqlite3.connect('base.sqlite')

# Consultar valores únicos de ImpactoVidaFamiliar
impacto_familia_query = "SELECT DISTINCT ImpactoVidaFamiliar FROM Planilha1"
impacto_familia_values = pd.read_sql(impacto_familia_query, conn)
print("Valores únicos de ImpactoVidaFamiliar:")
print(impacto_familia_values)
print("\n")

# Consultar valores únicos de ImpactoSaudeFisica
impacto_fisica_query = "SELECT DISTINCT ImpactoSaudeFisica FROM Planilha1"
impacto_fisica_values = pd.read_sql(impacto_fisica_query, conn)
print("Valores únicos de ImpactoSaudeFisica:")
print(impacto_fisica_values)
print("\n")

# Consultar valores únicos de ImpactoSaudeMental
impacto_mental_query = "SELECT DISTINCT ImpactoSaudeMental FROM Planilha1"
impacto_mental_values = pd.read_sql(impacto_mental_query, conn)
print("Valores únicos de ImpactoSaudeMental:")
print(impacto_mental_values)
print("\n")

# Fechar a conexão
conn.close()
