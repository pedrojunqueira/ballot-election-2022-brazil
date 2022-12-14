import json
from pathlib import Path
import concurrent.futures as cf
from datetime import datetime

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
            "RN": "Rio Grande do Norte",
            "RO": "Rondônia",
            "RR": "Roraima",
            "SC": "Santa Catarina",
            "SP": "São Paulo",
            "SE": "Sergipe",
            "TO": "Tocantins",
            "ZZ":"Exterior"
            }

STATE_BALLOTS_FILE_PATH = "./state_ballots/{uf}-p000407-cs.json"

URL_HASH = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/{uf}/{mu_cd}/{zone_cd}/{section_cd}/p000407-{uf}-m{mu_cd}-z{zone_cd}-s{section_cd}-aux.json"

URL_BU = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/{uf}/{mu_cd}/{zone_cd}/{section_cd}/{hash}/o00407-{mu_cd}{zone_cd}{section_cd}.bu"

BASE_DIR = Path(".").resolve()

bu_path = BASE_DIR / "bu"

BU_FILES = [ i.name for i in bu_path.iterdir() if i.suffix == '.bu']

def calculate_state_ballot_report(state_code:str)-> list:
    total_ballots = 0
    with open(STATE_BALLOTS_FILE_PATH.format(uf=state_code.lower()), "r+") as fp:
        state_data = json.load(fp)

    state_code = state_data["abr"][0]["cd"]
    councils  = state_data["abr"][0]["mu"]

    for council in councils:
        zones = council["zon"]
        for zone in zones:
            sections = zone["sec"]
            for section in sections:
                total_ballots += 1
    
    print("###############")
    print(f"State: {state_code}")
    print(f"Number of councils: {len(councils)}")
    print(f"Total number of ballots: {total_ballots}")
    print("###############")
    print()

    return total_ballots

def get_state_ballot_codes(state_code:str)-> list:
    ballots = []

    with open(STATE_BALLOTS_FILE_PATH.format(uf=state_code.lower()), "r+") as fp:
        state_data = json.load(fp)

    state_code = state_data["abr"][0]["cd"]
    councils  = state_data["abr"][0]["mu"]

    for council in councils:
        mu_cd = council["cd"]
        zones = council["zon"]
        for zone in zones:
            zone_cd = zone["cd"]
            sections = zone["sec"]
            for section in sections:
                section_cd = section["ns"]
                ballots.append(dict(state_code=state_code.lower(), mu_cd=mu_cd, zone_cd=zone_cd, section_cd=section_cd))
                ballot_codes = {}
    
    return ballots
                

def get_hash(ballot_codes:dict)-> str:
    
    url_request = URL_HASH.format(uf=ballot_codes["state_code"], mu_cd=ballot_codes["mu_cd"], 
                                    zone_cd=ballot_codes["zone_cd"],section_cd=ballot_codes["section_cd"])

    headers = {'Accept': 'application/json, text/plain, */*'}

    response = requests.get(url_request, headers=headers)

    hash_data  = response.json()
    hash_code = hash_data["hashes"][0]["hash"]
    
    return hash_code


def get_bu_file_name(ballot_codes:dict)-> str:
    mu_cd = ballot_codes['mu_cd']
    zone_cd = ballot_codes['zone_cd']
    section_cd = ballot_codes['section_cd']
    return f"o00407-{mu_cd}{zone_cd}{section_cd}.bu"


def get_ballot_bu(ballot_codes:dict, hash_code:str)->None:

    url_request = URL_BU.format(uf=ballot_codes["state_code"], mu_cd=ballot_codes["mu_cd"], 
                                    zone_cd=ballot_codes["zone_cd"],section_cd=ballot_codes["section_cd"],hash=hash_code)

    headers = {'Referer': 'https://resultados.tse.jus.br/oficial/app/index.html'}


    response = requests.get(url_request, headers=headers)

    file_name = get_bu_file_name(ballot_codes)

    with open(f"./bu/{file_name}", "wb") as fp:
        fp.write(response.content)

    print(f"file: {file_name} saved successfully")


def process_ballot(ballot_codes:dict)->None:
    hash_code = get_hash(ballot_codes)
    get_ballot_bu(ballot_codes, hash_code)


def create_batches(batch_size:int, ballots:list)-> list:
    batches_list = []
    batches =  int(round(len(ballots) / batch_size,0))
    reminder =  len(ballots) % batch_size
    end = 0
    for i in range(batches + 1):
        start = end
        end += batch_size if i < batches else (reminder+1)
        batches_list.append(ballots[start:end])
        start = end
    return batches_list

def get_reminder_ballots(batch:list)->list:
    return [ballot for ballot in batch if get_bu_file_name(ballot) not in BU_FILES]


if __name__ == "__main__":

    state_codes = [s for s in states.keys()]
    start_time = datetime.now()

    # # download BUs from site

    # for state_code in state_codes[20:21]:
    #     try:
    #         print(f"processing state_code: {state_code}")
    #         ballots = get_state_ballot_codes(state_code)
    #         batches = create_batches(200, ballots)
    #         batch_count = 1
    #         for batch in batches:
    #             ballots_to_process = get_reminder_ballots(batch)
    #             # print(len(ballots_to_process))
    #             if len(ballots_to_process) > 0:
    #                 print(f"processing batch {batch_count}/{len(batches)} ")
    #                 # with cf.ThreadPoolExecutor(max_workers=12) as executor:
    #                 #     executor.map(process_ballot, batch)
    #             batch_count += 1
    #     except Exception as e:
    #         print(e)

    print(len(BU_FILES))

    ballot_count_total = 0

    for state_code in state_codes:
        subtotal = calculate_state_ballot_report(state_code)
        ballot_count_total += subtotal
    print(f"total ballots in 2022: {ballot_count_total}")

    finish_time = datetime.now()

    total_time = finish_time - start_time

    # with open("brazil-states.json", "w+") as fp:
    #     json.dump(states, fp)

    print(f"execution took {total_time.seconds} seconds")




    