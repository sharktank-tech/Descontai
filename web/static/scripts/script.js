document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const buttonText = document.getElementById('buttonText');
    const spinner = document.getElementById('spinner');
    const searchButton = document.getElementById('searchButton');

    // Desabilitar o botão para evitar múltiplos envios
    searchButton.disabled = true;

    // Exibir o spinner e ocultar o texto do botão
    buttonText.classList.add('hidden');
    spinner.classList.remove('hidden');

    // Capturar os dados do formulário
    const palavras = document.getElementById('palavras_chave').value.trim();
    const departamento = document.getElementById('departamento').value;
    const tagAfiliado = 'seunome-20'; // Substitua pela sua tag de afiliado real

    const query = encodeURIComponent(palavras + ' ' + departamento);
    const url = `https://www.amazon.com.br/s?k=${query}&tag=${tagAfiliado}`;

    // Esperar um pequeno delay para garantir que o spinner seja exibido
    setTimeout(() => {
      // Redirecionar
      window.location.href = url;

      // Ocultar o spinner após o redirecionamento
      spinner.classList.add('hidden');
      buttonText.classList.remove('hidden');

      // Reabilitar o botão após o redirecionamento (opcional)
      searchButton.disabled = false;
    }, 300); // Atraso de 300ms para exibir a animação antes de redirecionar
  });