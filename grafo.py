# grafo.py
# OBJETIVO: Representar o mapa do problema como uma estrutura de dados de Grafo
# e fornecer uma maneira eficiente de calcular distâncias entre os pontos,
# usando o algoritmo de Dijkstra e uma otimização de cache.

import math
from dijkstra import dijkstra # Importamos nossa implementação do Dijkstra.

class Grafo:
    """
    Esta classe encapsula a representação do grafo e gerencia o cálculo de distâncias.
    A principal funcionalidade é o cache de distâncias para evitar recálculos desnecessários.
    """
    def __init__(self, dados):
        """
        O construtor da classe. Ele pega os dados lidos do arquivo de instância
        e constrói a estrutura do grafo (uma lista de adjacência).
        """
        n_header = dados["num_vertices"]
        self.n = n_header
        
        max_node_in_conns = 0
        if dados["conexoes"]:
            max_node_in_conns = max(max(u, v) for u, v, _, _ in dados["conexoes"])
        
        self.n = max(self.n, max_node_in_conns)
        
        # A lista de adjacência 'adj' é um dicionário onde a chave é um nó
        # e o valor é uma lista de tuplas (vizinho, custo).
        self.adj = {} 
        for u, v, custo, tipo in dados["conexoes"]:
            if u not in self.adj: self.adj[u] = []
            if v not in self.adj: self.adj[v] = []
            
            self.adj[u].append((v, custo))
            # Para arestas (não direcionadas), a conexão existe nos dois sentidos.
            if tipo in ("NE", "E"):
                self.adj[v].append((u, custo))
        
        # OTIMIZAÇÃO: Mecanismo de cache para evitar recalcular Dijkstra.
        # Chave: nó de origem. Valor: dicionário de distâncias a partir dessa origem.
        # Isso acelera drasticamente o algoritmo, pois muitas vezes precisamos
        # das distâncias a partir do mesmo ponto várias vezes.
        self.cache_distancias = {}

    def obter_distancias(self, no_origem):
        """
        Retorna um dicionário com as distâncias de 'no_origem' para todos os outros nós.
        Esta função é o ponto central de consulta de distâncias.
        """
        # 1. VERIFICA O CACHE
        # Se já calculamos as distâncias para este 'no_origem' antes,
        # simplesmente retornamos o resultado armazenado.
        if no_origem in self.cache_distancias:
            return self.cache_distancias[no_origem]
        
        # 2. CALCULA (SE NÃO ESTIVER NO CACHE)
        # Caso contrário, chamamos o algoritmo de Dijkstra para fazer o cálculo.
        distancias = dijkstra(self.n, self.adj, no_origem)
        
        # 3. ARMAZENA NO CACHE
        # Guardamos o resultado no cache para que, na próxima vez, a resposta seja instantânea.
        self.cache_distancias[no_origem] = distancias
        return distancias

def calcular_custo_rota(sequencia_servicos, grafo, deposito):
    """
    Calcula o custo total de uma rota específica. Uma rota é uma sequência de serviços.
    """
    if not sequencia_servicos:
        return 0.0

    custo_total = 0.0
    pos_atual = deposito # A rota sempre começa no depósito.

    # Itera sobre cada serviço na sequência da rota.
    for servico in sequencia_servicos:
        _, p1, p2, _, s_custo, t_custo = servico # Desempacota as informações do serviço.
        
        # Pega as distâncias do ponto atual para todos os outros.
        distancias_do_ponto_atual = grafo.obter_distancias(pos_atual)
        # O custo de viagem é o caminho mais curto de 'pos_atual' até 'p1' (início do serviço).
        custo_viagem = distancias_do_ponto_atual.get(p1, math.inf)

        if custo_viagem == math.inf: return math.inf # Se for inf, a rota é inviável.

        # Acumula os custos: custo da viagem + custo de travessia do serviço + custo de serviço.
        custo_total += custo_viagem
        custo_total += t_custo
        custo_total += s_custo
        
        # Atualiza a posição atual do veículo para o final do serviço ('p2').
        pos_atual = p2

    # Após o último serviço, calcula o custo de volta para o depósito.
    distancias_finais = grafo.obter_distancias(pos_atual)
    custo_volta = distancias_finais.get(deposito, math.inf)

    if custo_volta == math.inf: return math.inf

    custo_total += custo_volta
    return custo_total