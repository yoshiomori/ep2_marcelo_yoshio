# coding=utf-8
import random

f = open("trace", "w")
# Gerando os campos total virtual do arquivo trace
total = random.randint(100, 700)
virtual = random.randint(total, 1000)
f.write("%d %d\n" % (total, virtual))

# Gerando os tempos campos t0 e tf para cada linha, o numero de linhas é um valor aleatório entre 1 a 10
# tempo t0 < tf
numero_linhas = random.randint(1, 10)
tempos = [random.randint(0, 10) for i in range(0, 2 * numero_linhas)]
tempos.sort(reverse=True)
t0_tf = []
while len(tempos) > 0:
    t0 = tempos.pop()
    tf = random.choice(tempos)
    tempos.remove(tf)
    t0_tf.append([t0, tf])
t0_tf = [x for x in t0_tf if x[0] != x[1]]
t0_tf.reverse()

# para cada linha, onde o numero de linhas é aleatório, indo de 0 a até 10, é gerado os campos de um processo
for i in range(0, len(t0_tf)):
    tt = t0_tf.pop()
    b = random.randint(1, 10)
    f.write("%d %s %d %d " % (tt[0], "teste%d" % i, tt[1], b))
    # Gerando os campos de acesso
    tempo = [random.randint(tt[0], tt[1]) for ii in range(0, random.randint(1, 5))]
    tempo.sort()
    # tirando os tempos repetidos
    tempo = list(set(tempo))
    for t in tempo:
        f.write("%d %d " % (random.randint(0, b), t))
    f.write("\n")
f.close()
