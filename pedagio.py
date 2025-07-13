import random
from typing import Optional, Dict

class SistemaPedagio:

    def __init__(self):
        self.tarifas = {
            'moto': 2.50,
            'carro': 5.50,
            'onibus': 8.00,
            'caminhao': 10.00
        }

        self.cedulas = [
            200.00,
            100.00,
            50.00,
            20.00,
            10.00,
            5.00,
            2.00,
            1.00,
            0.50,
            0.25,
            0.10,
            0.05,
            0.01
        ]

        self.caixa = {}
        self.randomizar_caixa()

    def randomizar_caixa(self) -> None:
        print(" Randomizando o caixa...")
        self.caixa = {}

        pesos = {
            200.00: (0, 3),
            100.00: (0, 5),
            50.00: (1, 8),
            20.00: (2, 12),
            10.00: (3, 15),
            5.00: (5, 20),
            2.00: (8, 25),
            1.00: (10, 30),
            0.50: (15, 35),
            0.25: (20, 40),
            0.10: (25, 45),
            0.05: (30, 50),
            0.01: (40, 60)
        }

        for cedula in self.cedulas:
            min_qtd, max_qtd = pesos[cedula]
            quantidade = random.randint(min_qtd, max_qtd)
            if quantidade > 0:
                self.caixa[cedula] = quantidade

        print("Caixa atual:")
        self.mostrar_caixa()

    def mostrar_caixa(self) -> None:
        total = 0
        for denominacao in sorted(self.caixa.keys(), reverse=True):
            quantidade = self.caixa[denominacao]
            subtotal = denominacao * quantidade
            total += subtotal
            print(f"  R$ {denominacao:.2f} x {quantidade} = R$ {subtotal:.2f}")
        print(f"  Total no caixa: R$ {total:.2f}")
        print()


    def coin_change(self, valor_troco: float) -> Optional[Dict[float, int]]:

        if valor_troco == 0:
            return {}

        denominacoes_ordenadas = sorted(self.caixa.keys(), reverse=True)

        resultado = {}
        valor_restante = valor_troco

        for denominacao in denominacoes_ordenadas:
            if valor_restante >= denominacao and self.caixa[denominacao] > 0:
                quantidade_necessaria = int(valor_restante / denominacao)
                quantidade_disponivel = self.caixa[denominacao]
                quantidade_usada = min(quantidade_necessaria, quantidade_disponivel)

                if quantidade_usada > 0:
                    resultado[denominacao] = quantidade_usada
                    valor_restante -= denominacao * quantidade_usada
                    valor_restante = round(valor_restante, 2)

        if abs(valor_restante) < 0.01:
            return resultado
        else:
            return None
        
    def processar_pagamento(self, tipo_veiculo: str, valor_pago: float) -> bool:
        if tipo_veiculo not in self.tarifas:
            print(f" Tipo de veículo inválido: {tipo_veiculo}")
            return False

        tarifa = self.tarifas[tipo_veiculo]

        print(f" Veículo: {tipo_veiculo.capitalize()}")
        print(f" Tarifa: R$ {tarifa:.2f}")
        print(f"Valor pago: R$ {valor_pago:.2f}")

        if valor_pago < tarifa:
            print(f"Valor insuficiente! Faltam R$ {tarifa - valor_pago:.2f}")
            return False

        if valor_pago == tarifa:
            print("Pagamento exato! Sem troco.")
            return True

        valor_troco = round(valor_pago - tarifa, 2)

        print(f" Troco necessário: R$ {valor_troco:.2f}")

        troco = self.coin_change(valor_troco)

        if troco is None:
            print(" Não é possível dar o troco! Caixa insuficiente.")
            return False

        print(" Troco calculado:")
        total_moedas = 0
        for denominacao in sorted(troco.keys(), reverse=True):
            quantidade = troco[denominacao]
            total_moedas += quantidade
            print(f"  R$ {denominacao:.2f} x {quantidade}")

        print(f" Total de moedas/notas no troco: {total_moedas}")

        for denominacao, quantidade in troco.items():
            self.caixa[denominacao] -= quantidade

        return True

    def mostrar_tarifas(self) -> None:
        print(" Tarifas do Pedágio:")
        for veiculo, tarifa in self.tarifas.items():
            print(f"  {veiculo.capitalize()}: R$ {tarifa:.2f}")
        print()


def main():
    sistema = SistemaPedagio()

    print("=" * 50)
    print("  SISTEMA DE PEDÁGIO - COIN CHANGE")
    print("=" * 50)
    print()

    sistema.mostrar_tarifas()


if __name__ == "__main__":
    main()