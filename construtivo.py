# construtivo.py
# OBJETIVO: Implementar a heurística construtiva, que é o primeiro passo para
# resolver o problema. Ela gera uma solução inicial que é viável (respeita
# todas as regras), mas não necessariamente ótima.

import math
from grafo import Grafo, calcular_custo_rota

def gerar_solucao_viavel(dados):
    """
    Constrói uma solução inicial usando uma heurística de inserção gulosa (greedy).
    A estratégia é sempre escolher o próximo serviço "mais barato" para adicionar a uma rota.
    """
    capacidade = dados["capacidade"]
    deposito = dados["deposito"]
    reqs = dados["requisitos"]

    # 1. INICIALIZAÇÃO
    # Cria o objeto Grafo que usaremos para todos os cálculos de distância.
    g = Grafo(dados)

    # Cria uma lista única com todos os serviços (nós, arestas e arcos).
    servicos = []
    id_global = 1
    for s_type, s_list in [('N', reqs["nos"]), ('E', reqs["arestas"]), ('A', reqs["arcos"])]:
        for s_orig in s_list:
            s = s_orig.copy()
            s['tipo'] = s_type
            s['global_id'] = id_global
            s['atendido'] = False # Flag para controlar quais serviços já foram alocados.
            servicos.append(s)
            id_global += 1

    total_servicos = len(servicos)
    servicos_atendidos_cont = 0
    rotas_finais = []

    # 2. LOOP DE CRIAÇÃO DE ROTAS
    # Este 'while' externo continua até que todos os serviços tenham sido atendidos.
    # Cada iteração deste loop cria UMA nova rota.
    while servicos_atendidos_cont < total_servicos:
        servicos_atendidos_antes = servicos_atendidos_cont
        carga_atual = 0
        seq_serv_rota_obj = []
        pos_atual = deposito # Toda nova rota começa no depósito.

        # 3. LOOP DE CONSTRUÇÃO DA ROTA ATUAL
        # Este 'while' interno adiciona serviços à rota atual até ela ficar cheia.
        while True:
            # Usa o grafo para obter as distâncias do ponto atual para todos os outros nós.
            # Graças ao cache, isso é rápido se a 'pos_atual' já foi visitada.
            distancias_atuais = g.obter_distancias(pos_atual)
            melhor_indice = -1
            menor_custo_insercao = math.inf
            p1_escolhido, p2_escolhido, prox_pos_escolhida = 0, 0, -1

            # 4. ENCONTRAR O MELHOR SERVIÇO PARA INSERIR
            # Itera sobre todos os serviços para encontrar o "mais barato" para adicionar agora.
            for i, s in enumerate(servicos):
                # CONDIÇÕES DE FILTRO:
                # - O serviço não pode já ter sido atendido.
                # - A demanda do serviço não pode exceder a capacidade restante do veículo.
                if s['atendido'] or (carga_atual + s['demanda'] > capacidade):
                    continue

                custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = math.inf, 0, 0, 0
                u, v, s_custo, t_custo = s['u'], s['v'], s['s_custo'], s['t_custo']

                # CÁLCULO DO CUSTO DE INSERÇÃO para cada tipo de serviço
                if s['tipo'] == 'N': # Nó
                    custo_viagem = distancias_atuais.get(u, math.inf)
                    if custo_viagem != math.inf:
                        custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = custo_viagem + s_custo, u, u, u
                elif s['tipo'] == 'E': # Aresta (pode ser percorrida em dois sentidos)
                    custo_vu = distancias_atuais.get(u, math.inf)
                    custo1 = (custo_vu + t_custo + s_custo) if custo_vu != math.inf else math.inf
                    custo_vv = distancias_atuais.get(v, math.inf)
                    custo2 = (custo_vv + t_custo + s_custo) if custo_vv != math.inf else math.inf
                    if custo1 <= custo2 and custo1 != math.inf: # Escolhe o sentido mais barato
                        custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = custo1, u, v, v
                    elif custo2 < custo1 and custo2 != math.inf:
                        custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = custo2, v, u, u
                elif s['tipo'] == 'A': # Arco (sentido único)
                    custo_viagem = distancias_atuais.get(u, math.inf)
                    if custo_viagem != math.inf:
                        custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = custo_viagem + t_custo + s_custo, u, v, v

                # --- A ESCOLHA GULOSA (GREEDY) ---
                # Se o custo do candidato atual é o menor que encontramos até agora,
                # ele se torna o nosso novo "melhor candidato".
                if custo_candidato_atual < menor_custo_insercao:
                    menor_custo_insercao, melhor_indice = custo_candidato_atual, i
                    p1_escolhido, p2_escolhido, prox_pos_escolhida = p1_temp, p2_temp, pos_final_temp
            
            # 5. ADICIONAR O SERVIÇO ESCOLHIDO À ROTA
            if melhor_indice != -1:
                servico_escolhido = servicos[melhor_indice]
                servico_escolhido['atendido'] = True # Marca como atendido
                servicos_atendidos_cont += 1
                carga_atual += servico_escolhido['demanda']
                seq_serv_rota_obj.append((servico_escolhido['global_id'], p1_escolhido, p2_escolhido, servico_escolhido['demanda'], servico_escolhido['s_custo'], servico_escolhido['t_custo']))
                pos_atual = prox_pos_escolhida # Atualiza a posição do veículo
            else:
                # Se nenhum serviço pôde ser adicionado, a rota atual está finalizada.
                break
        
        # 6. FINALIZAR E SALVAR A ROTA
        if seq_serv_rota_obj:
            # Calcula o custo final da rota (incluindo a volta ao depósito).
            custo_rota_final = calcular_custo_rota(seq_serv_rota_obj, g, deposito)
            if custo_rota_final == math.inf:
                print(f"ERRO ({dados['nome']}): Rota inviável detectada durante construção!")
            # Salva a rota completa com todas as suas informações.
            rotas_finais.append({"servicos": seq_serv_rota_obj, "servicos_str": [f"(S {s[0]},{s[1]},{s[2]})" for s in seq_serv_rota_obj], "demanda": carga_atual, "custo": custo_rota_final})

        # Medida de segurança para evitar loops infinitos.
        if servicos_atendidos_cont == servicos_atendidos_antes and servicos_atendidos_cont < total_servicos:
            print(f"AVISO CRÍTICO ({dados['nome']}): Loop estagnado. {total_servicos - servicos_atendidos_cont} serviços não atendidos. Parando.")
            break
            
    return rotas_finais, g