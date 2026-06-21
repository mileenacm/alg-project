import random as rand

tam_matrix = ""

while type(tam_matrix) != int:
    try:
        tam_matrix = int(input('Tamanho da matriz referência: '))
    except ValueError:
        print("Escolha um número inteiro")


def formarMatriz(tam_matrix):
    mat_ref = [[0 for _ in range(tam_matrix)] for _ in range(tam_matrix)]

    for i in range(tam_matrix):
        for j in range(tam_matrix):
            if i < j:
                distancia = rand.randint(1, 100)
                mat_ref[i][j] = distancia
                mat_ref[j][i] = distancia

    return mat_ref


minha_matriz = formarMatriz(tam_matrix)

print("\nMatriz Gerada:")
for linha in minha_matriz:
    print(linha)

