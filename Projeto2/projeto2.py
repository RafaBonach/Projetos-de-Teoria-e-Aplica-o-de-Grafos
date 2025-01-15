import networkx as nx
import copy

# Primeiro, precisamos ler os arquivos e armazena-los em um vetor
listaProjetos = {}
arq = open('ListaProjetos.txt', 'r')
for linha in arq:
    linha = linha.strip()
    linha = linha.strip('()')
    linha = linha.replace(',', '')
    linha = linha.split(' ')
    listaProjetos[linha[0]] = [int(linha[1]), int(linha[2]), []]

    #print(linha)
arq.close()

listaAlunos = {}

arq = open('ListaAlunos.txt', 'r')
for linha in arq:
    linha = linha.strip()
    linha = linha.split(':')
    indice = linha[0].strip('()')

    linha[1] = linha[1].split(') ')
    interece = linha[1][0]
    interece = interece.strip('()')
    interece = interece.replace(',', '')
    interece = interece.split(' ')
    nota = linha[1][1]
    nota = int(nota.strip('()'))

    listaAlunos[indice] = [interece, nota]
    # print(indice, listaAlunos[indice])
arq.close()

# Agora, vamos criar um digrafo apenas com vertices com base nos dois vetores criados
"""
grafo = nx.DiGraph()
for noProjeto in listaProjetos:
    grafo.add_node(noProjeto[0])

for noAluno in listaAlunos.keys():
    grafo.add_node(noAluno)

#print(grafo)
"""

# Vamos agora fazer o emparelhamento estável

listaCandidatos = []
repescagem = []
candidatosRepescagem = {}
listaEmparelhamentos = {}
copiaListaAlunos = copy.deepcopy(listaAlunos);

for i in copiaListaAlunos.keys():
    listaCandidatos.append(i)
for i in copiaListaAlunos.keys():
    listaEmparelhamentos[i] = []
#print("Aluno  Projeto")
while len(listaCandidatos) > 0:
    aluno = listaCandidatos[0]

    while aluno in listaCandidatos and len(copiaListaAlunos[aluno][0]) > 0:
        projeto = copiaListaAlunos[aluno][0].pop(0)
        if copiaListaAlunos[aluno][1] >= listaProjetos[projeto][1]:
            if len(listaProjetos[projeto][2]) >= listaProjetos[projeto][0]:
                ultimoAluno = listaProjetos[projeto][2][-1]
                if copiaListaAlunos[ultimoAluno][1] < copiaListaAlunos[aluno][1]:
                    listaProjetos[projeto][2].remove(ultimoAluno)
                    listaProjetos[projeto][2].append(aluno)
                    listaCandidatos.remove(aluno)
                    listaCandidatos.append(ultimoAluno)

                    #listaEmparelhamentos[projeto].append(f'{projeto} X {ultimoAluno} -> {aluno}')
                    """
                    print(f'{aluno}: {listaAlunos[aluno][1]} - {projeto}: {listaProjetos[projeto][1]}')
                    print(f'{aluno}: {listaAlunos[aluno][1]} VS {piorAluno}: {listaAlunos[piorAluno][1]}')
                    print(listaProjetos[projeto][2], "\n")
                    
                else:
                    print(f'{aluno}: {listaAlunos[aluno][1]} X {projeto}: {listaProjetos[projeto][1]}')
                    print("COMPETIÇÃO")
                    print(f'{aluno}: {listaAlunos[aluno][1]} VS {piorAluno}: {listaAlunos[piorAluno][1]}')
                    print(listaProjetos[projeto][2], "\n")
                    """

            else:
                listaProjetos[projeto][2].append(aluno)
                listaCandidatos.remove(aluno)
                #listaEmparelhamentos[projeto].append(f'{projeto} -> {aluno}')
                """
                print(f'{aluno}: {listaAlunos[aluno][1]} - {projeto}: {listaProjetos[projeto][1]}')
                print(listaProjetos[projeto][2], "\n")
                """

        else:
            """print(f'{aluno}: {listaAlunos[aluno][1]} X {projeto}: {listaProjetos[projeto][1]}')
            """
            #print(listaProjetos[projeto][2], "\n")

    if len(copiaListaAlunos[aluno][0]) == 0 and aluno in listaCandidatos:
        listaCandidatos.remove(aluno)
        repescagem.append(aluno)

listaIntermediaria = []
for i in range(8):
    repescagem.sort()
    for j in repescagem:
        candidatosRepescagem[j] = copy.deepcopy(listaAlunos[j]);

    while len(repescagem) >0:
        aluno = repescagem.pop(0)

        while len(candidatosRepescagem[aluno][0]) > 0:
            projeto = candidatosRepescagem[aluno][0].pop(0)

            if candidatosRepescagem[aluno][1] >= listaProjetos[projeto][1]:
                if len(listaProjetos[projeto][2]) >= listaProjetos[projeto][0]:
                    ultimoAluno = listaProjetos[projeto][2][-1]
                    if listaAlunos[aluno][1] > listaAlunos[ultimoAluno][1]:
                        listaProjetos[projeto][2].remove(ultimoAluno)
                        listaProjetos[projeto][2].append(aluno)
                        aluno = ultimoAluno
                        candidatosRepescagem[aluno] = copiaListaAlunos[aluno]

                    elif listaAlunos[aluno][1] == listaAlunos[ultimoAluno][1]:
                        if len(candidatosRepescagem[aluno][0]) >= len(copiaListaAlunos[ultimoAluno][0]):
                            listaProjetos[projeto][2].remove(ultimoAluno)
                            listaProjetos[projeto][2].append(aluno)
                            aluno = ultimoAluno
                            candidatosRepescagem[aluno] = copiaListaAlunos[aluno]

                else:
                    listaProjetos[projeto][2].append(aluno)
                    break

        if len(candidatosRepescagem[aluno][0]) == 0:
            listaIntermediaria.append(aluno)

    repescagem = copy.deepcopy(listaIntermediaria)

j = 0
for i in listaProjetos.keys():
    if len(listaProjetos[i][2]) == 0:
        j += 1
        print(i, '\n')
    """if len(listaProjetos[i][2]) < listaProjetos[i][0] :
        j += 1
        print(i, '\n')"""

print(j)