# Solver para o **Problema de Roteamento de Arcos Capacitado (CARP)**
> **Disciplina:** Algoritmos em Grafos (GCC218)  
> **Universidade:** Universidade Federal de Lavras – UFLA  
> **Autores:** João Vitor Givisiez Lessa • Rafael Rabelo Pereira Damaso  

---

## ✨ Visão Geral
Este projeto implementa, em **Python 3**, uma solução completa para o CAPACITATED ARC ROUTING PROBLEM (CARP).  
O objetivo é planejar rotas de **custo mínimo** para uma frota de veículos, atendendo tarefas (nós, arestas ou arcos) com demandas específicas **sem exceder** a capacidade de cada veículo.

O algoritmo está dividido em **duas fases principais**:

1. **Heurística Construtiva** – Geração de uma solução inicial viável por inserção mais barata.  
2. **Otimização por Busca Local** – Refinamento da solução via **Variable Neighborhood Descent (VND)**.

---

## ⚙️ Metodologia

| Fase | Abordagem | Descrição resumida |
|------|-----------|--------------------|
| **Construtiva** | **Inserção Mais Barata** | Constrói rotas incrementalmente, sempre escolhendo a tarefa não atendida com **menor custo marginal**, respeitando a capacidade do veículo. |
| **Melhoria** | **VND** | Explora sucessivamente diferentes vizinhanças e reinicia do primeiro movimento sempre que encontra melhoria, até convergir. |

### ↔️ Estruturas de Vizinhança (VND)

- **Relocate** – Move um serviço de uma rota para outra.  
- **Swap** – Troca serviços entre duas rotas.  
- **2‑Opt (Intra‑rota)** – Remove cruzamentos dentro de uma rota.

### 🚗 Cálculo de Distâncias
Adota‑se **Dijkstra sob demanda** com **cache**.  
Isso elimina o gasto de pré‑computar todas as distâncias (como em Floyd‑Warshall) e acelera drasticamente a fase de busca local, preservando exatidão.

---

## 📂 Estrutura do Repositório
```
solver-carp-ufla/
├── Ins/                 # 409 instâncias .dat originais
│   ├── BHW1.dat
│   └── ...
├── SolucoesFinais/      # Saídas geradas (.dat)
│   ├── sol-BHW1.dat
│   └── ...
├── construtivo.py       # Heurística (Fase 1)
├── melhoria.py          # VND (Fase 2)
├── dijkstra.py          # Dijkstra + cache
├── grafo.py             # Estrutura de grafo + custos
├── leitura.py           # Parser de instâncias
├── rodar_todas.py       # Pipeline completo
├── README.md            # Este documento
└── tests/               # Casos de teste unitários (opcional)
```

---

## ▶️ Como Executar

### Pré‑requisitos
- **Python ≥ 3.8**  
- Diretório **`Ins/`** com todas as instâncias **.dat**

### Execução completa
```bash
# Na raiz do projeto
python rodar_todas.py
```
O script:

1. Lê cada instância em `Ins/`.
2. Executa a heurística construtiva seguida do VND.
3. Grava a solução correspondente em `SolucoesFinais/`.
4. **Retomável**: se uma solução já existir, aquela instância é pulada.

---

## 📈 Resultados Esperados
A combinação **Inserção + VND** gera soluções de boa qualidade em tempo compatível com aplicações acadêmicas, sendo adequada para instâncias clássicas de benchmark (por ex. conjuntos **B**, **C**, **D**, **E**).

---

## 👫 Autores
| Nome | Contato |
|------|---------|
| **João Vitor Givisiez Lessa** | [@github.com/joao-givisiez](https://github.com/joao-givisiez) |
| **Rafael Rabelo Pereira Damaso** | [@github.com/DamasoRafael](https://github.com/DamasoRafael) |

---

## 📜 Licença
Este projeto é disponibilizado sob a licença **MIT**. Consulte o arquivo `LICENSE` para detalhes.

---

## 🤝 Contribuições
Contribuições são bem‑vindas! Abra *issues* ou *pull requests* seguindo o guia de estilo *PEP8* e descrevendo claramente a proposta de melhoria.

---

> “Programar é traduzir problemas do mundo real em soluções que a máquina compreenda. Fazer isso de forma eficiente é arte e ciência.” — *GCC218*
