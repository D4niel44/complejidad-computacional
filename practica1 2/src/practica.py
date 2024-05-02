import argparse

def leer_ejemplar(path):
    """Lee el archivo que contiene al ejemplar codificado.

    Args:
        path: La ruta del archivo que contiene el ejemplar. El ejemplar
        se codifica utilizando lista de adyacencias. La línea i del archivo
        contiene los ids de los vértices adyacentes al vértice i, separados
        por espacios en blanco.

    Returns:
        Una lista de listas, donde la sublista i contiene los ids de los vértices
        adyacentes a al vértice i.
    """
    with open(path) as f:
        lines = f.readlines()
    return [[int(n) for n in l.strip().split(' ') if n] for l in lines] 

def contar_vertices(ejemplar):
    """Regresa el número de vértices del ejemplar.

    Args:
        ejemplar: El ejemplar, representado mediante listas de adyacencias.
    """
    return len(ejemplar)

def contar_aristas(ejemplar):
    """Regresa el número de aristas del ejemplar.

    Args:
        ejemplar: El ejemplar, representado mediante listas de adyacencias.
    """
    n_aristas = 0
    for i, vecinos in enumerate(ejemplar):
        for vecino in vecinos:
            # Evita contar dos veces las aristas.
            if vecino > i+1:
                n_aristas += 1
    return n_aristas

def vertice_grado_maximo(ejemplar):
    """Regresa el vértice de grado máximo y su grado. Si hay más de un vértice
    de grado máximo, se regresa el id del primero.

    Args:
        ejemplar: El ejemplar, representado mediante listas de adyacencias.
    """
    grados = [len(v) for v in ejemplar]
    grado_maximo = max(grados)
    return grados.index(grado_maximo) + 1, grado_maximo

def dos_colorear(ejemplar):
    """Regresa una dos-coloración del ejemplar, si el ejemplar es dos-coloreable, o
    None si el ejemplar no se puede colorear con dos colores.

    El algoritmo consiste en ir recorriendo los vértices que no han sido coloreados,
    y realiza un recorrido DFS asignando colores a todos sus vecinos. El algoritmo
    termina cuando ya se hayan asignado colores a todos los vértices del ejemplar. Si
    mientras se realiza el recorrido se encuentra un vecino al que no se le puede asignar
    un color sin que entre en conflicto con algunos de sus vértices adyacentes, se regresa
    None, dado que no es posible colorear el ejemplar con dos colores.

    Args:
        ejemplar: El ejemplar, representado mediante listas de adyacencias.
    """
    coloracion = {}
    for i in range(1, len(ejemplar)+1):
        if i not in coloracion:
            coloracion[i] = 0

            q = [i]
            while q:
                cur = q.pop()
                for vecino in ejemplar[cur-1]:
                    if vecino not in coloracion:
                        coloracion[vecino] = 1 - coloracion[cur]
                        q.append(vecino)
                    elif coloracion[vecino] == coloracion[cur]:
                        return None
    return coloracion

def coloracion_pretty(ejemplar, coloracion):
    """Regresa un cadena con una representación gráfica en forma de tabla de la coloración
    correspondiente al ejemplar. La tabla cuenta con dos columnas, la primera contiene el 
    id del vértice, y la segunda contiene el color asignado al vértice.

    Args:
        ejemplar: El ejemplar, representado mediante listas de adyacencias.
        coloracion: Dos-coloración del ejemplar, representada mediante un diccionario que
        asigna a cada vértice un color.
    """
    s = 'Vértice Color\n'
    for v in range(1, len(ejemplar)+1):
        c = coloracion[v]
        s += f'{v} {c}\n'
    return s
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ejecuta el algoritmo de 2-coloración')
    parser.add_argument('path', help='Ruta del archivo que contiene al ejemplar')
    args = parser.parse_args()

    ejemplar = leer_ejemplar(args.path)
    print('Número de Vértices:', contar_vertices(ejemplar))
    print('Número de Aristas', contar_aristas(ejemplar))
    vertice_grado_maximo, grado_maximo = vertice_grado_maximo(ejemplar)
    print(f'El vértice de grado máximo es {vertice_grado_maximo} y tiene grado {grado_maximo}')
    coloracion = dos_colorear(ejemplar)
    if coloracion:
        print('¿La gráfica del ejemplar es 2-coloreable?: SI')
        print(coloracion_pretty(ejemplar, coloracion))
    else:
        print('¿La gráfica del ejemplar es 2-coloreable?: NO')
    
