document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("searchForm");
  const button = document.getElementById("searchButton");
  const spinner = document.getElementById("spinner");
  const buttonText = document.getElementById("buttonText");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Mostra o spinner e oculta o texto do botão
    spinner.classList.remove("hidden");
    buttonText.classList.add("hidden");

    // Obtém os valores
    const departamento = document.getElementById("departamento").value;
    const palavrasChave = document.getElementById("palavras_chave").value.trim();
    const desconto = document.getElementById("desconto").value;
    const preco = document.getElementById("preco").value;

    // Codifica a URL de busca da Amazon
    let searchTerm = encodeURIComponent(palavrasChave || "descontos");

    // Base da URL
    const baseUrl = "https://www.amazon.com.br/s?k=";
    const tagAfiliado = "&tag=descont_ai-20"; // Substitua se necessário
    let filtros = "";

    // Filtro de preço (usando p_36 em centavos)
    switch (preco) {
      case "Abaixo de R$50":
        filtros += "&rh=p_36%3A0-5000";
        break;
      case "R$50 a R$100":
        filtros += "&rh=p_36%3A5000-10000";
        break;
      case "R$100 a R$200":
        filtros += "&rh=p_36%3A10000-20000";
        break;
      case "Acima de R$200":
        filtros += "&rh=p_36%3A20000-";
        break;
    }

    // Filtro de departamento (opcional)
    if (departamento && departamento !== "todos") {
      filtros += `&i=${encodeURIComponent(departamento)}`;
    }

    // Monta a URL final
    const finalUrl = `${baseUrl}${searchTerm}${filtros}${tagAfiliado}`;

    // Redireciona
    console.log("Redirecionando para:", finalUrl);  // Para depuração
    window.location.href = finalUrl;
  });
});