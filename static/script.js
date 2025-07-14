// Espera o documento HTML ser completamente carregado para executar o código
document.addEventListener('DOMContentLoaded', () => {

    // Mapeia os elementos do HTML para variáveis JavaScript
    const vehicleSelect = document.getElementById('vehicle-type');
    // APONTA PARA O NOVO ELEMENTO DE TARIFA
    const tariffDisplay = document.getElementById('tariff-display'); 
    const amountPaidInput = document.getElementById('amount-paid');
    const payButton = document.getElementById('pay-button');
    const resultMessageDiv = document.getElementById('result-message');
    const cashBoxStatusPre = document.getElementById('cash-box-status');
    const cashDenominationSelect = document.getElementById('cash-denomination');
    const cashQuantityInput = document.getElementById('cash-quantity');
    const addCashButton = document.getElementById('add-cash-button');
    const removeCashButton = document.getElementById('remove-cash-button');

    let currentRates = {}; // Armazena as tarifas carregadas

    // --- FUNÇÕES DE API ---

    /**
     * Busca as tarifas da API e preenche o menu de seleção de veículos.
     */
    async function carregarTarifas() {
        try {
            const response = await fetch('/api/tarifas');
            currentRates = await response.json();
            
            vehicleSelect.innerHTML = '<option value="">-- Selecione --</option>';
            for (const veiculo in currentRates) {
                const option = document.createElement('option');
                option.value = veiculo;
                option.textContent = veiculo.charAt(0).toUpperCase() + veiculo.slice(1);
                vehicleSelect.appendChild(option);
            }
        } catch (error) {
            console.error('Falha ao carregar tarifas:', error);
            vehicleSelect.innerHTML = '<option value="">Erro ao carregar</option>';
        }
    }

    /**
     * Busca a lista de denominações para o painel de gerenciamento.
     */
    async function carregarDenominacoes() {
        try {
            const response = await fetch('/api/cedulas');
            const cedulas = await response.json();
            
            cashDenominationSelect.innerHTML = '<option value="">-- Selecione --</option>';
            // Ordena da maior para a menor
            cedulas.sort((a, b) => b - a).forEach(cedula => {
                const option = document.createElement('option');
                option.value = cedula;
                option.textContent = `R$ ${cedula.toFixed(2)}`;
                cashDenominationSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Falha ao carregar denominações:', error);
        }
    }

    /**
     * Busca o estado atual do caixa na API e exibe na tela.
     */
    async function atualizarCaixa() {
        try {
            const response = await fetch('/api/caixa');
            const caixa = await response.json();
            const sortedDenominations = Object.keys(caixa).map(parseFloat).sort((a, b) => b - a);
            
            if (sortedDenominations.length === 0) {
                cashBoxStatusPre.textContent = 'Caixa Vazio';
                return;
            }

            const statusText = sortedDenominations.map(denom => {
                const valor = denom.toFixed(2).toString().padStart(7, ' ');
                const quantidade = caixa[denom] || 0;
                return `R$ ${valor} x ${quantidade}`;
            }).join('\n');
            
            cashBoxStatusPre.textContent = statusText;
        } catch (error) {
            console.error('Falha ao carregar caixa:', error);
            cashBoxStatusPre.textContent = 'Erro ao carregar o estado do caixa.';
        }
    }

    /**
     * Envia uma requisição para a API para gerenciar o caixa (adicionar/remover).
     */
    async function gerenciarCaixa(action) {
        const denominacao = cashDenominationSelect.value;
        const quantidade = cashQuantityInput.value;

        if (!denominacao || !quantidade || parseInt(quantidade) <= 0) {
            alert('Selecione uma denominação e uma quantidade válida.');
            return;
        }

        try {
            const response = await fetch(`/api/caixa/${action}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ denominacao, quantidade })
            });
            const result = await response.json();

            alert(result.mensagem); // Mostra um alerta com o resultado
            if(result.sucesso) {
                atualizarCaixa(); // Atualiza a exibição do caixa
                cashQuantityInput.value = ''; // Limpa o campo de quantidade
            }
        } catch (error) {
            console.error(`Erro ao ${action} caixa:`, error);
            alert('Erro de comunicação com o servidor.');
        }
    }

    /**
     * Envia os dados de pagamento para a API e exibe o resultado.
     */
    async function processarPagamento() {
        // Lógica de pagamento existente...
    }

    // --- EVENT LISTENERS ---

    // Quando o usuário muda o veículo, ATUALIZA O NOVO CAMPO DE TARIFA
    vehicleSelect.addEventListener('change', () => {
        const selectedVehicle = vehicleSelect.value;
        if (selectedVehicle && currentRates[selectedVehicle]) {
            tariffDisplay.textContent = `R$ ${currentRates[selectedVehicle].toFixed(2)}`;
        } else {
            tariffDisplay.textContent = 'R$ 0.00';
        }
    });
    
    payButton.addEventListener('click', processarPagamento);
    addCashButton.addEventListener('click', () => gerenciarCaixa('abastecer'));
    removeCashButton.addEventListener('click', () => gerenciarCaixa('remover'));

    // --- Carregamento inicial ---
    
    function inicializarPainel() {
        carregarTarifas();
        carregarDenominacoes();
        atualizarCaixa();
    }

    inicializarPainel();
});

