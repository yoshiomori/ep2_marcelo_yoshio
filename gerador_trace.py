# coding=utf-8
from random import random, randint, choice, shuffle

f = open("trace", "w")
# Gerando os campos total virtual do arquivo trace
total = randint(100, 1000)
virtual = randint(total, 10000)
f.write("%d %d\n" % (total, virtual))

# Gerando os tempos campos t0 e tf para cada linha, o numero de linhas é um valor aleatório entre 1 a 10
# tempo t0 < tf
numero_linhas = randint(1, 10)
tempos = [randint(0, 10) for i in range(0, 2 * numero_linhas)]
tempos.sort(reverse=True)
t0_tf = []
while len(tempos) > 0:
    t0 = tempos.pop()
    tf = choice(tempos)
    tempos.remove(tf)
    t0_tf.append([t0, tf])
t0_tf = [x for x in t0_tf if x[0] != x[1]]
shuffle(t0_tf)

partition = [random() for x in range(len(t0_tf))]
partition = [x / sum(partition) for x in partition]

# para cada linha, onde o numero de linhas é aleatório, indo de 0 a até 10, é gerado os campos de um processo
for i, part in enumerate(partition):
    tt = t0_tf.pop()
    b = randint(1, int(virtual * part))
    f.write("%d %s %d %d " % (tt[0], "teste%d" % i, tt[1], b))
    # Gerando os campos de acesso
    tempo = [randint(tt[0], tt[1]) for ii in range(0, randint(1, 5))]
    tempo.sort()
    # tirando os tempos repetidos
    tempo = list(set(tempo))
    for t in tempo:
        f.write("%d %d " % (randint(0, b), t))
    f.write("\n")
f.close()
