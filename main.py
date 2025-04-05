import sys
from similitud import (
    procesar_documentos,
    calcular_similitudes,
    mostrar_porcentajes,
    graficar_grafo,
    generar_tabla_hash
)

def main():
    sys.stdout = open("salida_terminal.txt", "w", encoding="utf-8")

    documentos_path = "documentos"
    print("Procesando documentos...")
    mapa_documentos = procesar_documentos(documentos_path)
    similitudes = calcular_similitudes(mapa_documentos)
    mostrar_porcentajes(similitudes)
    graficar_grafo(similitudes)

    print("\n🗃 TABLA HASH DE N-GRAMAS\n")
    tabla_hash = generar_tabla_hash(documentos_path)
    for hash_val, ocurrencias in tabla_hash.items():
        print(f"{hash_val}: {ocurrencias}")


if __name__ == "__main__":
    main()
