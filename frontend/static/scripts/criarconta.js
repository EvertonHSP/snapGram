const API_BASE_URL = 'http://127.0.0.1:5000/api';
function criarConta(username, email, senha, confirmacaoSenha) {
    if (senha !== confirmacaoSenha) {
        alert("As senhas não coincidem!");
        return;
    }

    const data = {
        username: username,
        email: email,
        password: senha
    };

    fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                if (data.message.includes("Usuário criado com sucesso")) {

                    sessionStorage.setItem('access_token', data.access_token);
                    window.location.href = 'feed.html';
                }
            } else {
                alert(data.error || "Erro ao criar conta!");
            }
        })
        .catch(error => {
            console.error("Erro na requisição:", error);
            alert("Ocorreu um erro, tente novamente.");
        });
}

document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();

    const username = document.querySelector('[name="username"]').value;
    const email = document.querySelector('[name="email"]').value;
    const senha = document.querySelector('[name="senha"]').value;
    const confirmacaoSenha = document.querySelector('[name="confirmacao_senha"]').value;


    if (!username || !email || !senha || !confirmacaoSenha) {
        alert('Todos os campos devem ser preenchidos!');
        return;
    }


    if (senha !== confirmacaoSenha) {
        alert('As senhas não coincidem!');
        return;
    }


    criarConta(username, email, senha, confirmacaoSenha);
});


const inputFields = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');

inputFields.forEach(inputField => {
    inputField.addEventListener('input', function () {
        const label = inputField.parentElement.querySelector('label');
        if (inputField.value.trim() !== '') {
            label.style.display = 'none';
        } else {
            label.style.display = 'block';
        }
    });
});
