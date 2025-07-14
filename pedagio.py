import random
from typing import Optional, Dict

class SistemaPedagio:
    """Representa o sistema de um pedágio, com tarifas e controle de caixa."""

    def __init__(self):
        """Inicializa o sistema com tarifas pré-definidas e um caixa randomizado."""
        
        # Define as tarifas para cada tipo de veículo.
        self.tarifas = {
            'moto': 2.50,
            'carro': 5.50,
            'onibus': 8.00,
            'caminhao': 10.00
        }

        # Lista com todas as denominações de cédulas e moedas brasileiras.
        self.cedulas = [
            200.00, 100.00, 50.00, 20.00, 10.00, 5.00, 2.00, 1.00,
            0.50, 0.25, 0.10, 0.05, 0.01
        ]

        # O caixa armazena a quantidade de cada cédula/moeda. É um dicionário.
        self.caixa = {}
        self.randomizar_caixa()

    def randomizar_caixa(self) -> None:
        """Preenche o caixa com uma quantidade aleatória de cada cédula e moeda."""
        self.caixa = {}

        # Define a quantidade mínima e máxima para cada denominação no caixa.
        pesos = {
            200.00: (0, 3), 100.00: (0, 5), 50.00: (1, 8),
            20.00: (2, 12), 10.00: (3, 15), 5.00: (5, 20),
            2.00: (8, 25), 1.00: (10, 30), 0.50: (15, 35),
            0.25: (20, 40), 0.10: (25, 45), 0.05: (30, 50),
            0.01: (40, 60)
        }

        for cedula in self.cedulas:
            min_qtd, max_qtd = pesos[cedula]
            quantidade = random.randint(min_qtd, max_qtd)
            if quantidade > 0:
                self.caixa[cedula] = quantidade

    def coin_change(self, valor_troco: float) -> Optional[Dict[float, int]]:
        """
        Calcula o troco usando as cédulas e moedas disponíveis no caixa.
        
        Este método utiliza um algoritmo guloso (greedy), começando pelas maiores
        denominações, para encontrar a combinação de notas e moedas para o troco.
        
        Retorna um dicionário com o troco ou None se não for possível.
        """
        if valor_troco == 0:
            return {}

        # Ordena as denominações da maior para a menor para a abordagem gulosa.
        denominacoes_ordenadas = sorted(self.caixa.keys(), reverse=True)
        resultado = {}
        valor_restante = round(valor_troco, 2)

        for denominacao in denominacoes_ordenadas:
            # Verifica se a denominação pode ser usada e se está disponível no caixa.
            if valor_restante >= denominacao and self.caixa.get(denominacao, 0) > 0:
                
                # Calcula quantas notas/moedas são necessárias e quantas estão disponíveis.
                quantidade_necessaria = int(valor_restante / denominacao)
                quantidade_disponivel = self.caixa[denominacao]
                
                # Usa a menor quantidade entre o necessário e o disponível.
                quantidade_usada = min(quantidade_necessaria, quantidade_disponivel)

                if quantidade_usada > 0:
                    resultado[denominacao] = quantidade_usada
                    valor_restante -= denominacao * quantidade_usada
                    
                    # Arredonda para evitar problemas de precisão com ponto flutuante.
                    valor_restante = round(valor_restante, 2)

        # Se o valor restante for zero (com uma pequena tolerância), o troco foi encontrado.
        # Retorna o resultado ou None se não foi possível compor o troco exato.
        if abs(valor_restante) < 0.01:
            return resultado
        else:
            return None