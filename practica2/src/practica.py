import argparse
import random

def leer_ejemplar(path):
    """Lee el archivo que contiene al ejemplar codificado.

    Args:
        path: La ruta del archivo que contiene el ejemplar. El ejemplar
        se codifica utilizando lista de adyacencias. La línea i del archivo
        contiene los ids de los vértices adyacentes al vértice i, separados
        por espacios en blanco.

    Returns:
        Una lista de listas, donde la sublista i contiene los ids de los vértices
        adyacentes a al vértice i y el entero K con el número de colores del ejemplar.
    """
    with open(path) as f:
        # La primera línea contiene el entero k
        k = f.readline()
        lines = f.readlines()
    return [[int(n) for n in l.strip().split(' ') if n] for l in lines], int(k)

def leer_certificado(path):
    with open(path) as f:
        lines = f.readlines()
    return [int(l.strip()) for l in lines]

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

def verificar(ejemplar, certificado, k):
    if max(certificado) > k:
        return False

    for i in range(1, len(ejemplar)+1):
        for vecino in ejemplar[i-1]:
            if certificado[i-1] == certificado[vecino-1]:
                return False
    return True


def generar_certificados(args):
    # Leemos el ejemplar sólo para saber la cantidad de vértices que tendremos y el entero k
    ejemplar, k = leer_ejemplar(args.path)
    num_vertices = contar_vertices(ejemplar)

    nom_salida = args.gen

    string = ""
    for _ in range(num_vertices):
        string = string + str(random.randint(1,k)) + "\n"

    # Creamos el archivo (se sobrescribe si ya existe)
    file = open(nom_salida,'w')
    # Escribimos los colores generados al azar
    file.write(string)

def verificar_certificado(args):
    ejemplar, k = leer_ejemplar(args.path_ejemplar)
    certificado = leer_certificado(args.path_certificado)
    print('Número de Vértices:', contar_vertices(ejemplar))
    print('Número de Aristas:', contar_aristas(ejemplar))
    print('Entero K:', k)
    print('Número colores utilizados (certificado):', max(certificado))
    respuesta = 'SI' if verificar(ejemplar, certificado, k) else 'NO'
    print(f'¿El ejemplar, con el certificado dado, es K={k} coloreable?', respuesta)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Programa para generar y verificar certificados del problema de coloración de gráficas')
    subparsers = parser.add_subparsers()

    g_parser = subparsers.add_parser('generar', description='Genera certificados aleatorios para coloracion')
    g_parser.add_argument('path', help='Ruta del archivo que contiene al ejemplar')
    g_parser.add_argument('gen', help='Ruta del archivo que queremos generar')
    g_parser.set_defaults(func=generar_certificados)

    v_parser = subparsers.add_parser('verificar', description='Verifica si el certificado es válido para el ejemplar')
    v_parser.add_argument('path_ejemplar', help='Ruta del archivo que contiene al ejemplar')
    v_parser.add_argument('path_certificado', help='Ruta del archivo que contiene el certificado del ejemplar')
    v_parser.set_defaults(func=verificar_certificado)

    args = parser.parse_args()
    args.func(args)
