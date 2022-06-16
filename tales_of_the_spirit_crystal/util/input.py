def leiaint(num):
    while True:
        n = input(num)
        if n.isnumeric() is False:
            print('\033[1;3;31mERROR! Digite um numero inteiro válido.\033[m')
        else:
            return int(n)


def linha(tam=75):
    print("-=" * tam)


def cabecalho(txt):
    linha()
    print(txt.center(150))
    linha()
