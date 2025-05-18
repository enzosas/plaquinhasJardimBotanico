import pandas as pd
from placa import gera_placa
from pathlib import Path


pasta_dir = Path(__file__).parent / 'pasta'

# Le o arquivo CSV
df = pd.read_csv('Cópia de Plantas cadastro 25_05 - Página1.csv')

for index, row in df.iterrows():
    codigo = row['Código']
    nome_popular = row['Nome popular']
    nome_cientifico = row['Nome científico']
    link = f"https://jbsm.inf.ufsm.br/acervo/item/{codigo}"

    gera_placa(nome_popular, nome_cientifico, codigo, link, "layout0", "PrimeiraEntrega")