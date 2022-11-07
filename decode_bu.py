from pathlib import Path
from collections import defaultdict
import json

import asn1tools as asn
import pandas as pd

from async_get_ballot_bu import get_state_ballot_codes, get_bu_file_name

BASE_DIR = Path(".").resolve()

bu_path = BASE_DIR / "bu"
ballot_metadata_path = BASE_DIR / "results_csv" / "ballot_metadata"
ballot_votes_path = BASE_DIR / "results_csv" / "ballot_votes"


BU_FILES = [ i.name for i in bu_path.iterdir() if i.suffix == '.bu']

asn1_paths = "./spec/bu.asn1"

conv = asn.compile_files(asn1_paths, codec="ber")

def decode_bu(file):
    with open( bu_path / file , 'rb') as fp:
            data = bytearray(fp.read())

    envelope_decoded = conv.decode("EntidadeEnvelopeGenerico", data)

    bu_encoded = envelope_decoded["conteudo"]

    bu_decoded = conv.decode("EntidadeBoletimUrna", bu_encoded)

    return bu_decoded


def process_results(results:dict, ballot_id:str, row_dict:defaultdict):
    for result in results:
        qty_apt_voters_ballot = result['qtdEleitoresAptos'] 
        votes = result['resultadosVotacao']
        if votes:
            for vote in votes:
                voters_voting = vote['qtdComparecimento']
                total_votes = vote['totaisVotosCargo']
                if total_votes:
                    for total_vote in total_votes:
                        _, position = total_vote['codigoCargo']
                        vote_counts = total_vote['votosVotaveis']
                        if vote_counts:
                            for vote_count in vote_counts:
                                vote_type = vote_count['tipoVoto']
                                qty = vote_count['quantidadeVotos']
                                if vote_type == 'nominal':
                                    party_code = vote_count['identificacaoVotavel']['partido']
                                    candidate_code = vote_count['identificacaoVotavel']['codigo']
                                    row_dict["ballot_id"].append(ballot_id)
                                    row_dict["position"].append(position)
                                    row_dict["vote_type"].append(vote_type)
                                    row_dict["party_code"].append(int(party_code))
                                    row_dict["candidate_code"].append(int(candidate_code))
                                    row_dict["qty_vote"].append(int(qty))
                                else:
                                    row_dict["ballot_id"].append(ballot_id)
                                    row_dict["position"].append(position)
                                    row_dict["vote_type"].append(vote_type)
                                    row_dict["party_code"].append(None)
                                    row_dict["candidate_code"].append(None)
                                    row_dict["qty_vote"].append(int(qty))
    
    return row_dict

def extract_ballot_results(bu_decoded:dict):
    return bu_decoded.get('resultadosVotacaoPorEleicao')

def extract_header(bu_decoded:dict, row_dict:defaultdict):
    creation_date = bu_decoded['cabecalho']['dataGeracao']
    row_dict["creation_date"].append(creation_date)
    return row_dict
    
def extract_ballot_info(bu_decoded:dict, row_dict:defaultdict):
    ballot = bu_decoded["urna"]
    ballot_load = ballot['correspondenciaResultado']['carga']
    # flat from here
    ballot_type = ballot['tipoUrna']
    ballot_number = ballot_load['numeroInternoUrna']
    ballot_serial_number = ballot_load['numeroSerieFC']
    ballot_load_datetime = ballot_load['dataHoraCarga']
    ballot_load_id = ballot_load['codigoCarga']
    row_dict["ballot_type"].append(ballot_type)
    row_dict["ballot_number"].append(ballot_number)
    row_dict["ballot_serial_number"].append(ballot_serial_number)
    row_dict["ballot_load_datetime"].append(ballot_load_datetime)
    row_dict["ballot_load_id"].append(ballot_load_id)
    return row_dict

def extract_section_data(bu_decoded:dict, row_dict:defaultdict):
    section = bu_decoded['identificacaoSecao']
    council_zone = section['municipioZona']
    # flat from here
    council_id = council_zone['municipio']
    zone_id = council_zone['zona']
    locality = section['local']
    section_number = section['secao']
    row_dict["council_id"].append(council_id)
    row_dict["zone_id"].append(zone_id)
    row_dict["locality"].append(locality)
    row_dict["section_number"].append(section_number)
    return row_dict

def extract_issue_date_time(bu_decoded:dict, row_dict:defaultdict):
    row_dict["issue_date_time"].append(bu_decoded['dataHoraEmissao'])
    return row_dict

def extract_ballot_voting_session(bu_decoded:dict, row_dict:defaultdict):
    _ , section_times = bu_decoded['dadosSecaoSA']
    opening_time =  section_times['dataHoraAbertura']
    closing_time =  section_times['dataHoraEncerramento']
    row_dict["opening_time"].append(opening_time)
    row_dict["closing_time"].append(closing_time)
    return row_dict

def extract_qty_voters_lib_code(bbu_decoded:dict, row_dict:defaultdict):
    row_dict["qty_voters_lib_code"].append(bu_decoded.get('qtdEleitoresLibCodigo'))
    return row_dict

def extract_qty_voters_biometric(bu_decoded:dict, row_dict:defaultdict):
    row_dict["qty_voters_biometric"].append(bu_decoded.get('qtdEleitoresCompBiometrico'))
    return row_dict


if __name__ == "__main__":
    with open("brazil-states.json", "r") as fp:
        states = json.load(fp)
        state_codes = [s for s in states.keys()]
    ballots_with_decoding_issues = []
    for state in state_codes:
        print(state)
        state_ballot_table_row_data = defaultdict(list)
        state_votes_table_row_data = defaultdict(list)
        st_ballots = get_state_ballot_codes(state)
        for ballot in st_ballots:
            file_name = get_bu_file_name(ballot)
            try:
                state_ballot_table_row_data["state_code"].append(state.upper())
                state_ballot_table_row_data["council_name"].append(ballot["mu_name"])
                state_ballot_table_row_data["file_name"].append(file_name)
                state_ballot_table_row_data["zone"].append(ballot["zone_cd"])
                state_ballot_table_row_data["section_cd"].append(ballot["section_cd"])
                ballot_id = file_name.split("-")[-1].split(".")[0]
                state_ballot_table_row_data["ballot_id"].append(ballot_id)

                bu_decoded = decode_bu(file_name)

                results = extract_ballot_results(bu_decoded)
                state_votes_table_row_data = process_results(results, ballot_id, state_votes_table_row_data)
            except Exception as err:
                print(err)
                ballots_with_decoding_issues.append(ballot)
    
        state_ballot_df = pd.DataFrame(state_ballot_table_row_data)
        state_ballot_df.to_csv(ballot_metadata_path / f"{state}_state_ballot_metadata.csv", index=False)
        state_votes_df = pd.DataFrame(state_votes_table_row_data)
        state_votes_df.to_csv(ballot_votes_path / f"{state}_state_votes_metadata.csv", index=False)

    with open("ballots_with_decoding_issues.json", "w+") as fp:
        json.dump(ballots_with_decoding_issues, fp)

    print(len(ballots_with_decoding_issues))