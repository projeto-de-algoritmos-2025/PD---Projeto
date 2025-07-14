from flask import Flask, jsonify, render_template, request

from pedagio import SistemaPedagio

app = Flask(__name__)
sistema = SistemaPedagio()

@app.route('/')
def index():
    return render_template('index.html')

# --- ROTAS DE DADOS ---
@app.route('/api/tarifas', methods=['GET'])
def get_tarifas():
    return jsonify(sistema.tarifas)

@app.route('/api/caixa', methods=['GET'])
def get_caixa():
    return jsonify(sistema.caixa)

@app.route('/api/cedulas', methods=['GET'])
def get_cedulas():
    return jsonify(sistema.cedulas)

# --- ROTAS DE AÇÃO ---
@app.route('/api/caixa/abastecer', methods=['POST'])
def api_abastecer_caixa():
    # (código inalterado)
    dados = request.get_json()
    try:
        denominacao = float(dados['denominacao'])
        quantidade = int(dados['quantidade'])
        if quantidade <= 0: raise ValueError("Quantidade deve ser positiva")
    except (ValueError, KeyError, TypeError):
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos.'}), 400
    sistema.abastecer_caixa(denominacao, quantidade)
    return jsonify({'sucesso': True, 'mensagem': f'{quantidade}x de R$ {denominacao:.2f} adicionadas ao caixa.'})

@app.route('/api/caixa/remover', methods=['POST'])
def api_remover_do_caixa():
    # (código inalterado)
    dados = request.get_json()
    try:
        denominacao = float(dados['denominacao'])
        quantidade = int(dados['quantidade'])
        if quantidade <= 0: raise ValueError("Quantidade deve ser positiva")
    except (ValueError, KeyError, TypeError):
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos.'}), 400
    sucesso = sistema.remover_do_caixa(denominacao, quantidade)
    if sucesso:
        return jsonify({'sucesso': True, 'mensagem': f'{quantidade}x de R$ {denominacao:.2f} removidas do caixa.'})
    else:
        return jsonify({'sucesso': False, 'mensagem': 'Não há cédulas/moedas suficientes para remover.'})

@app.route('/api/caixa/limpar', methods=['POST'])
def api_limpar_caixa():
    """Endpoint para esvaziar completamente o caixa."""
    sistema.limpar_caixa()
    return jsonify({'sucesso': True, 'mensagem': 'O caixa foi esvaziado com sucesso.'})

@app.route('/api/historico/limpar', methods=['POST'])
def api_limpar_historico():
    """Endpoint para limpar o histórico de transações."""
    sistema.limpar_historico()
    return jsonify({'sucesso': True, 'mensagem': 'O histórico foi limpo com sucesso.'})

@app.route('/api/historico', methods=['GET'])
def get_historico():
    """Retorna o histórico de transações."""
    return jsonify(sistema.obter_historico())

@app.route('/api/pagar', methods=['POST'])
def api_processar_pagamento():
    dados = request.get_json()
    try:
        tipo_veiculo = dados['tipo_veiculo']
        valor_pago = float(dados['valor_pago'])
    except (ValueError, KeyError, TypeError):
        return jsonify({'sucesso': False, 'mensagem': 'Dados de pagamento inválidos.'}), 400

    # Validações
    if tipo_veiculo not in sistema.tarifas:
        return jsonify({'sucesso': False, 'mensagem': 'Tipo de veículo inválido.'}), 400
    tarifa = sistema.tarifas[tipo_veiculo]
    if valor_pago < tarifa:
        return jsonify({'sucesso': False, 'mensagem': f"Valor insuficiente! Faltam R$ {tarifa - valor_pago:.2f}"})

    valor_troco = round(valor_pago - tarifa, 2)
    troco_calculado = sistema.coin_change(valor_troco)

    if troco_calculado is None:
        return jsonify({'sucesso': False, 'mensagem': 'Caixa insuficiente para dar o troco.'})

    # Lógica da Transação (Entrada e Saída)
    sistema.adicionar_pagamento_ao_caixa(valor_pago)
    for denominacao, quantidade in troco_calculado.items():
        sistema.remover_do_caixa(denominacao, quantidade)

    # Registrar transação no histórico
    sistema.registrar_transacao(tipo_veiculo, valor_pago, valor_troco, troco_calculado)

    return jsonify({
        'sucesso': True,
        'mensagem': 'Pagamento realizado com sucesso!',
        'valor_troco': valor_troco,
        'troco_detalhado': troco_calculado
    })

if __name__ == '__main__':
    app.run(debug=True)