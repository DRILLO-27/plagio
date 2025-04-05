from similitud import procesar_documentos, calcular_similitudes, mostrar_porcentajes, graficar_grafo

def main():
    documentos_path = "documentos"
    print("Procesando documentos...")
    mapa_documentos = procesar_documentos(documentos_path)
    similitudes = calcular_similitudes(mapa_documentos)
    mostrar_porcentajes(similitudes)
    graficar_grafo(similitudes)

if __name__ == "__main__":
    main()
