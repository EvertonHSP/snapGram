const API_BASE_URL = 'http://127.0.0.1:5000/api';
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const email = form.email.value;
            const senha = form.senha.value;


            loginUser(email, senha);
        });
    }


    const inputFields = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');

    inputFields.forEach(inputField => {
        inputField.addEventListener('input', function () {
            const label = inputField.parentElement.querySelector('label');
            if (label) {
                label.style.display = inputField.value.trim() !== '' ? 'none' : 'block';
            }
        });
    });
});

function loginUser(email, senha) {
    const data = {
        email: email,
        password: senha
    };

    fetch(`${API_BASE_URL}/auth/login`, {
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

                sessionStorage.setItem('access_token', data.access_token);

                alert("Login realizado com sucesso!");
                window.location.href = 'feed.html';
            } else {
                alert(data.error || "Erro ao fazer login!");
            }
        })
        .catch(error => {
            console.error("Erro na requisição:", error);
            alert("Ocorreu um erro, tente novamente.");
        });
}
