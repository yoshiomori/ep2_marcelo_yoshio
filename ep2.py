# coding=utf-8
from sys import argv
from simulador import Simulador


simulador = Simulador()
if len(argv) == 2:
    simulador.do_carrega(argv[1])
elif len(argv) == 1:
    simulador.cmdloop()
else:
    print "Programa não lida com essa quantidade de argumentos"