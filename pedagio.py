import random

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
