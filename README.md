# Sistema de Simulação de Pedágio - Projeto de Algoritmo

## 📖 Sobre o Projeto

Este projeto é um simulador de um sistema de pagamento de pedágio, desenvolvido como uma aplicação web que roda localmente. Ele demonstra a lógica por trás do cálculo de tarifas, processamento de pagamentos e, mais importante, a solução para o "problema do troco" (*Coin Change Problem*) de forma interativa.


## 👥 Autores

| Nome             | Matrícula   |
| ---------------- | ----------- |
| Caio Mesquita    | 222024283   |
| Manoel Teixeira  | 211041240   |

## ✨ Funcionalidades Principais

* **Interface Web Interativa:** Frontend construído com HTML, CSS e JavaScript para uma experiência de usuário rica e visual.
* **Cálculo de Tarifas:** Sistema de tarifas pré-definidas para diferentes tipos de veículos (`moto`, `carro`, `ônibus`, `caminhão`).
* **Processamento de Pagamento:** Lógica completa para aceitar pagamentos, validar o valor e calcular o troco.
* **Algoritmo de Troco (Coin Change):** Implementação de um algoritmo guloso para determinar a combinação ótima de notas e moedas para o troco, com base no que está disponível no caixa.
* **Gerenciamento Manual do Caixa:**
    * **Abastecimento:** Adicione qualquer quantidade de cédulas e moedas padrão ao caixa.
    * **Remoção:** Retire valores específicos do caixa.
    * **Limpeza:** Esvazie completamente o caixa com um único clique.


---

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    * ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
* **Frontend:**
    * ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
    * ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
    * ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para rodar a aplicação em sua máquina local.

### Pré-requisitos

* **Python 3** instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/).

### Passos para Instalação

1.  **Clone ou Baixe o Repositório**
    Faça o download dos arquivos do projeto e descompacte-os em uma pasta de sua preferência.


2.  **Instale as Dependências**
    Instale o Flask, que é a única dependência do projeto:
    ```bash
    pip install Flask
    ```

3.  **Execute a Aplicação**
    Ainda no terminal, execute o script principal do backend:
    ```bash
    python app.py
    ```
    O terminal exibirá uma mensagem indicando que o servidor está rodando, geralmente no endereço `http://127.0.0.1:5000`.

4.  **Acesse no Navegador**
    Abra seu navegador de internet preferido e acesse a URL:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🕹️ Como Usar a Aplicação

1.  **Abasteça o Caixa:**
    * A aplicação inicia com o caixa vazio. Utilize o painel **"Gerenciar Caixa"** à direita.
    * Selecione uma cédula/moeda (ex: R$ 10,00).
    * Digite a quantidade (ex: 20).
    * Clique no botão **"Abastecer"**.
    * Repita para várias denominações até que o caixa tenha saldo suficiente.

2.  **Processe um Pagamento:**
    * No painel **"Pagamento"** à esquerda, selecione um tipo de veículo. A tarifa será exibida no campo de destaque.
    * Digite o valor que o "motorista" pagou no campo "Valor Pago".
    * Clique em **"Processar Pagamento"**.

3.  **Verifique os Resultados:**
    * O painel **"Resultado"** mostrará se o pagamento foi bem-sucedido e os detalhes do troco.
    * O painel **"Situação do Caixa"** será atualizado automaticamente, mostrando a entrada do dinheiro e a saída do troco.

## Apresentação
Link para apresentação: [clique aqui](https://youtu.be/CDZ6RU4Wb6o)
