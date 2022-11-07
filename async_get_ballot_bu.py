import asyncio
from time import perf_counter
import json
from pathlib import Path

import aiohttp
import aiofiles

from get_ballot_bu import get_reminder_ballots

BASE_DIR = Path(".").resolve()

bu_path = BASE_DIR / "bu"

URL_HASH = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/{uf}/{mu_cd}/{zone_cd}/{section_cd}/p000407-{uf}-m{mu_cd}-z{zone_cd}-s{section_cd}-aux.json"
URL_BU = "https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/{uf}/{mu_cd}/{zone_cd}/{section_cd}/{hash}/o00407-{mu_cd}{zone_cd}{section_cd}.bu"
STATE_BALLOTS_FILE_PATH = "./state_ballots/{uf}-p000407-cs.json"

def get_state_ballot_codes(state_code:str)-> list:
    ballots = []

    with open(STATE_BALLOTS_FILE_PATH.format(uf=state_code.lower()), "r+") as fp:
        state_data = json.load(fp)

    state_code = state_data["abr"][0]["cd"]
    councils  = state_data["abr"][0]["mu"]

    for council in councils:
        mu_cd = council["cd"]
        mu_name = council["nm"]
        zones = council["zon"]
        for zone in zones:
            zone_cd = zone["cd"]
            sections = zone["sec"]
            for section in sections:
                section_cd = section["ns"]
                ballots.append(dict(state_code=state_code.lower(),
                                    mu_name=mu_name, mu_cd=mu_cd, zone_cd=zone_cd, section_cd=section_cd))
                ballot_codes = {}
    
    return ballots


async def fetch_hash(ballot_code:dict, session):
    
    url_request = URL_HASH.format(uf=ballot_code["state_code"], mu_cd=ballot_code["mu_cd"], 
                                zone_cd=ballot_code["zone_cd"],section_cd=ballot_code["section_cd"])

    async with session.get(url_request) as r:
        if r.status != 200:
            r.raise_for_status()
        text = await r.text()
        hash_data  = json.loads(text)
        hash_code = hash_data["hashes"][0]["hash"]
        return (ballot_code, hash_code)


async def fetch_bu(ballot_code:dict,hash_code:str,session):
    url_request = URL_BU.format(uf=ballot_code["state_code"], mu_cd=ballot_code["mu_cd"], 
                                    zone_cd=ballot_code["zone_cd"],section_cd=ballot_code["section_cd"],hash=hash_code)
    async with session.get(url_request) as r:
        if r.status != 200:
            r.raise_for_status()
        content = await r.content.read()
        return (ballot_code,content)

async def save_file(filename, content):
    async with aiofiles.open(bu_path / filename, "wb") as fp:
        await fp.write(content)
        await fp.flush()
    return f"{filename} successfully saved"

def get_bu_file_name(ballot_codes:dict)-> str:
    mu_cd = ballot_codes['mu_cd']
    zone_cd = ballot_codes['zone_cd']
    section_cd = ballot_codes['section_cd']
    return f"o00407-{mu_cd}{zone_cd}{section_cd}.bu"

async def save_files_task(bus):
    tasks = []
    for ballot, content in bus:
        filename = get_bu_file_name(ballot)
        task = asyncio.ensure_future(save_file(filename, content))
        tasks.append(task)
    contents = await asyncio.gather(*tasks)
    return contents


async def fetch_all(ballot_codes:dict, session):
    tasks = []
    for ballot_code in ballot_codes:
        task = asyncio.create_task(fetch_hash(ballot_code, session))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


async def fetch_all_bus(batch_input, session):
    tasks = []
    for ballot_code, hash_code in batch_input:
        task = asyncio.create_task(fetch_bu(ballot_code, hash_code, session))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


async def main(batch):
    batch
    async with aiohttp.ClientSession() as session:
        hashes = await fetch_all(batch, session)
    async with aiohttp.ClientSession() as session:
        bus = await fetch_all_bus(hashes, session)
    content = await save_files_task(bus)
    print(content)

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

if __name__ == '__main__':
    with open("brazil-states.json", "r") as fp:
        states = json.load(fp)
        state_codes = [s for s in states.keys()]
    for state in state_codes[12:13]:
        print(state)
        begin = perf_counter()
        st_ballots = get_state_ballot_codes(state)
        ballots = st_ballots
        batch_list = create_batches(70, ballots)
        for batch in batch_list:
            ballots_to_process = get_reminder_ballots(batch)
            if len(ballots_to_process) > 0 :
                start = perf_counter()
                asyncio.run(main(ballots_to_process))
                stop = perf_counter()
                print(f"time taken: {stop - start} to run a batch size: {len(ballots_to_process)}")
        end = perf_counter()
        print(f"TOTAL time taken: {end - begin}")

