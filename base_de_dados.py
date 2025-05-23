import pandas as pd
import wikipedia
import requests

wikipedia.set_lang("pt")

sheet_id = "1G-PYCy2HjnZIC9Mbrh1ICGa_aZM6SGKg"
gid = "1126475456"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

df = pd.read_csv(url)


def pesquisar_por_id(id):
    resultado = df[df["numtombo"] == int(id)]
    if resultado.empty:
        return None
    else:
        return resultado.to_dict(orient="records")[0] 


def pesquisar_por_nome_cientifico(nomecie):
    try:
        primeira_palavra, segunda_palavra = nomecie.strip().split(maxsplit=1)
    except ValueError:
        return None

    resultado = df[(df["genus"].str.lower() == primeira_palavra.lower()) &
                   (df["sp1"].str.lower() == segunda_palavra.lower())]

    if resultado.empty:
        return None
    else:
        return resultado.to_dict(orient="records")[0]

 

def buscar_nome_popular_wikipedia(nome_cientifico):
    try:
        pagina = wikipedia.page(nome_cientifico)
        resumo = pagina.summary
        return resumo
    except Exception as e:
        return None
    
def buscar_nome_popular_wikidata(nome_cientifico):
    url = "https://query.wikidata.org/sparql"
    headers = {"Accept": "application/sparql-results+json"}

    # 1. Tenta buscar alias em pt diferente do nome científico
    query_alias = f"""
    SELECT ?alias_pt WHERE {{
      ?item wdt:P225 "{nome_cientifico}" .
      ?item skos:altLabel ?alias_pt .
      FILTER(LANG(?alias_pt) = "pt")
      FILTER(?alias_pt != "{nome_cientifico}")
    }}
    LIMIT 1
    """

    response = requests.get(url, params={"query": query_alias}, headers=headers)
    if response.status_code == 200:
        results = response.json().get('results', {}).get('bindings', [])
        if results and 'alias_pt' in results[0]:
            return results[0]['alias_pt']['value'].title()

    # 2. Se não achou alias, tenta buscar label em pt diferente do nome científico
    query_label = f"""
    SELECT ?label_pt WHERE {{
      ?item wdt:P225 "{nome_cientifico}" .
      ?item rdfs:label ?label_pt .
      FILTER(LANG(?label_pt) = "pt")
      FILTER(?label_pt != "{nome_cientifico}")
    }}
    LIMIT 1
    """
    response = requests.get(url, params={"query": query_label}, headers=headers)
    if response.status_code == 200:
        results = response.json().get('results', {}).get('bindings', [])
        if results and 'label_pt' in results[0]:
            return results[0]['label_pt']['value'].title()

    return None

print(buscar_nome_popular_wikipedia("Spiraea ariifolia"))