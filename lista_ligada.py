# coding=utf-8

# Gerenciador de processo inicialmente
lista_ligada = [None, 0, 10, None, None]

# Registrando que o processo de nome proc1 e de tamanho 3 unidades vai ocupar uma região da memória de posição inicial
# lista_ligada[1].
# Se a região da memória registrada por lista_ligada ocupar mais espaço do que o tamanho do proc1 então o registro de
# proc1 estará entre as regiões registradas por lista_ligada[3] e lista_ligada atualizada da forma especificada abaixo
# senão se a lista_ligada[3] for igual à 3 então lista_ligada é registrada para o proc1
# senão não é possível fazer a inserção
nome = "proc1"
tamanho = 3  # unidades
if tamanho < lista_ligada[2]:
    lista_auxiliar = [nome, 0, tamanho, None, None] # Criando novo processo de tamanho 3 unidades
    lista_auxiliar[1] = lista_ligada[1]  # Atualiza posição inicial da lista do quadro de página do processo
    lista_auxiliar[3] = lista_ligada[3]  # Atualiza lista anterior da lista do quadro de página do novo processo
    lista_auxiliar[4] = lista_ligada  # Atualiza a próxima lista da lista do quadro de página do novo processo
    lista_ligada[1] += lista_auxiliar[2]  # Atualiza a posição inicial da lista do quadro de página livre
    lista_ligada[2] -= lista_auxiliar[2]  # Atualiza a quantidade de unidades da lista do quadro de página livre
    lista_ligada[3] = lista_auxiliar  # Atualiza a lista anterior da lista do quadro de página livre
    lista_ligada = lista_auxiliar
elif tamanho == lista_ligada[2]:
    lista_ligada[0] = nome
else:
    raise Exception