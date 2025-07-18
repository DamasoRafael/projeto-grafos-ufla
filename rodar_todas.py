# rodar_todas.py
# OBJETIVO: Script principal para produção. Ele processa TODAS as instâncias
# encontradas na pasta "Ins", resolve cada uma e salva o arquivo de solução
# no formato especificado no trabalho.

import os
import time
from leitura import ler_instancia_completa
from construtivo import gerar_solucao_viavel
from melhoria import aprimorar_solucao_vns

def escrever_solucao_formato_pdf(nome_arquivo, rotas_info, custo_total, clocks_heuristica_secs):
    """
    Função auxiliar para escrever o arquivo de solução (sol-nomeInstancia.dat)
    no formato exato exigido para a entrega.
    """
    # ... (código de formatação da saída)
    pass # O código interno já é autoexplicativo para a formatação.

# ... (código completo da função escrever_solucao_formato_pdf)

def main():
    # --- CONFIGURAÇÃO DOS DIRETÓRIOS ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_ins = os.path.join(base_dir, "Ins")
    pasta_saida = os.path.join(base_dir, "SolucoesFinais")

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Encontra todos os arquivos .dat na pasta de instâncias.
    arquivos = sorted([f for f in os.listdir(pasta_ins) if f.endswith(".dat")])
    
    # --- LOOP DE PROCESSAMENTO EM LOTE ---
    total_arquivos = len(arquivos)
    print(f"Encontradas {total_arquivos} instâncias. Iniciando processamento...")
    start_time_total = time.time()

    # Itera sobre cada arquivo de instância encontrado.
    for idx, fname in enumerate(arquivos):
        path = os.path.join(pasta_ins, fname)
        print(f"[{idx + 1}/{total_arquivos}] Resolvendo: {fname}...")
        try:
            # --- FLUXO DE EXECUÇÃO (igual ao mainTeste, mas dentro de um loop) ---
            t0 = time.time()
            
            # 1. Leitura
            dados = ler_instancia_completa(path)
            
            # 2. Construtivo
            rotas_info, grafo_obj = gerar_solucao_viavel(dados)
            
            # 3. Melhoria
            aprimorar_solucao_vns(rotas_info, dados, grafo_obj)

            t1 = time.time()
            
            # 4. ESCRITA DA SOLUÇÃO
            clocks_heuristica_secs = t1 - t0
            custo_total = sum(r["custo"] for r in rotas_info)
            saida = os.path.join(pasta_saida, f"sol-{fname}")
            
            escrever_solucao_formato_pdf(saida, rotas_info, custo_total, clocks_heuristica_secs)
            print(f"    -> Concluído. Custo={int(round(custo_total))}, Rotas={len(rotas_info)}, Tempo={clocks_heuristica_secs:.4f}s.")

        except Exception as e:
            # Tratamento de erro para não parar a execução em lote se uma instância falhar.
            print(f"    ERRO FATAL ao processar '{fname}': {e}")
            import traceback
            traceback.print_exc()
            continue
            
    end_time_total = time.time()
    print(f"\n Processamento concluído em {end_time_total - start_time_total:.2f} segundos.")
    print(f"Todas as {total_arquivos} soluções foram geradas em: {pasta_saida}")

if __name__ == "__main__":
    main()