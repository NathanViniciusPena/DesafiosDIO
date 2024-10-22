from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def processar_transacao(self, conta, operacao):
        operacao.executar(conta)

    def adicionar_conta(self, nova_conta):
        self.contas.append(nova_conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, titular):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._titular = titular
        self._historico = Historico()

    @classmethod
    def criar_conta(cls, titular, numero):
        return cls(numero, titular)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def titular(self):
        return self._titular

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para saque. @@@")
            return False
        if valor > self.saldo:
            print("\n@@@ Saldo insuficiente para realizar o saque. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque efetuado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para depósito. @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, titular, limite=500, limite_saques=3):
        super().__init__(numero, titular)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        total_saques = len([op for op in self.historico.transacoes if op["tipo"] == "Saque"])

        if valor > self.limite:
            print("\n@@@ Saque não permitido, valor acima do limite. @@@")
            return False

        if total_saques >= self.limite_saques:
            print("\n@@@ Limite de saques diários atingido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"Agência: {self.agencia}\nConta: {self.numero}\nTitular: {self.titular.nome}"


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def registrar_transacao(self, operacao):
        self._transacoes.append(
            {
                "tipo": operacao.__class__.__name__,
                "valor": operacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Operacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def executar(self, conta):
        pass


class Saque(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def executar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.registrar_transacao(self)


class Deposito(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def executar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.registrar_transacao(self)
