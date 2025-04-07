from grafos import (
    buscar_arquivos_txt,
    construir_grafo,
    salvar_lista_adjacencia,
    ordem_tamanho,
    vertices_isolados,
    graus_saida_entrada,
    grafo_euleriano
)

def main():
    # Etapa 1: Buscar arquivos
    caminho = "/home/est.igor/grafos/grafos/Amostra Enron - 2016"
    arquivos = buscar_arquivos_txt(caminho)
    print(f"{len(arquivos)} arquivos encontrados.")

    # Etapa 2: Construir grafo
    grafo = construir_grafo(arquivos)
    print("Grafo construído.")

    # Etapa 3: Salvar lista de adjacência
    salvar_lista_adjacencia(grafo, "grafo_adjacencia.txt")
    print("Lista de adjacência salva.")

    # Etapa 4: Estatísticas
    ordem, tamanho = ordem_tamanho(grafo)
    print(f"Ordem: {ordem}, Tamanho: {tamanho}")

    isolados = vertices_isolados(grafo)
    print(f"Vértices isolados: {len(isolados)}")

    top_saida, top_entrada = graus_saida_entrada(grafo)
    print("Top 20 grau de saída:", top_saida[:5])
    print("Top 20 grau de entrada:", top_entrada[:5])

    # Etapa 5: Verificar se é Euleriano
    euleriano, msg = grafo_euleriano(grafo)
    print("Euleriano?", euleriano)
    if not euleriano:
        print(msg)

if __name__ == "__main__":
    main()