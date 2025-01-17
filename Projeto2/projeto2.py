import matplotlib.pyplot as plt # Biblioteca responsável por criar as imagens do grafo
from matplotlib import pylab as pl # Biblioteca responsável por criar as imagens do grafo
import imageio # Biblioteca responsavel por fazer o gif do grafo.
import networkx as nx # Biblioteca responsavel por manipular o grafo
from networkx.drawing.layout import bipartite_layout
import copy

# Para facilitar a manipulação, vamos deixar as listas como variaveis Globais.
listaAlunos = {}
listaProjetos = {}

def le_entradas():
    # Abre o arquivo para leitura
    with open('entradaProj2.24TAG.txt', 'r') as arquivo:
        # Lê linha a linha do arquivo
        for linha in arquivo:
            # Verifica se é a linha de leitura
            if linha[0:1] == '(':
                # Se for um Projeto, processa ele e armazena no dicionario listaProjetos
                if linha[1:2] == 'P':
                    # Remove espaços no inicio e fim da linha
                    linha = linha.strip()
                    # Remove () no inicio e fim da linha
                    linha = linha.strip('()')
                    # Troca , por ''
                    linha = linha.replace(',', '')
                    # Separa os valores
                    linha = linha.split(' ')
                    # Incrementa os valores no dicionario junto com uma lista de integrantes do projeto
                    listaProjetos[linha[0]] = [int(linha[1]), int(linha[2]), []]

                # Se for um aluno, processa ele e armazena no dicionario listaAlunos
                elif linha[1:2] == 'A':
                    # Remove espaços no inicio e fim da linha
                    linha = linha.strip()
                    # Separa as informações da linha
                    nome, informacoes = linha.split(':')
                    # Remove () no inicio e fim da linha
                    nome = nome.strip('()')

                    informacoes = informacoes.strip('()')
                    # Separa as informações pelo ) já que possuem informações que não são separadas por espaço, como é o caso do aluno 177
                    interece, nota = informacoes.split(')')
                    # Troca , por ''
                    interece = interece.replace(',', '')
                    # separa as informações
                    interece = interece.split(' ')

                    # Remove espaços no inicio e fim da linha
                    nota = nota.strip()
                    # Remove () no inicio e fim da linha
                    nota = nota.strip('()')
                    # Transforma em int
                    nota = int(nota)

                    # Incrementa os valores no dicionario
                    listaAlunos[nome] = [interece, nota]

def cria_grafo_bipartido():
    grafo = nx.DiGraph()
    projetos = [x for x in listaProjetos.keys()]
    alunos = [x for x in listaAlunos.keys()]
    grafo.add_nodes_from(projetos, bipartite=0)
    grafo.add_nodes_from(alunos, bipartite=2)

    #pos = bipartite_layout(grafo, projetos) # Define a posição para caso queira desenhar na tela
    return grafo

def emparelhamento(grafo):
    copiaListaAlunos = copy.deepcopy(listaAlunos);
    listaCandidatos = [i for i in copiaListaAlunos.keys()]
    listaEmparelhamentos = {i:j for i, j in copiaListaAlunos.items()}



    def algoritmo_Gale_Shapley():
        repescagem = []

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

                            #cria aresta entre projeto e aluno
                            grafo.add_edge(projeto, aluno)
                            #remove aresta entre projeto e último aluno
                            grafo.remove_edge(projeto, ultimoAluno)

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

                        # cria aresta entre projeto e aluno
                        grafo.add_edge(projeto, aluno)


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

        return repescagem.copy()

    def emparelhamentoRepescagem(repescagem, candidatosRepescagem):
        listaIntermediaria = []
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

                            # remove aresta entre projeto e último aluno
                            grafo.remove_edge(projeto, ultimoAluno)
                            # cria aresta entre projeto e aluno
                            grafo.add_edge(projeto, aluno)

                            # O ultimo aluno da lista do projeto, passa a ser o aluno que tentará outro projeto
                            aluno = ultimoAluno
                            # A lista de repescagem recebe os projetos que o aluno ainda não tentou
                            candidatosRepescagem[aluno] = copiaListaAlunos[aluno]

                        elif listaAlunos[aluno][1] == listaAlunos[ultimoAluno][1]:
                            if len(candidatosRepescagem[aluno][0]) >= len(copiaListaAlunos[ultimoAluno][0]):
                                listaProjetos[projeto][2].remove(ultimoAluno)
                                listaProjetos[projeto][2].append(aluno)

                                # remove aresta entre projeto e último aluno
                                grafo.remove_edge(projeto, ultimoAluno)
                                # cria aresta entre projeto e aluno
                                grafo.add_edge(projeto, aluno)

                                # O ultimo aluno da lista do projeto, passa a ser o aluno que tentará outro projeto
                                aluno = ultimoAluno
                                # A lista de repescagem recebe os projetos que o aluno ainda não tentou
                                candidatosRepescagem[aluno] = copiaListaAlunos[aluno]

                    else:
                        listaProjetos[projeto][2].append(aluno)

                        # cria aresta entre projeto e aluno
                        grafo.add_edge(projeto, aluno)

                        break

            if len(candidatosRepescagem[aluno][0]) == 0:
                listaIntermediaria.append(aluno)

        return listaIntermediaria.copy()

    repescagem = algoritmo_Gale_Shapley()

    for i in range(9):
        candidatosRepescagem = {i: copy.deepcopy(listaAlunos[i]) for i in repescagem}
        repescagem = emparelhamentoRepescagem(repescagem, copy.deepcopy(candidatosRepescagem))

    return grafo

# Primeiro, precisamos realizar uma leitura do arquivo e manipular os dados antes de utiliza-los
le_entradas()
# Então, com os dados organizados, vamos criar um grafo bipartido para poder mostrar como ficou o emparelhamento
grafo = cria_grafo_bipartido()
# Então, realizamos o emparelhamento do grafo.
grafo = emparelhamento(grafo)

