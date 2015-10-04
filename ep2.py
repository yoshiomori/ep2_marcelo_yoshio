# coding=utf-8
from sys import argv
from simulador import Simulador


simulador = Simulador()
if len(argv) == 2:
    simulador.do_carrega(argv[1])
    simulador.do_espaco("1")
    simulador.do_executa(3)
elif len(argv) == 1:
    simulador.cmdloop()
else:
    print "Programa não lida com essa quantidade de argumentos"