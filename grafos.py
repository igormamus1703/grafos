import os
from collections import defaultdict

def buscar_arquivos_txt(caminho_base):
    arquivos_txt = []
    for root, dirs, files in os.walk(caminho_base):
        for file in files:
            if file.endswith(""):
                arquivos_txt.append(os.path.join(root, file))
    return arquivos_txt

arquivos = buscar_arquivos_txt("/home/est.igor/grafos/grafos/Amostra Enron - 2016")


def extrair_emails(caminho_arquivo):
    remetente = None
    destinatarios = []

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
    grafo = {}

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
    with open(caminho_saida, "w") as f:
        for remetente in grafo:
            for destinatario in grafo[remetente]:
                peso = grafo[remetente][destinatario]
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


def grafo_euleriano(grafo):
    entrada = defaultdict(int)
    saida = defaultdict(int)

    for origem in grafo:
        saida[origem] = sum(grafo[origem].values())
        for destino in grafo[origem]:
            entrada[destino] += grafo[origem][destino]

    for v in set(list(entrada.keys()) + list(saida.keys())):
        if entrada[v] != saida[v]:
            return False, f"Vértice {v} tem entrada={entrada[v]} e saída={saida[v]}"
    return True, "O grafo é Euleriano."

def salvar_lista_compactada(grafo, caminho_saida):
    with open(caminho_saida, "w") as f:
        for remetente in grafo:
            linha = f"{remetente.upper()}"
            for destinatario, peso in grafo[remetente].items():
                linha += f" -> {destinatario} [peso: {peso}]"
            f.write(linha + "\n")

