document.addEventListener('DOMContentLoaded', function () {
  // Configurações
  const AFFILIATE_TAG = 'ofertasflashh-20';
  const REDIRECT_DELAY = 300;

  // Elementos do DOM
  const elements = {
    searchForm: document.getElementById('searchForm'),
    buttonText: document.getElementById('buttonText'),
    spinner: document.getElementById('spinner'),
    searchButton: document.getElementById('searchButton'),
    keywordInput: document.getElementById('palavras_chave'),
    departmentInput: document.getElementById('departamento'),
    discountInput: document.getElementById('desconto'),
    priceInput: document.getElementById('preco')
  };

  // Mapeamento de faixas de preço para parâmetros da Amazon
  const PRICE_RANGES = {
    'Abaixo de R$50': 'p_36:12546630011',
    'Abaixo de R$100': 'p_36:12546640011',
    'Abaixo de R$200': 'p_36:12546650011',
    'Acima de R$200': 'p_36:12546660011'
  };

  // Mapeamento de descontos para parâmetros da Amazon
  const DISCOUNT_RANGES = {
    '10% ou mais': 'p_n_pct-off-with-tax:2665401011',
    '25% ou mais': 'p_n_pct-off-with-tax:2665402011',
    '50% ou mais': 'p_n_pct-off-with-tax:2665403011',
    '70% ou mais': 'p_n_pct-off-with-tax:2665404011'
  };

  // Manipulador do formulário de busca
  function handleSearchFormSubmit(e) {
    e.preventDefault();

    if (!validateElements(elements)) return;

    // Prepara UI para o carregamento
    setLoadingState(true);

    // Obtém dados do formulário
    const keywords = elements.keywordInput.value.trim();
    const department = elements.departmentInput.value;
    const discount = elements.discountInput.value;
    const priceRange = elements.priceInput.value;

    // Constrói parâmetros de busca
    let searchParams = [];

    // Adiciona palavras-chave e departamento
    if (keywords) searchParams.push(`k=${encodeURIComponent(keywords + (department !== 'Todos' ? ' ' + department : ''))}`);

    // Adiciona filtro de desconto se selecionado
    if (discount !== '10% ou mais' && DISCOUNT_RANGES[discount]) {
      searchParams.push(DISCOUNT_RANGES[discount]);
    }

    // Adiciona filtro de preço se selecionado
    if (priceRange !== 'Qualquer' && PRICE_RANGES[priceRange]) {
      searchParams.push(PRICE_RANGES[priceRange]);
    }

    // Constrói URL final
    const baseUrl = 'https://www.amazon.com.br/s';
    const urlParams = searchParams.join('&');
    const url = `${baseUrl}?${urlParams}&tag=${AFFILIATE_TAG}`;

    // Redireciona após um pequeno delay
    setTimeout(() => {
      window.location.href = url;
      // Opcional: Restaura estado (normalmente não é necessário devido ao redirecionamento)
      setLoadingState(false);
    }, REDIRECT_DELAY);
  }

  // Manipulador de links de afiliados (mantido igual)
  function handleAffiliateLinkClick(e) {
    e.preventDefault();

    const rawLink = this.getAttribute('data-link');
    if (!rawLink) return;

    try {
      const url = new URL(rawLink);

      // Adiciona tag de afiliado se não existir
      if (!url.searchParams.has('tag')) {
        url.searchParams.set('tag', AFFILIATE_TAG);
      }

      window.open(url.toString(), '_blank');
    } catch (err) {
      console.error('Erro ao processar link de afiliado:', err);
    }
  }

  // Funções auxiliares
  function validateElements(elements) {
    return Object.values(elements).every(el => el !== null);
  }

  function setLoadingState(isLoading) {
    elements.searchButton.disabled = isLoading;
    elements.buttonText.classList.toggle('hidden', isLoading);
    elements.spinner.classList.toggle('hidden', !isLoading);
  }

  // Inicialização
  if (elements.searchForm) {
    elements.searchForm.addEventListener('submit', handleSearchFormSubmit);
  }

  // Configura links de afiliado
  document.querySelectorAll('.link-afiliado').forEach(link => {
    link.addEventListener('click', handleAffiliateLinkClick);
  });

});