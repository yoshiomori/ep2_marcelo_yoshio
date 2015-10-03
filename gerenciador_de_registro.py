# coding=utf-8

# Um registro é lista com 5 elementos cujo primeiro elemento é o nome do processo, segundo elemento
# é a posição inicial da região na memória, terceiro elemento é o tamanho da região, quarto elemento é uma
# referencia para o registro da região anterior e ultimo elemento é uma referencia para o registro da região posterior


class Registro(object):
    registros = []
    registro = None

    def __init__(self, tamanho):
        self.registros.append(None)  # Não tem nome
        self.registros.append(0)  # Posição inicial
        self.registros.append(tamanho)  # Tamanho inicial
        self.registros.append(self.registros)  # lista anterior (lista circular)
        self.registros.append(self.registros)  # lista posterior (lista circular)

    # Essa função recebe como o argumento o nome e o tamanho do processo
    def first_fit(self, nome, tamanho):
        self.registro = self.registros
        nao_registrado = True
        while nao_registrado:
            try:
                if self.registro[0] is not None or tamanho > self.registro[2]:
                    raise ValueError
                self.registro[0] = nome
                if tamanho < self.registro[2]:
                    self.registro[2], self.registro[4] = tamanho, [None, self.registro[1] + tamanho,
                                                                   self.registro[2] - tamanho,
                                                                   self.registro, self.registro[4]]
                nao_registrado = False
            except ValueError:
                if self.registro[4] != self.registros:
                    self.registro = self.registro[4]  # Passa para o próximo registro quando não consegue
                else:
                    print "Não tem espaço para o processo %s" % nome
                    break

    def remova(self, nome):
        nao_encontrado = True
        auxiliar = self.registros
        while nao_encontrado:
            if auxiliar[0] == nome:
                if auxiliar[0] is None:  # Lança excessão quando tenta-se remover registro que já está livre
                    raise ValueError
                auxiliar[0] = None
                anterior = auxiliar[3]
                posterior = auxiliar[4]
                if posterior != self.registros:
                    if posterior[0] is None:  # Removendo o próximo registro se está livre
                        auxiliar[2] += posterior[2]
                        auxiliar[4] = posterior[4]
                        del posterior[:]
                if anterior != self.registros:
                    if anterior[0] is None:  # Removendo o registro anterior se está livre
                        anterior[2] += auxiliar[2]
                        anterior[4] = posterior
                        del auxiliar[:]
                nao_encontrado = False
            auxiliar = auxiliar[4]
            if auxiliar == self.registros:
                print "Processo %s não foi encontrado" % nome
                break


registro = Registro(10)
registro.first_fit("proc1", 3)
registro.first_fit("proc2", 3)
registro.first_fit("proc3", 3)
registro.remova("proc2")
registro.first_fit("proc4", 3)
registro.first_fit("proc5", 1)
print registro.registros
