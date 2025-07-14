import random
from datetime import datetime
from typing import Dict, List, Optional


class SistemaPedagio:
    """Representa o sistema de um pedágio, com tarifas e controle de caixa."""

    def __init__(self):
        """Inicializa o sistema com o caixa vazio."""
        self.tarifas = {
            'moto': 2.50, 'carro': 5.50, 'onibus': 8.00, 'caminhao': 10.00
        }
        self.cedulas = [
            200.00, 100.00, 50.00, 20.00, 10.00, 5.00, 2.00, 1.00,
            0.50, 0.25, 0.10, 0.05, 0.01
        ]
        self.caixa: Dict[float, int] = {}
        self.historico_transacoes: List[Dict] = []

    def abastecer_caixa(self, denominacao: float, quantidade: int):
        """Adiciona uma quantidade de uma cédula ou moeda específica ao caixa."""
        if denominacao in self.cedulas and quantidade > 0:
            self.caixa[denominacao] = self.caixa.get(denominacao, 0) + quantidade

    def remover_do_caixa(self, denominacao: float, quantidade: int) -> bool:
        """Remove uma quantidade de uma cédula ou moeda. Retorna False se não houver o suficiente."""
        if denominacao in self.caixa and self.caixa[denominacao] >= quantidade:
            self.caixa[denominacao] -= quantidade
            if self.caixa[denominacao] == 0:
                del self.caixa[denominacao]
            return True
        return False

    def adicionar_pagamento_ao_caixa(self, valor_pago: float):
        """Adiciona o valor pago ao caixa, decompondo-o em cédulas e moedas padrão."""
        valor_restante = round(valor_pago, 2)
        for d in self.cedulas:
            if valor_restante >= d:
                qtd = int(valor_restante / d)
                if qtd > 0:
                    self.caixa[d] = self.caixa.get(d, 0) + qtd
                    valor_restante -= d * qtd
                    valor_restante = round(valor_restante, 2)

    def coin_change(self, valor_troco: float) -> Optional[Dict[float, int]]:
        """Calcula o troco usando as cédulas e moedas disponíveis no caixa."""
        if valor_troco == 0:
            return {}
        denominacoes_ordenadas = sorted(self.caixa.keys(), reverse=True)
        resultado = {}
        valor_restante = round(valor_troco, 2)
        for d in denominacoes_ordenadas:
            if valor_restante >= d and self.caixa.get(d, 0) > 0:
                qtd_nec = int(valor_restante / d)
                qtd_disp = self.caixa[d]
                qtd_usada = min(qtd_nec, qtd_disp)
                if qtd_usada > 0:
                    resultado[d] = qtd_usada
                    valor_restante -= d * qtd_usada
                    valor_restante = round(valor_restante, 2)
        if abs(valor_restante) < 0.01:
            return resultado
        return None

    def registrar_transacao(self, tipo_veiculo: str, valor_pago: float, valor_troco: float, troco_detalhado: Dict[float, int]):
        transacao = {
            'id': len(self.historico_transacoes) + 1,
            'data_hora': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'tipo_veiculo': tipo_veiculo,
            'tarifa': self.tarifas[tipo_veiculo],
            'valor_pago': valor_pago,
            'valor_troco': valor_troco,
            'troco_detalhado': troco_detalhado
        }
        self.historico_transacoes.append(transacao)

    def obter_historico(self) -> List[Dict]:
        """Retorna o histórico de transações."""
        return self.historico_transacoes.copy()

    def limpar_historico(self):
        self.historico_transacoes = []

    def limpar_caixa(self):
        self.caixa = {}