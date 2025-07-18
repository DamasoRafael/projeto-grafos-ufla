# dijkstra.py
# OBJETIVO: Este arquivo contém a implementação do algoritmo clássico de Dijkstra.
# Ele é o motor para encontrar o caminho mais curto entre dois pontos no nosso mapa (grafo).

import heapq  # Usamos heapq para implementar a fila de prioridade, que é essencial para a eficiência do Dijkstra.
import math   # Usamos math.inf para representar uma distância infinita.

def dijkstra(num_vertices, adj_list, start_node):
    """
    Executa o algoritmo de Dijkstra a partir de um nó inicial para encontrar
    as distâncias mais curtas para todos os outros nós no grafo.

    Args:
        num_vertices (int): O número total de vértices no grafo.
        adj_list (dict): A lista de adjacência do grafo, onde adj_list[u] = [(v, custo), ...].
        start_node (int): O nó de onde o cálculo das distâncias deve começar.

    Returns:
        dict: Um dicionário mapeando cada nó à sua distância mais curta a partir do start_node.
    """
    # 1. INICIALIZAÇÃO
    # Criamos um dicionário para armazenar as distâncias.
    # Inicialmente, a distância para todos os nós é infinita (math.inf).
    dist = {i: math.inf for i in range(num_vertices + 1)}
    
    # A distância do nó inicial para ele mesmo é sempre 0.
    dist[start_node] = 0
    
    # A fila de prioridade (pq) armazena tuplas de (distância, nó).
    # Ela sempre nos dará o nó com a menor distância primeiro.
    # Começamos com o nó de partida.
    pq = [(0, start_node)]

    # 2. LOOP PRINCIPAL
    # O algoritmo continua enquanto houver nós na fila de prioridade para serem processados.
    while pq:
        # Pega o nó 'u' com a menor distância 'd' da fila. Esta é a escolha "gulosa".
        d, u = heapq.heappop(pq)

        # OTIMIZAÇÃO: Se a distância 'd' que pegamos da fila for maior que a distância
        # que já conhecemos para 'u', significa que já encontramos um caminho mais curto antes.
        # Então, simplesmente ignoramos e continuamos.
        if d > dist[u]:
            continue

        # 3. RELAXAMENTO (O CORAÇÃO DO ALGORITMO)
        # Para cada vizinho 'v' do nó 'u' que acabamos de pegar...
        if u in adj_list:
            for v, weight in adj_list[u]:
                # Verificamos se o caminho através de 'u' é mais curto do que o caminho que conhecíamos para 'v'.
                # Ou seja, se (distância até u) + (custo de u para v) < (distância atual até v)
                if dist[u] + weight < dist[v]:
                    # Se for, encontramos um caminho melhor!
                    # Atualizamos a distância de 'v'.
                    dist[v] = dist[u] + weight
                    # E adicionamos 'v' à fila de prioridade com sua nova distância menor.
                    heapq.heappush(pq, (dist[v], v))
    
    # Ao final, o dicionário 'dist' contém as menores distâncias de 'start_node' para todos os outros.
    return dist