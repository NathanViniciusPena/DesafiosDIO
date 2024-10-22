import textwrap


def menu_principal():
    menu_opcoes = """\n
    ------------- MENU -------------
    [1]\tAdicionar Saldo
    [2]\tRealizar Saque
    [3]\tMostrar Extrato
    [4]\tCadastrar Novo Cliente
    [5]\tMostrar Contas Cadastradas
    [6]\tCadastrar Novo Usuário
    [7]\tSair
    => """
    return input(textwrap.dedent(menu_opcoes))


def adicionar_saldo(saldo_atual, valor_deposito, extrato, /):
    if valor_deposito > 0:
        saldo_atual += valor_deposito
        extrato += f"Depósito:\tR$ {valor_deposito:.2f}\n"
        print("\n--- Saldo adicionado com sucesso! ---")
    else:
        print("\nOperação falhou! O valor informado é inválido.")

    return saldo_atual, extrato


def realizar_saque(*, saldo_atual, valor_saque, extrato, limite_saque, total_saques, limite_saques):
    saldo_insuficiente = valor_saque > saldo_atual
    limite_excedido = valor_saque > limite_saque
    limite_saques_excedido = total_saques >= limite_saques

    if saldo_insuficiente:
        print("\n@@@ Operação falhou! Saldo insuficiente. @@@")

    elif limite_excedido:
        print("\n@@@ Operação falhou! Valor do saque excede o limite. @@@")

    elif limite_saques_excedido:
        print("\n@@@ Operação falhou! Limite de saques atingido. @@@")

    elif valor_saque > 0:
        saldo_atual -= valor_saque
        extrato += f"Saque:\t\tR$ {valor_saque:.2f}\n"
        total_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo_atual, extrato


def mostrar_extrato(saldo_atual, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Nenhuma movimentação realizada." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo_atual:.2f}")
    print("==========================================")


def cadastrar_usuario(lista_usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = filtrar_usuario(cpf, lista_usuarios)

    if usuario_existente:
        print("\n@@@ CPF já cadastrado! @@@")
        return

    nome_completo = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco_completo = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    lista_usuarios.append({"nome": nome_completo, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco_completo})

    print("=== Usuário cadastrado com sucesso! ===")


def filtrar_usuario(cpf, lista_usuarios):
    usuarios_filtrados = [usuario for usuario in lista_usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def cadastrar_conta(agencia, numero_conta, lista_usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, lista_usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado! Processo de criação de conta encerrado. @@@")


def mostrar_contas(lista_contas):
    for conta in lista_contas:
        informacoes_conta = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(informacoes_conta))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite_saque = 500
    extrato = ""
    total_saques = 0
    lista_usuarios = []
    lista_contas = []

    while True:
        opcao = menu_principal()

        if opcao == "1":
            valor_deposito = float(input("Informe o valor do depósito: "))

            saldo, extrato = adicionar_saldo(saldo, valor_deposito, extrato)

        elif opcao == "2":
            valor_saque = float(input("Informe o valor do saque: "))

            saldo, extrato = realizar_saque(
                saldo_atual=saldo,
                valor_saque=valor_saque,
                extrato=extrato,
                limite_saque=limite_saque,
                total_saques=total_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            cadastrar_usuario(lista_usuarios)

        elif opcao == "5":
            numero_conta = len(lista_contas) + 1
            conta = cadastrar_conta(AGENCIA, numero_conta, lista_usuarios)

            if conta:
                lista_contas.append(conta)

        elif opcao == "6":
            mostrar_contas(lista_contas)

        elif opcao == "7":
            break

        else:
            print("Operação inválida. Por favor, escolha uma opção novamente.")


main()

