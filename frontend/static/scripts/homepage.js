document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();  // Previne o envio tradicional do formulário

            const email = form.email.value;
            const senha = form.senha.value;

            // Chama a função de login que faz a requisição para a API
            loginUser(email, senha);
        });
    }

    // Esconde o rótulo quando o campo for preenchido (como no criarconta.js)
    const inputFields = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');

    inputFields.forEach(inputField => {
        inputField.addEventListener('input', function () {
            const label = inputField.parentElement.querySelector('label');
            if (label) { // Verifica se o label existe antes de alterar
                label.style.display = inputField.value.trim() !== '' ? 'none' : 'block';
            }
        });
    });
});

function loginUser(email, senha) {
    const data = {
        email: email,
        password: senha // Certifique-se de que o backend espera 'password'
    };

    fetch('/api/auth/login', {  // Confirme se a rota da API é essa
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                // Armazena o token JWT
                localStorage.setItem('access_token', data.access_token);

                alert("Login realizado com sucesso!");
                window.location.href = '/feed'; // Redireciona para o feed ou outra página
            } else {
                alert(data.error || "Erro ao fazer login!");
            }
        })
        .catch(error => {
            console.error("Erro na requisição:", error);
            alert("Ocorreu um erro, tente novamente.");
        });
}
