import os
from collections import defaultdict

def buscar_arquivos_txt(caminho_base):
    arquivos_txt = []
    for root, dirs, files in os.walk(caminho_base):#explicação: percorre todos os diretórios e subdiretórios e arquivos a partir do caminho base
        for file in files:#explicação: percorre todos os arquivos encontrados
            if file.endswith(""):#explicação: verifica se o arquivo termina com .txt
                arquivos_txt.append(os.path.join(root, file))#explicação: adiciona o caminho completo do arquivo à lista
    return arquivos_txt

# Função para extrair remetente e destinatários de um arquivo
def extrair_emails(caminho_arquivo):
    remetente = None#explicação: inicializa a variável remetente como None
    destinatarios = []#explicação: inicializa a lista destinatarios como vazia
    # Lê o arquivo e extrai os campos "From" e "To"
    # abre o arquivo no caminho especificado para leitura
    # usa 'utf-8' como codificação e ignora erros de codificação
    # lê o arquivo linha por linha
    # verifica se a linha começa com "From:" ou "To:"
    # se a linha começar com "From:", extrai o remetente
    # se a linha começar com "To:", extrai os destinatários
    # quebra a linha em partes e remove espaços em branco
    # se o remetente e destinatários forem encontrados, sai do loop
    # se o remetente e destinatários não forem encontrados, retorna None, None

    with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            if linha.lower().startswith("from:"):
                remetente = linha.split(":", 1)[1].strip().lower()
            elif linha.lower().startswith("to:"):
                lista = linha.split(":", 1)[1].strip().lower()
                destinatarios = [email.strip() for email in lista.split(",") if email.strip()]
            if remetente and destinatarios:
                break

    return remetente, destinatarios

def construir_grafo(lista_arquivos):
    grafo = {}#explicação: inicializa o grafo como um dicionário vazio
    # Para cada arquivo na lista de arquivos
    # extrai os emails de remetente e destinatário
    # se o remetente não estiver no grafo, adiciona
    # se o destinatário não estiver no grafo, adiciona
    # adiciona o destinatário ao grafo do remetente
    # incrementa o peso da aresta entre o remetente e o destinatário
    # retorna o grafo construído

    for arquivo in lista_arquivos:
        from_email, to_emails = extrair_emails(arquivo)
        if from_email and to_emails:
            if from_email not in grafo:
                grafo[from_email] = {}
            for to in to_emails:
                if to not in grafo[from_email]:
                    grafo[from_email][to] = 0
                grafo[from_email][to] += 1  # Ponderação pelo número de mensagens

    return grafo

def salvar_lista_adjacencia(grafo, caminho_saida):
    with open(caminho_saida, "w") as f:#explicação: abre o arquivo de saída para escrita
        for remetente in grafo:# percorre os remetentes no grafo
            for destinatario in grafo[remetente]:# percorre os destinatários do remetente
                peso = grafo[remetente][destinatario]# obtém o peso da aresta
                # escreve no arquivo no formato "remetente -> destinatario [peso]"
                f.write(f"{remetente} -> {destinatario} [peso: {peso}]\n")
                

def ordem_tamanho(grafo):
    vertices = set(grafo.keys())
    for destinos in grafo.values():
        vertices.update(destinos.keys())
    ordem = len(vertices)

    tamanho = sum(len(destinos) for destinos in grafo.values())
    return ordem, tamanho

def vertices_isolados(grafo):
    todos = set(grafo.keys())
    destinos = set()
    for d in grafo.values():
        destinos.update(d.keys())
    isolados = destinos.symmetric_difference(todos)
    return list(isolados)


def graus_saida_entrada(grafo):
    grau_saida = {v: sum(d.values()) for v, d in grafo.items()}

    grau_entrada = defaultdict(int)
    for origem in grafo:
        for destino, peso in grafo[origem].items():
            grau_entrada[destino] += peso

    top_saida = sorted(grau_saida.items(), key=lambda x: x[1], reverse=True)[:20]
    top_entrada = sorted(grau_entrada.items(), key=lambda x: x[1], reverse=True)[:20]

    return top_saida, top_entrada


