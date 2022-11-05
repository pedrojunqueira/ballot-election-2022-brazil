from pathlib import Path
import json

import asn1tools as asn

BASE_DIR = Path(".").resolve()

bu_path = BASE_DIR / "bu"

BU_FILES = [ i.name for i in bu_path.iterdir() if i.suffix == '.bu']

print(type(BU_FILES[0]))

asn1_paths = "./spec/bu.asn1"

conv = asn.compile_files(asn1_paths, codec="ber")

counter = 0

for file in BU_FILES:
    try:
        with open(f"./bu/{file}", 'rb') as fp:
            data = bytearray(fp.read())

        envelope_decoded = conv.decode("EntidadeEnvelopeGenerico", data)

        bu_encoded = envelope_decoded["conteudo"]

        bu_decoded = conv.decode("EntidadeBoletimUrna", bu_encoded)

        # print(bu_decoded)
        results = bu_decoded.get('resultadosVotacaoPorEleicao')
        if results:
            for result in results:
                print(f"registered voters {result['qtdEleitoresAptos']}")
                votes = result['resultadosVotacao']
                if votes:
                    for vote in votes:
                        print(f"voters voting: {vote['qtdComparecimento']}")
                        total_votes = vote['totaisVotosCargo']
                        if total_votes:
                            for total_vote in total_votes:
                                _, position = total_vote['codigoCargo']
                                print(f"result for: {position}")
                                vote_counts = total_vote['votosVotaveis']
                                if vote_counts:
                                    for vote_count in vote_counts:
                                        vote_type = vote_count['tipoVoto']
                                        qty = vote_count['quantidadeVotos']
                                        if vote_type == 'nominal':
                                            candidate_code = vote_count['identificacaoVotavel']['codigo']
                                            print(f"candidate: {candidate_code} got {qty} votes ")
                                        else:
                                            print(f"{vote_type} got {qty} votes ")
                    print()






    except Exception as e:
        counter +=1
        print(file)
        print(e)
print(counter)
