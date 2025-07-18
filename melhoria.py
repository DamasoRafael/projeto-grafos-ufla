# melhoria.py
# OBJETIVO: Este arquivo contém as heurísticas de melhoria (busca local).
# Depois de ter uma solução inicial do construtivo, este código tenta
# aprimorá-la fazendo pequenas alterações iterativas para reduzir o custo total.

import math
import time
from grafo import calcular_custo_rota

# --- CRITÉRIO DE PARADA ---
# Define um tempo máximo global para a fase de melhoria, para evitar que
# o programa rode indefinidamente em instâncias muito complexas.
MAX_TIME_GLOBAL_SECONDS = 120 

def aprimorar_solucao_vns(rotas_info, dados, grafo):
    """
    Função principal que orquestra a melhoria da solução usando uma abordagem
    inspirada no VNS (Variable Neighborhood Search - Busca em Vizinhança Variável).
    Ela aplica uma sequência de movimentos (Relocate, Swap, 2-Opt) repetidamente.
    """
    print("    -> Iniciando fase de melhoria VNS (Relocate, Swap, 2-Opt)...")
    
    start_time_global = time.time()

    # O loop principal do VNS. Ele continuará tentando melhorar a solução
    # até que nenhum dos movimentos consiga encontrar uma redução de custo.
    while True:
        # Critério de parada por tempo.
        if time.time() - start_time_global > MAX_TIME_GLOBAL_SECONDS:
            print("      AVISO: Tempo limite global atingido. Finalizando melhoria.")
            break

        custo_antes_iteracao = sum(r['custo'] for r in rotas_info)
        
        # --- ESTRUTURA VNS ---
        # 1. Tenta o primeiro tipo de movimento: Relocate.
        #    A ideia é: se um movimento simples funciona, ótimo. Comece de novo.
        print(f"      [VNS] Custo atual: {int(round(custo_antes_iteracao))}. Tentando Relocate...")
        if find_best_relocate(rotas_info, dados, grafo):
            continue # Se melhorou, o 'continue' reinicia o loop do VNS.

        # 2. Se Relocate não melhorou, tenta um movimento mais complexo: Swap.
        print(f"      [VNS] Custo atual: {int(round(sum(r['custo'] for r in rotas_info)))}. Tentando Swap...")
        if find_best_swap(rotas_info, dados, grafo):
            continue # Se melhorou, reinicia o loop do VNS.
        
        # 3. Se nem Relocate nem Swap funcionaram, tenta um movimento intra-rota: 2-Opt.
        print(f"      [VNS] Custo atual: {int(round(sum(r['custo'] for r in rotas_info)))}. Tentando 2-Opt...")
        if find_best_2opt(rotas_info, dados, grafo):
            continue # Se melhorou, reinicia o loop do VNS.
        
        # 4. Se NENHUM dos movimentos acima resultou em melhoria,
        #    significa que atingimos um "ótimo local". O algoritmo para.
        break

    print("    -> Melhoria VNS concluída.")


def find_best_relocate(rotas_info, dados, grafo):
    """
    Movimento RELOCATE (Realocação): Tenta mover um serviço de uma rota para outra.
    Busca o melhor movimento de realocação possível em toda a solução.
    Retorna True se uma melhoria foi feita, False caso contrário.
    """
    deposito = dados["deposito"]
    capacidade = dados["capacidade"]
    melhor_ganho = 0
    melhor_movimento = None

    # Itera sobre cada rota de origem (r1)
    for r1_idx, rota1 in enumerate(rotas_info):
        # Itera sobre cada serviço (s1) na rota de origem
        for s1_idx in range(len(rota1["servicos"])):
            servico_para_mover = rota1["servicos"][s1_idx]
            
            # Itera sobre cada rota de destino (r2)
            for r2_idx, rota2 in enumerate(rotas_info):
                if r1_idx == r2_idx: continue # Não podemos mover um serviço para a mesma rota

                # VERIFICAÇÃO DE VIABILIDADE: Garante que a rota de destino tem capacidade.
                if rota2["demanda"] + servico_para_mover[3] > capacidade:
                    continue

                custo_original = rota1["custo"] + rota2["custo"]
                
                # CÁLCULO DO GANHO:
                # 1. Calcula o novo custo da rota de origem sem o serviço.
                rota1_temp = rota1["servicos"][:s1_idx] + rota1["servicos"][s1_idx+1:]
                custo1_novo = calcular_custo_rota(rota1_temp, grafo, deposito)

                # 2. Tenta inserir o serviço em todas as posições possíveis da rota de destino.
                for s2_idx in range(len(rota2["servicos"]) + 1):
                    rota2_temp = rota2["servicos"][:s2_idx] + [servico_para_mover] + rota2["servicos"][s2_idx:]
                    custo2_novo = calcular_custo_rota(rota2_temp, grafo, deposito)
                    
                    custo_novo_total = custo1_novo + custo2_novo
                    ganho = custo_original - custo_novo_total

                    # Se o ganho deste movimento for o melhor até agora, armazena-o.
                    if ganho > melhor_ganho:
                        melhor_ganho = ganho
                        melhor_movimento = (r1_idx, s1_idx, r2_idx, s2_idx)
    
    # Se encontramos um movimento que gera um ganho positivo...
    if melhor_movimento:
        # ... APLICA O MOVIMENTO ...
        r1_idx, s1_idx, r2_idx, s2_idx = melhor_movimento
        
        servico_movido = rotas_info[r1_idx]["servicos"].pop(s1_idx)
        rotas_info[r2_idx]["servicos"].insert(s2_idx, servico_movido)
        
        # ... e atualiza os dados das rotas modificadas.
        for idx in [r1_idx, r2_idx]:
            rotas_info[idx]["custo"] = calcular_custo_rota(rotas_info[idx]["servicos"], grafo, deposito)
            rotas_info[idx]["demanda"] = sum(s[3] for s in rotas_info[idx]["servicos"])
            rotas_info[idx]["servicos_str"] = [f"(S {s[0]},{s[1]},{s[2]})" for s in rotas_info[idx]["servicos"]]

        return True # Indica que uma melhoria foi feita.
    return False


