Solver para o Problema de Roteamento de Arcos Capacitado (CARP)
Visão Geral
Este projeto, desenvolvido para a disciplina de Algoritmos em Grafos (GCC218) da Universidade Federal de Lavras (UFLA), apresenta uma solução completa em Python para o Problema de Roteamento de Arcos Capacitado (CARP). O objetivo é encontrar um conjunto de rotas de custo mínimo para uma frota de veículos, atendendo a um conjunto de tarefas (em nós, arestas e arcos) com demandas específicas, sem exceder a capacidade dos veículos.

A solução é implementada em duas fases principais:

Heurística Construtiva: Geração de uma solução inicial viável utilizando um algoritmo guloso de inserção mais barata.

Otimização por Busca Local: Refinamento da solução inicial através de uma meta-heurística Variable Neighborhood Descent (VND) para reduzir o custo total.

🚀 Metodologia Implementada
Arquitetura
A solução utiliza uma abordagem otimizada para o cálculo de distâncias, empregando o Algoritmo de Dijkstra sob demanda com um sistema de cache. Isso evita o custo computacional de um pré-cálculo completo com Floyd-Warshall, tornando a execução mais eficiente, especialmente durante a fase de busca local.

Fase 1: Heurística Construtiva (construtivo.py)
A solução inicial é gerada por uma heurística de inserção mais barata. O algoritmo constrói cada rota iterativamente, sempre selecionando o serviço não atendido que pode ser adicionado à rota atual com o menor custo marginal de inserção, respeitando a capacidade do veículo.

Fase 2: Otimização com VND (melhoria.py)
Para otimizar a solução inicial, foi implementada a meta-heurística Variable Neighborhood Descent (VND). O VND explora sistematicamente um conjunto de estruturas de vizinhança para encontrar melhorias. O processo é reiniciado a partir da primeira vizinhança sempre que uma melhoria é encontrada, parando apenas quando nenhum movimento em nenhuma das vizinhanças consegue mais reduzir o custo.

Os movimentos de vizinhança implementados são:

Relocate (Inter-rotas): Move um serviço de uma rota para outra.

Swap (Inter-rotas): Troca um serviço de uma rota por um serviço de outra.

2-Opt (Intra-rota): Otimiza a sequência de serviços dentro de uma única rota, removendo cruzamentos.

📂 Estrutura do Projeto
solver-carp-ufla/
│
├── Ins/
│   ├── BHW1.dat
│   └── ... (outras 408 instâncias)
│
├── SolucoesFinais/
│   ├── sol-BHW1.dat
│   └── ... (soluções geradas)
│
├── construtivo.py      # Heurística construtiva (Fase 2)
├── dijkstra.py         # Implementação do Algoritmo de Dijkstra
├── grafo.py            # Classe Grafo e funções de custo
├── leitura.py          # Parser para os arquivos de instância
├── melhoria.py         # Algoritmos de otimização VND (Fase 3)
├── rodar_todas.py      # Script principal para executar o pipeline
├── README.md           # Este arquivo
└── ... (outros arquivos de teste)

▶️ Como Executar
Pré-requisitos:

Python 3.8 ou superior.

Verifique se a pasta Ins/ contém todos os arquivos .dat das instâncias.

Execução Completa:
Para executar o pipeline completo (construtivo + melhoria) para todas as instâncias, execute o seguinte comando no terminal, na pasta raiz do projeto:

python rodar_todas.py

O script irá processar todas as instâncias e salvar os arquivos de solução na pasta SolucoesFinais/. Ele automaticamente ignora as instâncias que já foram processadas, permitindo continuar a execução de onde parou.

🧑‍💻 Autores
João Vitor Givisiez Lessa

Rafael Rabelo Pereira Damaso
