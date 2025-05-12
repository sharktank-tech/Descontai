// Manipulador do formulário de busca
document.addEventListener('DOMContentLoaded', function () {
  const searchForm = document.getElementById('searchForm');

  if (searchForm) {
    searchForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const buttonText = document.getElementById('buttonText');
      const spinner = document.getElementById('spinner');
      const searchButton = document.getElementById('searchButton');

      if (!buttonText || !spinner || !searchButton) return;

      // Desabilita o botão e mostra o spinner
      searchButton.disabled = true;
      buttonText.classList.add('hidden');
      spinner.classList.remove('hidden');

      // Captura os dados do formulário
      const palavras = document.getElementById('palavras_chave').value.trim();
      const departamento = document.getElementById('departamento').value;
      const tagAfiliado = 'ofertasflashh-20';

      const query = encodeURIComponent(palavras + ' ' + departamento);
      const url = `https://www.amazon.com.br/s?k=${query}&tag=${tagAfiliado}`;

      // Pequeno atraso antes do redirecionamento
      setTimeout(() => {
        window.location.href = url;

        // Restaura o estado do botão (opcional, pois vai redirecionar)
        spinner.classList.add('hidden');
        buttonText.classList.remove('hidden');
        searchButton.disabled = false;
      }, 300);
    });
  }

  // Aplica a tag de afiliado nos botões de produto
  document.querySelectorAll('.link-afiliado').forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();

      const rawLink = this.getAttribute('data-link');
      if (!rawLink) return;

      try {
        const url = new URL(rawLink);

        // Verifica se a URL já contém a tag de afiliado, se não, adiciona
        if (!url.searchParams.has('tag')) {
          url.searchParams.set('tag', 'ofertasflashh-20');
        }

        // Abre o link com a tag de afiliado
        window.open(url.toString(), '_blank');
      } catch (err) {
        console.error('Link de afiliado inválido:', rawLink);
      }
    });
  });
});