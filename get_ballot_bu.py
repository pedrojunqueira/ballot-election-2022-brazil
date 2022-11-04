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

file_path = "./state_ballots/{uf}-p000407-cs.json"

section_count = 0

for uf in states.keys():

    with open(file_path.format(uf=uf.lower()), "r+") as fp:
        state_data = json.load(fp)

    state_uf = state_data["abr"][0]["cd"]
    state_name = state_data["abr"][0]["ds"]
    councils  = state_data["abr"][0]["mu"]

    for council in councils:
        # print(council["cd"])
        # print(council["nm"])
        zones = council["zon"]
        for zone in zones:
            zone_name = zone["cd"]
            sections = zone["sec"]
            for section in sections:
                section_count += 1
                section_ns = section["ns"]
                section_nsp = section["nsp"]

print(section_count)

days_to_process = section_count/60/60/24

print(days_to_process)


##### get hash

uf = "zz"
mu_cd = "29491"
zone_cd = "0001"
section_cd = "0735"


# zz/29491/0001/0735/p000407-zz-m29491-z0001-s0735-aux.json

url = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/{uf}/{mu_cd}/{zone_cd}/{section_cd}/p000407-{uf}-m{mu_cd}-z{zone_cd}-s{section_cd}-aux.json"

url_request = url.format(uf=uf, mu_cd=mu_cd, zone_cd=zone_cd,section_cd=section_cd)

print(url_request)

headers = {'Accept': 'application/json, text/plain, */*'}

response = requests.get(url_request, headers=headers)

if response.status_code == 200:
    r  = response.json()
    hash_code = r["hashes"][0]["hash"]
    print(hash_code)

## get BU

uf = "zz"
mu_cd = "29491"
zone_cd = "0001"
section_cd = "0735"

url = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/{uf}/{mu_cd}/{zone_cd}/{section_cd}/{hash}/o00407-{mu_cd}{zone_cd}{section_cd}.bu"

url_request = url.format(uf=uf, mu_cd=mu_cd, zone_cd=zone_cd,section_cd=section_cd, hash=hash_code)

print(url_request)

# url =   "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/zz/29491/0001/0735/2d30346a4f726357683073327967314634454f766b78766d4b436d7161684a74532d2d35466c2d7a346e493d/o00407-2949100010735.bu"

payload={}
headers = {
  'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
  'Referer': 'https://resultados.tse.jus.br/oficial/app/index.html',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
  'sec-ch-ua-platform': '"macOS"'
}

response = requests.request("GET", url_request, headers=headers, data=payload)

file_name = f"o00407-{mu_cd}{zone_cd}{section_cd}.bu"

with open(f"./bu/{file_name}", "wb") as fp:
    fp.write(response.content)
