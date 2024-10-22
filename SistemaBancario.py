menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
-> """

s = 0
l = 500
extrato = ""
n_saques = 0
limite_s = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            s += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        exc_sal = valor > s

        exc_lim = valor > l

        exc_saq = n_saques >= limite_s

        if exc_sal:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif exc_lim:
            print("Operação falhou! O valor do saque excede o limite.")

        elif exc_saq:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            s -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            n_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {s:.2f}")
        print("==========================================")

    elif opcao == "4":
        print("Obrigado por usar nossos serviços!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
