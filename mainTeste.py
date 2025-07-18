# mainTeste.py
# OBJETIVO: Um script simples para testar a solução em UMA ÚNICA instância.
# É útil para depuração e análise detalhada de um caso específico.

import os
import time
# Importa as funções principais de cada módulo do projeto.
from leitura import ler_instancia_completa
from construtivo import gerar_solucao_viavel
from melhoria import aprimorar_solucao_vns # Mudei para VNS para consistência

def main():
    # --- CONFIGURAÇÃO ---
    # Altere o nome do arquivo aqui para testar a instância desejada
    inst = "mgval_0.25_5C.dat" 

    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "Ins", inst)

    if not os.path.exists(path):
        print(f"ERRO: Arquivo de instância não encontrado em '{path}'")
        return

    print(f"--- Resolvendo instância: {inst} ---")
    
    # --- FLUXO DE EXECUÇÃO ---
    # 1. LEITURA DOS DADOS
    # Carrega todas as informações do arquivo .dat para a memória.
    dados = ler_instancia_completa(path)

    t_inicio = time.time()

    # 2. HEURÍSTICA CONSTRUTIVA
    # Gera a primeira solução viável usando a nossa estratégia de inserção gulosa.
    print("1. Gerando solução construtiva inicial...")
    rotas_info, grafo_obj = gerar_solucao_viavel(dados)
    custo_inicial = sum(r["custo"] for r in rotas_info)
    print(f"   -> Custo inicial: {int(round(custo_inicial))}, Rotas: {len(rotas_info)}")

    # 3. HEURÍSTICA DE MELHORIA
    # Pega a solução inicial e tenta aprimorá-la usando a busca local (VNS).
    print("\n2. Aprimorando solução com VNS (Relocate, Swap, 2-Opt)...")
    aprimorar_solucao_vns(rotas_info, dados, grafo_obj)

    t_fim = time.time()
    tempo_total_secs = t_fim - t_inicio
    
    custo_final = sum(r["custo"] for r in rotas_info)

    # --- RESULTADO FINAL ---
    print("\n--- Resultado Final ---")
    print(f"Custo Inicial:      {int(round(custo_inicial))}")
    print(f"Custo Final (após VNS): {int(round(custo_final))}")
    print(f"Número de Rotas:    {len(rotas_info)}")
    print(f"Tempo de Execução:  {tempo_total_secs:.4f} segundos")
    print("-----------------------\n")

if __name__ == "__main__":
    main()