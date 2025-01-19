import matplotlib.pyplot as plt # Biblioteca responsável por criar as imagens do grafo
from matplotlib import pylab as pl # Biblioteca responsável por criar as imagens do grafo
import networkx as nx # Biblioteca responsavel por manipular o grafo
from networkx.drawing.layout import bipartite_layout
import copy
import os

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

"""
    COISAS À FAZER
    Tentar diminuir o tamanho dos vertices
    Diminuir a quantidade de imagens
    otimizar cria_gif() para rodar mais rapido
    Terminar de documentar o código
    Fazer o readme.md
    Verificar o que ainda falta
"""

def exclui_imagens(diretorio):
    try:
        # Se o diretorio não existe
        if not os.path.exists(diretorio):
            print(f"O diretório {diretorio} não existe.")
            return

        for arquivo in os.listdir(diretorio):
            caminho_arquivo = os.path.join(diretorio, arquivo)

            # Verifica se o arquivo existe
            if os.path.isfile(caminho_arquivo):
                nome, ext = os.path.splitext(arquivo)

                if ('.png' and ext.lower() == '.png'):
                    os.remove(caminho_arquivo)
    except Exception as e:
        print(f'Ocorreu o seguinte erro: {e}')

# Função que cria uma imagem PNG do emparelhento
def cria_imagem_emparelhemento(subgrafos, conj_vertices, repeticao):
    def fazer_imagens(grafo, destino, formato, cores):
        fig = plt.figure(figsize=(300, 300))
        pl.figure()
        nx.draw_networkx(grafo, pos=formato, with_labels=False, node_size=5, node_color=cores, edge_color='g')
        plt.savefig(destino, transparent=False, facecolor='w')
        plt.close()

    grafo = subgrafos[-1]
    pos = bipartite_layout(grafo, conj_vertices)  # Define a posição para desenhar na tela
    colors = ["lightblue" if i[0:1] == "P" else "red" for i in grafo.nodes]  # A cor do vertice do Projeto é Azul claro e a cor do aluno é vermelho
    fazer_imagens(grafo, f'./grafo_gerado/emparelhamento_{repeticao}.png', pos, colors)


def mostra_emparelhamento_terminal(listaEmparelhemento, qtdExecucoes):
    print(f" ---------------------EXECUÇÃO {qtdExecucoes}-------------------------------- ")
    print("Formato: {Projeto: Aluno Alocado -> Aluno desalocado\n")
    for projeto, conexoes in listaEmparelhemento.items():
        if conexoes[1] == '':
            print(f"{projeto}: {conexoes[0]}")
        else:
            print(f"{projeto}: {conexoes[0]} -> {conexoes[1]}")

    print('\n\n')

