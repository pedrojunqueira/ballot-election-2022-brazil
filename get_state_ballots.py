import json

import requests

states = {
            "AC": "Acre",
            "AL": "Alagoas",
            "AP": "Amapá",
            "AM": "Amapá",
            "BA": "Bahia",
            "CE": "Ceará",
            "DF": "Distrito Federal",
            "ES": "Espirito Santo",
            "GO": "Goiás",
            "MA": "Maranhão",
            "MS": "Mato Grosso do Sul",
            "MT": "Mato Grosso",
            "MG": "Minas Gerais",
            "PA": "Pará",
            "PB": "Paraíba",
            "PR": "Paraná",
            "PE": "Pernambuco",
            "PI": "Piauí",
            "RJ": "Rio de Janeiro",
            "RS": "Rio Grande do Sul",
            "RO": "Rondônia",
            "RR": "Roraima",
            "SC": "Santa Catarina",
            "SP": "São Paulo",
            "SE": "Sergipe",
            "TO": "Tocantins",
            "DF":"Distrito Federal", 
            "ZZ":"Exterior"
            }


headers = {
  'Accept': 'application/json, text/plain, */*'
}

url = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/config/{uf}/{uf}-p000407-cs.json"


for uf in states.keys():
    url_request = url.format(uf=uf.lower())
    file_name = url_request.split("/")[-1]
    print(f"getting data for -> {uf}")
    response = requests.request("GET", url_request, headers=headers)
    if response.status_code == 200:
        with open(f"./state_ballots/{file_name}", "w+") as fp:
            json.dump(response.json(),fp)
        print(f"saved file -> {file_name}")
    else:
        print(f"for state {uf} request failed")




