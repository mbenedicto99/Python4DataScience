print ("teste")
print(23, 23, sep="-")
print(23, 23, sep="-", end="##\n")

entrada = input("Diga SIM ou NAO")
print ("\n\n")

#if entrada == "SIM":
#    print("Voce disse SIM")
#elif entrada -- "NAO":
#    print("Voce disse NAO")
#else:
#    print("Voce nao escolheu uma opcao")
#

for i in range(1, 4):
    print (i)

if entrada == 'SIM':
    print(f'{entrada=}')

print("#####################")
entrada = input("[E]ntrar - [S]air:")
senha = input('Senha: ')

senha_per = '1234'

if entrada == 'E' and senha == senha_per:
    print ("Entrada permitida")
else:
    print ("Entrada Recusada")