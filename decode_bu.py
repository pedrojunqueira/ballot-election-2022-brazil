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
                    print()






    except Exception as e:
        counter +=1
        print(file)
        print(e)

# ['cabecalho', 
# 'fase', 
# 'urna', 
# 'identificacaoSecao', 
# 'dataHoraEmissao', 
# 'dadosSecaoSA', 
# 'resultadosVotacaoPorEleicao', 
# 'chaveAssinaturaVotosVotavel']

# {'cabecalho': {'dataGeracao': '20221030T170437', 'idEleitoral': ('idPleito', 407)}, 
# 'fase': 'oficial', 
# 'urna': {'tipoUrna': 'secao', 'versaoVotacao': '8.26.0.0 - Onça-pintada', 'correspondenciaResultado': {'identificacao': ('identificacaoSecaoEleitoral', {'municipioZona': {'municipio': 29530, 'zona': 1}, 'local': 1, 'secao': 84}), 
#                 'carga': {'numeroInternoUrna': 1050840, 'numeroSerieFC': b'\xee\x85X\xcc', 'dataHoraCarga': '20220913T135500', 'codigoCarga': '572868572189728515131873'}}, 'tipoArquivo': 'votacaoUE', 'numeroSerieFV': b'\xe2K\x04"'}, 
# 'identificacaoSecao': {'municipioZona': {'municipio': 29530, 'zona': 1}, 'local': 1015, 'secao': 84}, 
# 'dataHoraEmissao': '20221030T170351', 
# 'dadosSecaoSA': ('dadosSecao', {'dataHoraAbertura': '20221030T080001', 'dataHoraEncerramento': '20221030T170050'}), 
# 'resultadosVotacaoPorEleicao': [{'idEleicao': 545, 'qtdEleitoresAptos': 305, 'resultadosVotacao': 
#     [{'tipoCargo': 'majoritario', 'qtdComparecimento': 171, 'totaisVotosCargo': 
#         [{'codigoCargo': ('cargoConstitucional', 'presidente'), 'ordemImpressao': 1, 'votosVotaveis': 
#                                                                                             [{'tipoVoto': 'nominal', 'quantidadeVotos': 100, 'identificacaoVotavel': {'partido': 13, 'codigo': 13}, 'assinatura': b'U\xac\xdf\xac\xa5\x00N!$\x0c\x92^P\x05\xfb\xf7&\x1d1\xad\x90s\x89b\x00\x05CR`ubl\xa0G\xa0\x80\xfd\xcf0\xbe\xf7\xe4\x8cC\xfc\x90\x1emC\xffsu\xb1&d9Cr|\x81|\xc2m\n'}, {'tipoVoto': 'nominal', 'quantidadeVotos': 62, 'identificacaoVotavel': {'partido': 22, 'codigo': 22}, 'assinatura': b'\xee\xf2D\xfb=\x00s\xf4<r\xe8=M\xb0\x8b\xc42\x9a\xabZ\xc8.\x80\xec\xdd\xc8\xb4#c\x86\xb0R\xd5\xf3\\\x97t\xca\x19\xa3\xb9\xd0+)\x19\x13\xf5T\xfeP\xa6\xb3\xed\xecAg\xb7b]\xc1\xb9D\xea\x03'}, {'tipoVoto': 'branco', 'quantidadeVotos': 1, 'assinatura': b"#\x1a\xf3\x92Y\xa1\xfa0\xfa?L}\xfb\x97\r\xdd\xb6\xc7\xae%\xdc\x14w\x81\xe0wT>\x8f\xd3\xc6\xe3~\xbc*\xcf\xdc\x01XP'*\x97t\xfc\xf4\x8cA:\xde\x02\x97;\xc0\xcaO\r\xef\xe0\xb5z\x9b\xff\t"}, {'tipoVoto': 'nulo', 'quantidadeVotos': 8, 'assinatura': b't]\x0b\xe4\x84\xa1\xf7(`\xb8\xc0K\xc2\xc5M{\xf1\xea\xf9\xd4\xc7\x18\xfe$N\xc4~^I\x9d\x7f\x9f\x83`:(\\h\x97@\xa9\x87\xf1\x88\xac\x8d\x0f?\xef5\xb5\xa0\x0b1\t\xbc\xcc\x92\x0b\x9c(0u\x07'}]}]}]}], 
# 'chaveAssinaturaVotosVotavel': b'o\xc3yB\x05\x8a\x9dM\xd4\xfd\xe0\xb3U\x95\xd7>$3\xe0\x11R\xbd\x07\xbf\xd0\xa7\xc5l\xedl\x1a\xf3'}

print(counter)
