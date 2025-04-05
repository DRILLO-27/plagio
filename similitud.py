import os
import re
import itertools
import hashlib
import networkx as nx
import matplotlib.pyplot as plt

N_GRAMA = 3
TOP_N = 10

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"[^a-z\d\s]", "", texto)
    return texto

def obtener_ngrama(tokens, n=N_GRAMA):
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def hash_ngramas(ngr):
    return hashlib.md5(ngr.encode()).hexdigest()

def procesar_documento(path):
    with open(path, "r", encoding="utf-8") as f:
        contenido = f.read()
    limpio = limpiar_texto(contenido)
    tokens = limpio.split()
    ngramas = obtener_ngrama(tokens)
    return set([hash_ngramas(ng) for ng in ngramas])

def procesar_documentos(documentos_path):
    documentos = [f for f in os.listdir(documentos_path) if f.endswith(".txt")]
    mapa_documentos = {}
    for doc in documentos:
        ruta = os.path.join(documentos_path, doc)
        mapa_documentos[doc] = procesar_documento(ruta)
    return mapa_documentos

def similitud_jaccard(set1, set2):
    if not set1 or not set2:
        return 0.0
    inter = len(set1 & set2)
    union = len(set1 | set2)
    return inter / union

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    izquierda = merge_sort(arr[:mid])
    derecha = merge_sort(arr[mid:])
    return merge(izquierda, derecha)

def merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i][2] > der[j][2]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def calcular_similitudes(mapa_documentos):
    pares = list(itertools.combinations(mapa_documentos.keys(), 2))
    similitudes = []
    for doc1, doc2 in pares:
        set1 = mapa_documentos[doc1]
        set2 = mapa_documentos[doc2]
        sim = similitud_jaccard(set1, set2)
        similitudes.append((doc1, doc2, sim))
    return merge_sort(similitudes)

def mostrar_porcentajes(similitudes):
    print("\n\U0001F4CA PORCENTAJE DE PLAGIO ENTRE DOCUMENTOS\n")
    for doc1, doc2, score in similitudes:
        porcentaje = round(score * 100, 2)
        print(f"{doc1} <--> {doc2} : {porcentaje}%")

def graficar_grafo(similitudes, min_similitud=0.05):
    G = nx.Graph()
    print("\nAgregando aristas al grafo:")
    for doc1, doc2, score in similitudes[:TOP_N]:
        if score >= min_similitud:
            porcentaje = round(score * 100, 2)
            print(f"{doc1} <-> {doc2} = {porcentaje}%")
            G.add_edge(doc1, doc2, weight=porcentaje)

    if not G.edges:
        print("\u26A0\uFE0F No hay suficientes similitudes para graficar. Reduce el umbral o revisá los datos.")
        return

    pos = nx.spring_layout(G, seed=42)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2500)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')
    edge_labels = {(u, v): f"{G[u][v]['weight']}%" for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9)
    plt.title("\U0001F517 Grafo de Similitud de Documentos", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
