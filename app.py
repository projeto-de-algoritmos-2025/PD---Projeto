from flask import Flask, render_template, jsonify, request
from pedagio import SistemaPedagio

app = Flask(__name__)
sistema = SistemaPedagio()

# --- Rota da Página Principal ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Rotas da API de DADOS ---
@app.route('/api/tarifas', methods=['GET'])
def get_tarifas():
    return jsonify(sistema.tarifas)

@app.route('/api/caixa', methods=['GET'])
def get_caixa():
    return jsonify(sistema.caixa)

@app.route('/api/cedulas', methods=['GET'])
def get_cedulas():
    """Fornece a lista de todas as denominações possíveis."""
    return jsonify(sistema.cedulas)

# --- Rotas da API de AÇÕES ---
@app.route('/api/caixa/abastecer', methods=['POST'])
def api_abastecer_caixa():
    dados = request.get_json()
    try:
        denominacao = float(dados['denominacao'])
        quantidade = int(dados['quantidade'])
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
    except (ValueError, KeyError, TypeError):
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos.'}), 400
    
    sistema.abastecer_caixa(denominacao, quantidade)
    return jsonify({'sucesso': True, 'mensagem': 'Caixa abastecido com sucesso!'})

@app.route('/api/caixa/remover', methods=['POST'])
def api_remover_do_caixa():
    dados = request.get_json()
    try:
        denominacao = float(dados['denominacao'])
        quantidade = int(dados['quantidade'])
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
    except (ValueError, KeyError, TypeError):
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos.'}), 400
    
    sucesso = sistema.remover_do_caixa(denominacao, quantidade)
    if sucesso:
        return jsonify({'sucesso': True, 'mensagem': 'Valor removido com sucesso!'})
    else:
        return jsonify({'sucesso': False, 'mensagem': 'Não há cédulas/moedas suficientes para remover.'})

@app.route('/api/pagar', methods=['POST'])
def api_processar_pagamento():
    dados = request.get_json()
    try:
        tipo_veiculo = dados['tipo_veiculo']
        valor_pago = float(dados['valor_pago'])
    except (ValueError, KeyError, TypeError):
        return jsonify({'sucesso': False, 'mensagem': 'Dados de pagamento inválidos.'}), 400

    if tipo_veiculo not in sistema.tarifas:
        return jsonify({'sucesso': False, 'mensagem': 'Tipo de veículo inválido.'}), 400

    tarifa = sistema.tarifas[tipo_veiculo]
    if valor_pago < tarifa:
        return jsonify({'sucesso': False, 'mensagem': f"Valor insuficiente! Faltam R$ {tarifa - valor_pago:.2f}"})

    valor_troco = round(valor_pago - tarifa, 2)
    troco_calculado = sistema.coin_change(valor_troco)

    if troco_calculado is None:
        return jsonify({'sucesso': False, 'mensagem': 'Caixa insuficiente para dar o troco.'})

    # Processa a transação no caixa
    sistema.adicionar_pagamento_ao_caixa(valor_pago)
    
    # --- LINHA CORRIGIDA ---
    # Agora usando um 'for' loop padrão para remover o troco do caixa
    for denominacao, quantidade in troco_calculado.items():
        sistema.remover_do_caixa(denominacao, quantidade)

    return jsonify({
        'sucesso': True,
        'mensagem': 'Pagamento realizado com sucesso!',
        'valor_troco': valor_troco,
        'troco_detalhado': troco_calculado
    })

if __name__ == '__main__':
    app.run(debug=True)