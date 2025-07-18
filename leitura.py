# leitura.py (Versão Limpa e Comentada para Apresentação)
# OBJETIVO: Este arquivo é responsável por ler os arquivos de instância (.dat),
# que contêm a descrição do problema (mapa, serviços, capacidade do veículo, etc.),
# e carregar esses dados em uma estrutura de dicionário Python para fácil acesso.

import os

def ler_instancia_completa(caminho):
    """
    Função principal que lê um arquivo de instância do CARP, linha por linha,
    e o transforma em um dicionário Python estruturado.

    Args:
        caminho (str): O caminho completo para o arquivo .dat da instância.

    Returns:
        dict: Um dicionário contendo todos os dados da instância.
    """
    with open(caminho, "r", encoding="utf-8") as f:
        # Lê todas as linhas do arquivo, removendo espaços em branco e linhas vazias.
        linhas = [l.strip() for l in f if l.strip()]

    # Estrutura de dados principal para armazenar as informações da instância.
    # É inicializada com valores padrão.
    dados = {
        "nome": os.path.basename(caminho),
        "optimal_value": None,
        "capacidade": 0,
        "deposito": 0,
        "num_vertices": 0,
        "requisitos": {
            "nos": [],
            "arestas": [],
            "arcos": []
        },
        "conexoes": []
    }

    # Função auxiliar para identificar linhas de cabeçalho que devem ser ignoradas.
    def is_header(l):
        h = l.upper()
        return ("DEMAND" in h or "S. COST" in h or "FROM" in h or "TO" in h or "T. COST" in h or "COST" in h)

    # Função auxiliar para tentar extrair uma conexão (u, v, custo) de uma linha.
    def try_parse_connection(line_parts):
        try:
            u = int(line_parts[-3])
            v = int(line_parts[-2])
            custo = int(line_parts[-1])
            return u, v, custo
        except (IndexError, ValueError):
            return None, None, None

    # Loop principal para percorrer o arquivo linha por linha.
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        lstr = linha.strip().upper()

        # --- PARTE 1: Leitura do Cabeçalho (Informações Gerais) ---
        # Cada 'if' aqui procura por uma palavra-chave para identificar a informação.
        if "OPTIMAL VALUE" in lstr: i+=1; continue # Ignora o valor ótimo
        elif "CAPACITY" in lstr: dados["capacidade"] = int(linha.split(":")[1].strip()); i+=1; continue
        elif "DEPOT NODE" in lstr: dados["deposito"] = int(linha.split(":")[1].strip()); i+=1; continue
        elif "#NODES" in lstr: dados["num_vertices"] = int(linha.split(":")[1].replace('\t','').strip()); i+=1; continue
        # Ignora outras informações não utilizadas no nosso modelo.
        elif "#VEHICLES" in lstr: i+=1; continue
        elif "#EDGES" in lstr: i+=1; continue
        elif "#ARCS" in lstr: i+=1; continue
        elif "#REQUIRED" in lstr: i+=1; continue
        elif "NAME:" in lstr: i+=1; continue

        # --- PARTE 2: Leitura dos Serviços Requeridos ---
        # Esta seção identifica blocos de serviços (Nós, Arestas, Arcos).
        
        # Bloco de Nós Requeridos (Required Nodes)
        elif lstr.startswith("REN."):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or not l.strip().upper().startswith("N") or is_header(l): break
                try:
                    partes = l.split(); sid = int(partes[0][1:]); d = int(partes[1]); sc = int(partes[2])
                    dados["requisitos"]["nos"].append({"id": sid, "u": sid, "v": sid, "demanda": d, "s_custo": sc, "t_custo": 0})
                except Exception as e: print(f"AVISO Leitura ReN: '{l}' - {e}")
                i += 1
            continue
        
        # Bloco de Arestas Requeridas (Required Edges)
        elif lstr.startswith("REE."):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or not l.strip().upper().startswith("E") or is_header(l): break
                try:
                    partes = l.split(); sid = int(partes[0][1:]); u = int(partes[1]); v = int(partes[2]); tc = int(partes[3]); d = int(partes[4]); sc = int(partes[5])
                    dados["requisitos"]["arestas"].append({"id": sid, "u": u, "v": v, "demanda": d, "s_custo": sc, "t_custo": tc})
                    # Uma aresta requerida também é uma conexão no grafo. Adicionamos nos dois sentidos.
                    dados["conexoes"].append((u, v, tc, "E")); dados["conexoes"].append((v, u, tc, "E"))
                except Exception as e: print(f"AVISO Leitura ReE: '{l}' - {e}")
                i += 1
            continue

        # Bloco de Arcos Requeridos (Required Arcs)
        elif lstr.startswith("REA."):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or not l.strip().upper().startswith("A") or is_header(l): break
                try:
                    partes = l.split(); sid = int(partes[0][1:]); u = int(partes[1]); v = int(partes[2]); tc = int(partes[3]); d = int(partes[4]); sc = int(partes[5])
                    dados["requisitos"]["arcos"].append({"id": sid, "u": u, "v": v, "demanda": d, "s_custo": sc, "t_custo": tc})
                    # Um arco requerido é uma conexão de mão única.
                    dados["conexoes"].append((u, v, tc, "A"))
                except Exception as e: print(f"AVISO Leitura ReA: '{l}' - {e}")
                i += 1
            continue

        # --- PARTE 3: Leitura da Topologia do Grafo (Conexões não requeridas) ---
        
        # Bloco de Arestas Não-Requeridas (Non-required Edges)
        elif lstr.startswith("EDGE"):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or is_header(l) or l.upper().startswith("ARC"): break
                partes = l.split()
                u, v, custo = try_parse_connection(partes)
                if u is not None:
                    # Adiciona a conexão nos dois sentidos, pois é uma aresta.
                    dados["conexoes"].append((u, v, custo, "NE"))
                    dados["conexoes"].append((v, u, custo, "NE"))
                else: pass
                i += 1
            continue

        # Bloco de Arcos Não-Requeridos (Non-required Arcs)
        elif lstr.startswith("ARC"):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or is_header(l) or l.upper().startswith("END"): break
                partes = l.split()
                u, v, custo = try_parse_connection(partes)
                if u is not None:
                    # Adiciona a conexão em sentido único, pois é um arco.
                    dados["conexoes"].append((u, v, custo, "NA"))
                else: pass
                i += 1
            continue

        # Avança para a próxima linha se nenhuma das condições acima for atendida.
        i += 1
    return dados