document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Previne o envio tradicional do formulário

        const email = form.email.value;
        const senha = form.senha.value;

        // Chama a função de login que faz a requisição para a API
        loginUser(email, senha);
    });
});
