from grafos import (
    buscar_arquivos_txt,
    construir_grafo,
    salvar_lista_adjacencia,
    ordem_tamanho,
    vertices_isolados,
    graus_saida_entrada,
    grafo_euleriano,
    salvar_lista_compactada,
    vertices_ate_distancia,
    calcular_diametro
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
    salvar_lista_compactada(grafo, "grafo_compactado.txt")
    print("Lista de adjacência compactada salva.")

    # Etapa 4: Estatísticas
    ordem, tamanho = ordem_tamanho(grafo)
    print(f"Ordem: {ordem}, Tamanho: {tamanho}")

    isolados = vertices_isolados(grafo)
    print(f"Vértices isolados: {len(isolados)}")

    top_saida, top_entrada = graus_saida_entrada(grafo)
    print("Top 20 grau de saída:", top_saida[:20])
    print("Top 20 grau de entrada:", top_entrada[:5])

    # Etapa 5: Verificar se é Euleriano
    caminho_saida_euleriano = "resultado_euleriano.txt"
    grafo_euleriano(grafo, caminho_saida_euleriano)
        
    # Etapa 6: Calcular diâmetro   
    diametro, caminho = calcular_diametro(grafo)
    print(f"Diâmetro do grafo: {diametro}")
    print("Caminho correspondente:")
    for v in caminho:
        print(" ->", v)
        
    # Etapa 7: Verificar vértices até distância
    origem = str(input("Digite o vértice de origem: "))
    limite = int(input("Digite o limite de distância: "))
    alcance = vertices_ate_distancia(grafo, origem, limite)
    print(f"Vértices até distância {limite} de {origem}:")
    for vertice in alcance:
        print(" -", vertice)
     

if __name__ == "__main__":
    main()