def grafo_euleriano(grafo, caminho_saida):
    entrada = defaultdict(int)
    saida = defaultdict(int)
    violacoes = []
    
    # Calcula graus de entrada e saída
    for origem in grafo:
        saida[origem] = sum(grafo[origem].values())
        for destino in grafo[origem]:
            entrada[destino] += grafo[origem][destino]
    
    # Verifica graus iguais para todos os vértices
    todos_vertices = set(entrada.keys()).union(set(saida.keys()))
    for v in todos_vertices:
        if entrada.get(v, 0) != saida.get(v, 0):
            violacoes.append(f"Vértice {v}: entrada={entrada.get(v,0)}, saída={saida.get(v,0)}")
    
    # Verifica conectividade forte (usando Kosaraju)
    conectado = kosaraju(grafo)  # Assume que a função kosaraju já está implementada
    
    # Salva o resultado detalhado no arquivo
    with open(caminho_saida, "w") as f:
        if len(violacoes) == 0 and conectado:
            f.write("O grafo atende a todas as condições para ser Euleriano:\n")
            f.write("- Todos os vértices têm grau de entrada igual ao de saída.\n")
            f.write("- O grafo é fortemente conectado.\n")
        else:
            f.write("O grafo NÃO é Euleriano. Motivos:\n")
            if len(violacoes) > 0:
                f.write("- Vértices com graus de entrada/saída desiguais:\n")
                f.write("\n".join(violacoes) + "\n")
            if not conectado:
                f.write("- O grafo não é fortemente conectado.\n")
    
    # Retorna apenas True/False para exibir no terminal
    if len(violacoes) == 0 and conectado:
        print("O grafo é Euleriano.")
        return True
    else:
        print("O grafo não é Euleriano.")
        return False
    
def salvar_lista_compactada(grafo, caminho_saida):
    with open(caminho_saida, "w") as f:
        for remetente in grafo:
            linha = f"{remetente.upper()}"
            for destinatario, peso in grafo[remetente].items():
                linha += f" -> {destinatario} [peso: {peso}]"
            f.write(linha + "\n")


import heapq  # Adicione no início do arquivo

def vertices_ate_distancia(grafo, origem, distancia_max):
    distancias = {origem: 0}
    heap = [(0, origem)]
    visitados = set()

    while heap:
        dist_atual, atual = heapq.heappop(heap)
        if dist_atual > distancia_max:
            continue
        if atual in visitados:
            continue
        visitados.add(atual)

        for vizinho, peso in grafo.get(atual, {}).items():
            nova_dist = dist_atual + peso
            if nova_dist <= distancia_max and (vizinho not in distancias or nova_dist < distancias.get(vizinho, float('inf'))):
                distancias[vizinho] = nova_dist
                heapq.heappush(heap, (nova_dist, vizinho))

    return list(visitados)
           

def dijkstra_com_caminho(grafo, origem):
    distancias = {origem: 0}
    anteriores = {}
    fila = [origem]

    while fila:
        atual = min(fila, key=lambda v: distancias[v])
        fila.remove(atual)

        for vizinho, peso in grafo.get(atual, {}).items():
            nova_dist = distancias[atual] + peso
            if vizinho not in distancias or nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                anteriores[vizinho] = atual
                if vizinho not in fila:
                    fila.append(vizinho)

    return distancias, anteriores

def reconstruir_caminho(anteriores, origem, destino):
    caminho = [destino]
    while destino in anteriores:
        destino = anteriores[destino]
        caminho.insert(0, destino)
    if caminho[0] == origem:
        return caminho
    return []  # caso não seja alcançável

def calcular_diametro(grafo):
    maior_distancia = -1
    melhor_caminho = []
    origem_final = ""
    destino_final = ""

    for origem in grafo:
        distancias, anteriores = dijkstra_com_caminho(grafo, origem)
        for destino in distancias:
            if origem != destino and distancias[destino] > maior_distancia:
                maior_distancia = distancias[destino]
                origem_final = origem
                destino_final = destino
                melhor_caminho = reconstruir_caminho(anteriores, origem, destino)

    return maior_distancia, melhor_caminho
            

def kosaraju(grafo):
    visitados = set()
    ordem = []
    componentes = []

    # Primeira passada: ordenação por tempo de finalização
    def dfs(v):
        if v not in visitados:
            visitados.add(v)
            for u in grafo.get(v, {}):
                dfs(u)
            ordem.append(v)

    for v in grafo:
        dfs(v)

    # Grafo transposto (inverte direção das arestas)
    grafo_transposto = defaultdict(dict)
    for origem in grafo:
        for destino in grafo[origem]:
            if destino not in grafo_transposto:
                grafo_transposto[destino] = {}
            grafo_transposto[destino][origem] = grafo[origem][destino]

    # Segunda passada: identificar componentes
    visitados.clear()
    while ordem:
        v = ordem.pop()
        if v not in visitados:
            componente = []
            pilha = [v]
            visitados.add(v)
            while pilha:
                node = pilha.pop()
                componente.append(node)
                for vizinho in grafo_transposto.get(node, {}):
                    if vizinho not in visitados:
                        visitados.add(vizinho)
                        pilha.append(vizinho)
            componentes.append(componente)

    return len(componentes) == 1  # Se só há 1 componente, é fortemente conectado
