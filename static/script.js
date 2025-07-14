// Espera o documento HTML ser completamente carregado para executar o código
document.addEventListener('DOMContentLoaded', () => {
	// Mapeamento dos Elementos
	const vehicleSelect = document.getElementById('vehicle-type');
	const tariffDisplay = document.getElementById('tariff-display');
	const amountPaidInput = document.getElementById('amount-paid');
	const payButton = document.getElementById('pay-button');
	const resultMessageDiv = document.getElementById('result-message');
	const cashBoxStatusPre = document.getElementById('cash-box-status');
	const cashDenominationSelect = document.getElementById('cash-denomination');
	const cashQuantityInput = document.getElementById('cash-quantity');
	const addCashButton = document.getElementById('add-cash-button');
	const removeCashButton = document.getElementById('remove-cash-button');
	const clearCashButton = document.getElementById('clear-cash-button');

	let currentRates = {};

	// --- Funções de API ---

	async function carregarTarifas() {
		try {
			const response = await fetch('/api/tarifas');
			currentRates = await response.json();
			vehicleSelect.innerHTML = '<option value="">-- Selecione --</option>';
			for (const v in currentRates) {
				const o = document.createElement('option');
				o.value = v;
				o.textContent = v.charAt(0).toUpperCase() + v.slice(1);
				vehicleSelect.appendChild(o);
			}
		} catch (error) {
			console.error('Falha ao carregar tarifas:', error);
		}
	}

	async function carregarDenominacoes() {
		try {
			const response = await fetch('/api/cedulas');
			const cedulas = await response.json();
			cashDenominationSelect.innerHTML =
				'<option value="">-- Selecione --</option>';
			cedulas
				.sort((a, b) => b - a)
				.forEach((c) => {
					const o = document.createElement('option');
					o.value = c;
					o.textContent = `R$ ${c.toFixed(2)}`;
					cashDenominationSelect.appendChild(o);
				});
		} catch (error) {
			console.error('Falha ao carregar denominações:', error);
		}
	}

	/**
	 * CORREÇÃO APLICADA AQUI
	 * Busca o estado atual do caixa na API e exibe na tela de forma robusta.
	 */
	async function atualizarCaixa() {
		try {
			const response = await fetch('/api/caixa');
			const caixa = await response.json(); // Ex: {'5.0': 10, '100.0': 5}

			// Pega as chaves como texto (ex: ['5.0', '100.0'])
			const chavesEmTexto = Object.keys(caixa);

			// Ordena as chaves com base em seu valor numérico
			chavesEmTexto.sort((a, b) => parseFloat(b) - parseFloat(a));

			if (chavesEmTexto.length === 0) {
				cashBoxStatusPre.textContent = 'Caixa Vazio';
				return;
			}

			// Mapeia usando a chave em texto para garantir o acesso correto
			const statusText = chavesEmTexto
				.map((chave) => {
					const valorNumerico = parseFloat(chave);
					const valorFormatado = valorNumerico
						.toFixed(2)
						.toString()
						.padStart(7, ' ');
					// Usa a 'chave' (texto) para acessar o valor, que é a forma correta
					const quantidade = caixa[chave];
					return `R$ ${valorFormatado} x ${quantidade}`;
				})
				.join('\n');

			cashBoxStatusPre.textContent = statusText;
		} catch (error) {
			console.error('Falha ao carregar caixa:', error);
			cashBoxStatusPre.textContent = 'Erro ao carregar caixa.';
		}
	}

	function exibirResultado(sucesso, mensagem, trocoInfo = null) {
		resultMessageDiv.className = sucesso ? 'success' : 'error';
		let html = `<strong>${mensagem}</strong>`;
		if (sucesso && trocoInfo && trocoInfo.valor_troco > 0) {
			html += `<p>Troco a devolver: R$ ${trocoInfo.valor_troco.toFixed(
				2
			)}</p><ul>`;
			for (const [d, q] of Object.entries(trocoInfo.troco_detalhado)) {
				html += `<li>${q}x de R$ ${parseFloat(d).toFixed(2)}</li>`;
			}
			html += `</ul>`;
		}
		resultMessageDiv.innerHTML = html;
	}

	// --- Funções de Ação ---
	async function gerenciarCaixa(action) {
		const denominacao = cashDenominationSelect.value;
		const quantidade = cashQuantityInput.value;
		if (!denominacao || !quantidade || parseInt(quantidade) <= 0) {
			Swal.fire({
				icon: 'warning',
				title: 'Atenção',
				text: 'Selecione uma denominação e uma quantidade válida.',
			});
			return;
		}
		try {
			const response = await fetch(`/api/caixa/${action}`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ denominacao, quantidade }),
			});
			const result = await response.json();
			Swal.fire({
				icon: result.sucesso ? 'success' : 'error',
				title: result.sucesso ? 'Sucesso' : 'Erro',
				text: result.mensagem,
			});
			if (result.sucesso) {
				atualizarCaixa();
				cashQuantityInput.value = '';
			}
		} catch (error) {
			Swal.fire({
				icon: 'error',
				title: 'Erro',
				text: 'Erro de comunicação com o servidor.',
			});
		}
	}

	async function limparCaixa() {
		const confirm = await Swal.fire({
			title: 'Tem certeza?',
			text: 'Deseja realmente esvaziar o caixa?',
			icon: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#3085d6',
			cancelButtonColor: '#d33',
			confirmButtonText: 'Sim, esvaziar!',
			cancelButtonText: 'Cancelar',
		});

		if (!confirm.isConfirmed) return;

		try {
			const response = await fetch('/api/caixa/limpar', { method: 'POST' });
			const result = await response.json();
			Swal.fire({
				icon: result.sucesso ? 'success' : 'error',
				title: result.sucesso ? 'Sucesso' : 'Erro',
				text: result.mensagem,
			});
			if (result.sucesso) {
				atualizarCaixa();
			}
		} catch (error) {
			Swal.fire({
				icon: 'error',
				title: 'Erro',
				text: 'Erro de comunicação com o servidor.',
			});
		}
	}

	async function processarPagamento() {
		const tipo_veiculo = vehicleSelect.value;
		const valor_pago = amountPaidInput.value;
		if (!tipo_veiculo || !valor_pago || parseFloat(valor_pago) <= 0) {
			Swal.fire({
				icon: 'warning',
				title: 'Atenção',
				text: 'Selecione um veículo e um valor pago válido.',
			});
			return;
		}
		try {
			const response = await fetch('/api/pagar', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ tipo_veiculo, valor_pago }),
			});
			const resultado = await response.json();
			exibirResultado(resultado.sucesso, resultado.mensagem, resultado);
			if (resultado.sucesso) {
				atualizarCaixa();
				amountPaidInput.value = '';
			}
		} catch (error) {
			exibirResultado(false, 'Erro de comunicação.');
		}
	}

	// --- Configuração dos Eventos ---
	vehicleSelect.addEventListener('change', () => {
		const v = vehicleSelect.value;
		tariffDisplay.textContent = v
			? `R$ ${currentRates[v].toFixed(2)}`
			: 'R$ 0.00';
	});

	payButton.addEventListener('click', processarPagamento);
	addCashButton.addEventListener('click', () => gerenciarCaixa('abastecer'));
	removeCashButton.addEventListener('click', () => gerenciarCaixa('remover'));
	clearCashButton.addEventListener('click', limparCaixa);

	// --- Carregamento Inicial ---
	function inicializarPainel() {
		carregarTarifas();
		carregarDenominacoes();
		atualizarCaixa();
	}
	inicializarPainel();
});
