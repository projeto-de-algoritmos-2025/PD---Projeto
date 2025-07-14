# app.py

from flask import Flask, render_template
from pedagio import SistemaPedagio

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Cria uma instância do nosso sistema de pedágio
sistema = SistemaPedagio()

# Define a rota principal da aplicação
@app.route('/')
def index():
    """Esta função é chamada quando alguém acessa a página inicial."""
    # O Flask irá procurar por 'index.html' dentro da pasta 'templates'
    return render_template('index.html')

# Executa o servidor quando o script é iniciado diretamente
if __name__ == '__main__':
    # debug=True faz com que o servidor reinicie automaticamente após cada alteração
    app.run(debug=True)