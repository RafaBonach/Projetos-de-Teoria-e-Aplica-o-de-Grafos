import networkx as nx


# Primeiro, precisamos ler os arquivos e armazena-los em um vetor
listaProjetos = []
projeto = []
arq = open('ListaProjetos.txt', 'r')
for linha in arq:
    linha = linha.strip()
    linha = linha.strip('()')
    linha = linha.replace(',', '')
    linha = linha.split(' ')

    listaProjetos.append(linha)
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
grafo = nx.DiGraph()
for noProjeto in listaProjetos:
    grafo.add_node(noProjeto[0])

for noAluno in listaAlunos.keys():
    grafo.add_node(noAluno)
#print(grafo)
