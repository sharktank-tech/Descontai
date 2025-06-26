document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("searchForm");
  const button = document.getElementById("searchButton");
  const spinner = document.getElementById("spinner");
  const buttonText = document.getElementById("buttonText");

  if (!form || !button) {
    console.error("Elementos essenciais não encontrados!");
    return;
  }

  form.addEventListener("submit", function(e) {
    e.preventDefault();

    // Ativar estado de loading
    if (spinner) spinner.classList.remove("hidden");
    if (buttonText) buttonText.classList.add("hidden");
    button.disabled = true;

    // Obter valores do formulário
    const formData = {
      departamento: document.getElementById("departamento").value,
      palavrasChave: document.getElementById("palavras_chave").value.trim() || "ofertas",
      desconto: document.getElementById("desconto").value,
      preco: document.getElementById("preco").value
    };

    console.log("Parâmetros da busca:", formData);

    // Construir URL da Amazon
    const amazonUrl = buildAmazonUrl(formData);
    console.log("URL gerada:", amazonUrl);

    // Redirecionar após pequeno delay (para visualizar o loading)
    setTimeout(() => {
      window.location.assign(amazonUrl); // Método mais confiável que href
    }, 800);
  });

  function buildAmazonUrl(params) {
    const baseUrl = "https://www.amazon.com.br/s?k=";
    const searchTerm = encodeURIComponent(params.palavrasChave);
    const tagAfiliado = "&tag=descontai-20"; // SUBSTITUA pelo seu código

    // Mapeamento de departamentos
    const departamentosMap = {
      "Eletrônicos": "electronics",
      "Casa": "kitchen",
      "Moda": "fashion",
      "Livros": "books",
      "Beleza": "beauty"
    };

    // Filtro de preço (em centavos)
    const faixasPreco = {
      "Abaixo de R$50": "0-5000",
      "R$50 a R$100": "5000-10000",
      "R$100 a R$200": "10000-20000",
      "Acima de R$200": "20000-"
    };

    // Construir parâmetros
    let filters = "";

    // Filtro por departamento
    if (params.departamento && params.departamento !== "Todos") {
      filters += `&i=${departamentosMap[params.departamento] || params.departamento.toLowerCase()}`;
    }

    // Filtro por preço
    if (params.preco && faixasPreco[params.preco]) {
      filters += `&rh=p_36%3A${faixasPreco[params.preco]}`;
    }

    return `${baseUrl}${searchTerm}${filters}${tagAfiliado}`;
  }
});