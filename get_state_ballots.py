import json
import concurrent.futures as cf

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
            "RN": "Rio Grande do Norte",
            "RS": "Rio Grande do Sul",
            "RO": "Rondônia",
            "RR": "Roraima",
            "SC": "Santa Catarina",
            "SP": "São Paulo",
            "SE": "Sergipe",
            "TO": "Tocantins",
            "ZZ":"Exterior"
            }


HEADERS = {
  'Accept': 'application/json, text/plain, */*'
}

URL_TEMPLATE = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/config/{uf}/{uf}-p000407-cs.json"


def get_state_ballot(state_code:str) -> None:
    url_request = URL_TEMPLATE.format(uf=state_code.lower())
    file_name = url_request.split("/")[-1]
    print(f"getting data for -> {state_code}")
    response = requests.get(url = url_request, headers = HEADERS)
    if response.status_code == 200:
        with open(f"./state_ballots/{file_name}", "w+") as fp:
            json.dump(response.json(),fp)
        print(f"saved file -> {file_name}")
    else:
        print(f"for state {state_code} request failed")

with cf.ThreadPoolExecutor() as executor:
    executor.map(get_state_ballot, states.keys())
