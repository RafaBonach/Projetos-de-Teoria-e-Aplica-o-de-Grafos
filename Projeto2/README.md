# Projeto 2 de Teoria de Grafos e Aplicação


---


##### Por Rafael Oliveira Bonach, 221008365
###### Universidade de Brasília
###### Departamento de Ciência da Computação


Este projeto trata-se de um sistema de alocação de alunos a projetos. A ideia consiste em, dado um conjunto de alunos, sendo que cada aluno possui uma preferência de trabalhos e uma nota, e de trabalhos, que possui uma quantidade de vagas e uma nota pré-requisito, elabore um emparelhamento estável máximo e impessoal entre os alunos e os trabalhos.


Os dados de trabalhos e projetos a serem lidos foram disponibilizados na plataforma moodle pelo professor, ao qual encontra-se neste diretório com o nome de [entradaProj2.24TAG.txt](./entradaProj2.24TAG.txt).


Segue algumas informações sobre o projeto:
O projeto contém **2 readme** que possuem as **mesmas informações**,  **dois arquivos python**, **um arquivo txt** e **três pastas**.


Os arquivos python, apesar de possuírem informações parecidas, são diferentes em um quesito:
* O arquivo [projeto2.py](projeto2.py), foi o primeiro projeto feito, contudo, observa-se que pela quantidade de imagens que tiveram de ser compiladas para fazer o GIF das alocações, gerou-se um tempo exorbitante de execução, aproximadamente 7 minutos de execução. Levando isso em conta, optei por deixar os gifs já gerados na pasta [gif-dos-emparelhamentos](gif-dos-emparelhamentos) e deixar o projeto disponível para caso deseje analisá-lo.
* O arquivo [projeto2Executavel.py](projeto2Executavel.py), é o arquivo principal que cria apenas os grafos já alocados e os armazena em [grafo_gerado](grafo_gerado), além de que ele compila no terminal todos os emparelhamentos feitos. A maior diferença do primeiro arquivo para o segundo, está na forma como implementei a função que cria um gif dos grafos, sendo que neste segundo ele só cria as imagens resultantes do emparelhamento.


Para realizar a devida compilação do projeto, é necessário que seja instalada as bibliotecas
* [scipy](https://scipy.org/)
* [networkx](https://networkx.org/)
* [copy](https://docs.python.org/pt-br/3/library/copy.html)
* [os](https://docs.python.org/pt-br/3/library/os.html)


Ambos os códigos estão devidamente comentados, modularizados(divididos em funções específicas) e bem explicados. Para a correta compilação do código, é necessária a existência das **pastas [_grafo_gerado_](grafo_gerado), [_gif-dos-emparelhamentos_](gif-dos-emparelhamentos) e [_temporary_imgs_](temporary_imgs)**.


Ao ser executado, o código irá rodar as funções pré-estabelecidas, fazendo automaticamente a coleta das informações relevantes no arquivo txt, a criação do grafo, o processo de emparelhamento estável máximo e o plot das imagens e gifs em suas respectivas pastas.


### Créditos
> [Abraham, Irving & Manlove. Two algorithms for the Student-Project Allocation problem, 2007)](https://www.sciencedirect.com/science/article/pii/S1570866706000207)
>
> [Rossi, Ryan A; Ahmed, Nesreen K. The Network Data Repository with Interactive Graph Analytics and Visualization. Network Repository, 2015](http://networkrepository.com)
>
> [McNulty, Keith. Handbook of Graphs and Networks in People Analytics. CRC Press](https://ona-book.org/index.html)