def emparelhamento(grafo, subconjunto):
    """
        Precisa-se de uma copia da lista de alunos pois as informações da lista de desejos de cada aluno será manipulada.
        Assim evitamos que as informações se percam para que possamos reutiliza-las no futuro.

        Depois vamos colocar os alunos em uma lista de candidatos que será usada para identificar se um aluno foi ou não alocado a um projeto.

    """
    copiaListaAlunos = copy.deepcopy(listaAlunos)
    listaCandidatos = [i for i in copiaListaAlunos.keys()]

    subgrafos = [grafo.copy()]

    # Lista de todas as interações
    listaEmparelhamentos = {i: [] for i in listaProjetos.keys()}

    """
        O Algoritmo a seguir segue a mesma logica que o algotimo de Gale-Shapley, só que com algumos modificações similares
        ao algoritmo de alocação Estudante-Projeto usado como referencia.
    """
    def algoritmo_Gale_Shapley():
        # Usaremos uma repescagem para fazer um novo emparelhamento no futuro
        repescagem = []

        """
        Resumo do algoritmo:
            * O Algoritmo rodará enquanto tiver alunos na lista de Candidatos;
            * Para cada aluno selecionado, verifica-se se ele ainda está na lista de candidatos e se ainda possui algum projeto em sua lista de desejos
            * No caso afirmativo, tentaremos fazer o emparelhamento similar ao que foi feito no algoritmo de alocação Estudante-Projeto
            * Caso contrario, entende-se que ou ele foi alocado ou ele não conseguiu ser alocado em nenhum projeto, então
                - Se ele não tiver sido alocado, ele vai para a lista de repescagem
                - Se tiver sido alocado, é feita a ligação no grafo para mostrar o emparelhemento na tela.
        """
        while len(listaCandidatos) > 0:
            aluno = listaCandidatos[0]

            while aluno in listaCandidatos and len(copiaListaAlunos[aluno][0]) > 0:
                projeto = copiaListaAlunos[aluno][0].pop(0)

                # Verifica se o aluno possui nota minima para conseguir o projeto
                if copiaListaAlunos[aluno][1] >= listaProjetos[projeto][1]:
                    # Verifica se o projeto já está cheio
                    if len(listaProjetos[projeto][2]) >= listaProjetos[projeto][0]:
                        ultimoAluno = listaProjetos[projeto][2][-1]
                        # Compara a nota do ultimo aluno alocado com o aluno que estamos tentando alocar
                        if copiaListaAlunos[ultimoAluno][1] < copiaListaAlunos[aluno][1]:
                            # Se a nota co aluno for maior que a do ultimo aluno, aloca o aluno e coloca o ultimo aluno na lista de candidatos
                            listaProjetos[projeto][2].remove(ultimoAluno)
                            listaProjetos[projeto][2].append(aluno)
                            listaCandidatos.remove(aluno)
                            listaCandidatos.append(ultimoAluno)


                            #cria aresta entre projeto e aluno
                            grafo.add_edge(projeto, aluno)
                            #remove aresta entre projeto e último aluno
                            grafo.remove_edge(projeto, ultimoAluno)
                            subgrafos.append(grafo.copy())

                            # Faz a troca dos alunos
                            listaEmparelhamentos[projeto].append([aluno, ultimoAluno])

                    # Se o projeto não estiver cheio, aloca ele no projeto
                    else:
                        listaProjetos[projeto][2].append(aluno)
                        listaCandidatos.remove(aluno)

                        # cria aresta entre projeto e aluno
                        grafo.add_edge(projeto, aluno)
                        subgrafos.append(grafo.copy())

                        # Adiciona aluno ao projeto
                        listaEmparelhamentos[projeto].append([aluno, ''])

            #Caso o aluno não tenha sido alocado e tenha acabado os seus projetos de interece, ele vai pra repescagem
            if len(copiaListaAlunos[aluno][0]) == 0 and aluno in listaCandidatos:
                listaCandidatos.remove(aluno)
                repescagem.append(aluno)

        return repescagem.copy()

    """
        Aqui segue uma logica muito parecida com a função algoritmo_Gale_Shapley,
        só que dessa vez, verifica-se qual o grau de interece do aluno pelo projeto em sua lista de desejos.
    """
    def emparelhamentoRepescagem(repescagem, candidatosRepescagem):
        # Lista que servir como repescagem no futuro
        repescagemIntermediaria = []

        # Enquanto a lista de repescagem tiver alunos, continua o algoritmo
        while len(repescagem) >0:
            aluno = repescagem.pop(0)
            """
                Neste caso, uma diferença do algoritmo_Gale_Shapley para esse é que não verifica mais se o aluno está na repescagem
                Agora, toda vez que houver uma torca de alunos em um projeto, o ultimo aluno se torna o aluno e
                a sua lista de interesses final do algoritmo_Gale_Shapley é passada para o candidatosRepescagem
            """
            while len(candidatosRepescagem[aluno][0]) > 0:
                projeto = candidatosRepescagem[aluno][0].pop(0)

                # Verifica se o aluno possui nota suficiente
                if candidatosRepescagem[aluno][1] >= listaProjetos[projeto][1]:
                    # Verifica se o projeto está cheio
                    if len(listaProjetos[projeto][2]) >= listaProjetos[projeto][0]:
                        ultimoAluno = listaProjetos[projeto][2][-1]
                        # Se o ultimo aluno tiver uma nota inferio a nota do aluno, é feita a troca
                        if listaAlunos[aluno][1] > listaAlunos[ultimoAluno][1]:
                            listaProjetos[projeto][2].remove(ultimoAluno)
                            listaProjetos[projeto][2].append(aluno)

                            # remove aresta entre projeto e último aluno
                            grafo.remove_edge(projeto, ultimoAluno)
                            # cria aresta entre projeto e aluno
                            grafo.add_edge(projeto, aluno)
                            subgrafos.append(grafo.copy())

                            # Adiciona o emparelhamento
                            listaEmparelhamentos[projeto].append([aluno, ultimoAluno])

                            # O ultimo aluno da lista do projeto, passa a ser o aluno que tentará outro projeto
                            aluno = ultimoAluno

                            """
                            Nota importante:
                                É interessante notar uma coisa, não é feita uma copia da lista de interesses do ultimo aluno,
                                ms sim é passado o endereço da lista de desejos.
                                Isso faz com que tanto candidatosRepescagem, quanto copiaListaAlunos consigam alterar seus valores.
                                Optei por fazer isso pois no próximo elif, é feita uma comparação das listas candidatosRepescagem e
                                copiaListaAlunos. Assim se um aluno for alocado em um projeto, e depois desalocado, a copiaListaAlunos
                                nao ficará com a versão antiga da candidatosRepescagem.
                            """
                            candidatosRepescagem[aluno] = copiaListaAlunos[aluno]

                        # Caso os alunos possuam notas iguais, é verificado quem tem mais interesse pelo projeto
                        elif listaAlunos[aluno][1] == listaAlunos[ultimoAluno][1]:
                            if len(candidatosRepescagem[aluno][0]) >= len(copiaListaAlunos[ultimoAluno][0]):
                                listaProjetos[projeto][2].remove(ultimoAluno)
                                listaProjetos[projeto][2].append(aluno)

                                # remove aresta entre projeto e último aluno
                                grafo.remove_edge(projeto, ultimoAluno)
                                # cria aresta entre projeto e aluno
                                grafo.add_edge(projeto, aluno)
                                subgrafos.append(grafo.copy())

                                #Adiciona o emparelhento
                                listaEmparelhamentos[projeto].append([aluno, ultimoAluno])

                                # O ultimo aluno da lista do projeto, passa a ser o aluno que tentará outro projeto
                                aluno = ultimoAluno

                                # Mesca coisa da nota do If anterior
                                candidatosRepescagem[aluno] = copiaListaAlunos[aluno]

                    # Caso o projeto não esteja cheio, o aluno é alocado
                    else:
                        listaProjetos[projeto][2].append(aluno)

                        # cria aresta entre projeto e aluno
                        grafo.add_edge(projeto, aluno)
                        subgrafos.append(grafo.copy())

                        listaEmparelhamentos[projeto].append([aluno, ''])

                        break

            # Se o aluno não tiver mais projetos de interesse, ele passa para a repescagem
            if len(candidatosRepescagem[aluno][0]) == 0:
                repescagemIntermediaria.append(aluno)

        return repescagemIntermediaria.copy()

    # Chamada das funções
    repescagem = algoritmo_Gale_Shapley()

    # Mostra no terminal quais foram os emparelhentos
    mostra_emparelhamento_terminal(listaEmparelhamentos, 1)

    # Cria uma imagem do emparelhento no diretorio ./grafo-gerado
    cria_imagem_emparelhemento(subgrafos, subconjunto, 1)

    for i in range(2,11):
        candidatosRepescagem = {i: copy.deepcopy(listaAlunos[i]) for i in repescagem}

        repescagem = emparelhamentoRepescagem(repescagem, copy.deepcopy(candidatosRepescagem))

        # Mostra no terminal quais foram os emparelhentos
        mostra_emparelhamento_terminal(listaEmparelhamentos, 1)

        # Cria uma imagem do emparelhento no diretorio ./grafo-gerado
        cria_imagem_emparelhemento(subgrafos, subconjunto, i)

"""

    Codigo principal

"""
# Primeiro, precisamos realizar uma leitura do arquivo e manipular os dados antes de utiliza-los
le_entradas()
# Então, com os dados organizados, vamos criar um grafo bipartido para poder mostrar como ficou o emparelhamento
grafo = cria_grafo_bipartido()
# Então, realizamos o emparelhamento do grafo
projetos = [x for x in listaProjetos.keys()]
emparelhamento(grafo, projetos)


