import pandas as pd
import wikipedia

sheet_id = "1G-PYCy2HjnZIC9Mbrh1ICGa_aZM6SGKg"
gid = "1126475456"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

df = pd.read_csv(url)

def pesquisar_por_id(id):
    resultado = df[df["numtombo"] == int(id)]
    if resultado.empty:
        print(f"Nenhum registro encontrado com esse id = {id}")
    else:
        return resultado.to_dict(orient="records")[0]  
