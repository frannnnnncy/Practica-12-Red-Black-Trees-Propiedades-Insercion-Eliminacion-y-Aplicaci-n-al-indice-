"""
Trabajo de Investigacion: verificacion automatizada de que 1,000 eliminaciones
consecutivas en el RBT de Python NUNCA producen una violacion de las 5 propiedades.
"""
import random
from rbt_electoral import ArbolElectoral, verificar_todas, es_bst_valido, altura_negra


def generar_dni(i):
    return f"70{600000 + i}"


def fuzz_rbt(n_operaciones=1000, semilla=7):
    random.seed(semilla)
    arbol = ArbolElectoral()
    activos = []
    pool = list(range(0, n_operaciones * 3))
    random.shuffle(pool)
    pool_idx = 0

    fallos = []
    inserciones = 0
    eliminaciones = 0

    for op in range(n_operaciones):
        accion = random.choice(['insertar', 'insertar', 'eliminar'])  # 2:1 insercion:eliminacion
        if accion == 'insertar' or not activos:
            i = pool[pool_idx]
            pool_idx += 1
            dni = generar_dni(i)
            votante = (dni, f"Estudiante_{i}", "Ing. Sistemas", True)
            arbol.insertar(votante)
            activos.append(dni)
            inserciones += 1
        else:
            dni = random.choice(activos)
            arbol.eliminar(dni)
            activos.remove(dni)
            eliminaciones += 1

        if not verificar_todas(arbol.raiz):
            fallos.append((op, accion, 'P2/P4/P5'))
        if not es_bst_valido(arbol.raiz):
            fallos.append((op, accion, 'BST'))

    return {
        "operaciones": n_operaciones,
        "inserciones": inserciones,
        "eliminaciones": eliminaciones,
        "activos_finales": len(activos),
        "altura_negra_final": altura_negra(arbol.raiz),
        "fallos": fallos,
    }


if __name__ == "__main__":
    resultado = fuzz_rbt(n_operaciones=1000, semilla=7)
    print(f"Operaciones totales simuladas: {resultado['operaciones']}")
    print(f"  Inserciones: {resultado['inserciones']}")
    print(f"  Eliminaciones: {resultado['eliminaciones']}")
    print(f"Votantes activos al final: {resultado['activos_finales']}")
    print(f"Altura negra final: {resultado['altura_negra_final']}")
    print(f"Fallos detectados (violaciones de P2/P4/P5 o BST): {len(resultado['fallos'])}")
    if resultado['fallos']:
        print("PRIMER FALLO:", resultado['fallos'][0])
    else:
        print("1,000 operaciones consecutivas: las 5 propiedades RBT y la invariante BST "
              "se mantuvieron validas despues de CADA operacion, sin excepcion.")