def find_best_swap(rotas_info, dados, grafo):
    """
    Movimento SWAP (Troca): Tenta trocar um serviço de uma rota por um serviço de outra.
    Busca a melhor troca possível em toda a solução.
    Retorna True se uma melhoria foi feita, False caso contrário.
    """
    deposito = dados["deposito"]
    capacidade = dados["capacidade"]
    melhor_ganho = 0
    melhor_movimento = None

    # Itera sobre todos os pares de rotas (r1, r2)
    for r1_idx in range(len(rotas_info)):
        for r2_idx in range(r1_idx + 1, len(rotas_info)):
            rota1 = rotas_info[r1_idx]
            rota2 = rotas_info[r2_idx]
            
            # Itera sobre todos os pares de serviços (s1, s2), um de cada rota
            for s1_idx, servico1 in enumerate(rota1["servicos"]):
                for s2_idx, servico2 in enumerate(rota2["servicos"]):
                    
                    # VERIFICAÇÃO DE VIABILIDADE: Garante que a troca não viola a capacidade de nenhuma das rotas.
                    if (rota1["demanda"] - servico1[3] + servico2[3] > capacidade) or \
                       (rota2["demanda"] - servico2[3] + servico1[3] > capacidade):
                        continue

                    custo_original = rota1["custo"] + rota2["custo"]
                    
                    # CÁLCULO DO GANHO:
                    # Cria rotas temporárias com a troca para calcular o novo custo.
                    rota1_temp_servicos = rota1["servicos"][:s1_idx] + [servico2] + rota1["servicos"][s1_idx+1:]
                    rota2_temp_servicos = rota2["servicos"][:s2_idx] + [servico1] + rota2["servicos"][s2_idx+1:]

                    custo_novo_total = calcular_custo_rota(rota1_temp_servicos, grafo, deposito) + \
                                       calcular_custo_rota(rota2_temp_servicos, grafo, deposito)

                    ganho = custo_original - custo_novo_total
                    # Se o ganho for o melhor até agora, armazena o movimento.
                    if ganho > melhor_ganho:
                        melhor_ganho = ganho
                        melhor_movimento = (r1_idx, s1_idx, r2_idx, s2_idx)

    # Se uma troca vantajosa foi encontrada...
    if melhor_movimento:
        # ... APLICA A TROCA ...
        r1_idx, s1_idx, r2_idx, s2_idx = melhor_movimento
        
        servico1 = rotas_info[r1_idx]["servicos"][s1_idx]
        servico2 = rotas_info[r2_idx]["servicos"][s2_idx]
        rotas_info[r1_idx]["servicos"][s1_idx] = servico2
        rotas_info[r2_idx]["servicos"][s2_idx] = servico1

        # ... e atualiza os dados das rotas modificadas.
        for idx in [r1_idx, r2_idx]:
            rotas_info[idx]["custo"] = calcular_custo_rota(rotas_info[idx]["servicos"], grafo, deposito)
            rotas_info[idx]["demanda"] = sum(s[3] for s in rotas_info[idx]["servicos"])
            rotas_info[idx]["servicos_str"] = [f"(S {s[0]},{s[1]},{s[2]})" for s in rotas_info[idx]["servicos"]]
            
        return True
    return False

def find_best_2opt(rotas_info, dados, grafo):
    """
    Movimento 2-Opt (Intra-rota): Tenta melhorar UMA rota de cada vez,
    "descruzando" caminhos. Ele remove duas arestas da rota e as reconecta
    da única outra maneira possível, invertendo a sequência de serviços entre elas.
    """
    deposito = dados["deposito"]
    houve_melhoria_geral = False

    # Aplica o 2-Opt para cada rota individualmente.
    for rota in rotas_info:
        if len(rota["servicos"]) < 2: continue
        
        custo_inicial_rota = rota["custo"]
        
        # Continua tentando melhorar a mesma rota até que nenhuma melhoria 2-Opt seja possível.
        melhoria_na_rota = True
        while melhoria_na_rota:
            melhoria_na_rota = False
            custo_atual = calcular_custo_rota(rota["servicos"], grafo, deposito)
            
            # Itera sobre todos os pares de arestas para remover (j, k).
            for j in range(len(rota["servicos"]) - 1):
                for k in range(j + 1, len(rota["servicos"])):
                    # AQUI ESTÁ A LÓGICA DO 2-OPT:
                    # Cria uma nova sequência invertendo o trecho entre j e k.
                    # O [::-1] é o que faz a inversão.
                    nova_sequencia = rota["servicos"][:j] + rota["servicos"][j:k+1][::-1] + rota["servicos"][k+1:]
                    
                    novo_custo = calcular_custo_rota(nova_sequencia, grafo, deposito)
                    
                    # Se a nova rota é mais barata, aceita a mudança.
                    if novo_custo < custo_atual:
                        rota["servicos"] = nova_sequencia
                        custo_atual = novo_custo
                        melhoria_na_rota = True
                        houve_melhoria_geral = True
                        break # Sai do loop interno para recomeçar a busca na rota modificada.
                if melhoria_na_rota: break
        
        # Atualiza o custo final e a representação em string da rota.
        rota["custo"] = calcular_custo_rota(rota["servicos"], grafo, deposito)
        rota["servicos_str"] = [f"(S {s[0]},{s[1]},{s[2]})" for s in rota["servicos"]]
            
    return houve_melhoria_geral