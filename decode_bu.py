
import asn1tools as asn

asn1_paths = "./spec/bu.asn1"

conv = asn.compile_files(asn1_paths, codec="ber")

with open("./bu/o00407-2949100010735.bu", 'rb') as fp:
    data = bytearray(fp.read())

envelope_decoded = conv.decode("EntidadeEnvelopeGenerico", data)

bu_encoded = envelope_decoded["conteudo"]

bu_decoded = conv.decode("EntidadeBoletimUrna", bu_encoded)

print(bu_decoded)

# # print(bu_decoded.keys())

# print("cabecalho:", bu_decoded['cabecalho'])
# print()
# print("fase:" , bu_decoded['fase'])
# print()
# print("tipo urna:", bu_decoded['urna'].get('tipoUrna'))
# print()
# print("identificacao secao:", bu_decoded['identificacaoSecao'])
# print()
# print("horario emissao:", bu_decoded['dataHoraEmissao'])
# print()
# print("dados secao:" , bu_decoded['dadosSecaoSA'])
# print()
# print("quantidade eleitores:",bu_decoded['qtdEleitoresLibCodigo'])
# print()
# print("qtd eleitores biometricos:", bu_decoded['qtdEleitoresCompBiometrico'])
# print()
# results =  bu_decoded['resultadosVotacaoPorEleicao']

# for result in results:
#     print(f'qtdEleitoresAptos: {result["qtdEleitoresAptos"]}')
#     vote_result = result['resultadosVotacao']
#     for v in vote_result:
#         # print(v)
#         print(f'tipoCargo: {v["tipoCargo"]}')
#         print(f'qtdComparecimento: {v["qtdComparecimento"]}')
#         votos_cargo = v['totaisVotosCargo'][0]
#         _ , cargo  = votos_cargo["codigoCargo"]
#         print(cargo)
#         print()
#         votes = votos_cargo["votosVotaveis"]
#         for vote in votes:
#             print(f'tipo Voto: {vote["tipoVoto"]}')
#             print(f'quantidadeVotos: {vote["quantidadeVotos"]}')
#             print(f'identificacaoVotavel {vote.get("identificacaoVotavel")}')
#             print()


# print(bu_decoded['chaveAssinaturaVotosVotavel'])

