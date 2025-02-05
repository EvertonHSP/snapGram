function criarConta(username, email, senha, confirmacaoSenha) {
    if (senha !== confirmacaoSenha) {
        alert("As senhas não coincidem!");
        return;
    }

    const data = {
        username: username,
        email: email,
        password: senha  // Mantém a chave 'password' conforme esperado no backend
    };

    fetch('/api/auth/register', {
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
                alert(data.message); // Exibe mensagem de sucesso ou erro
                if (data.message.includes("Usuário criado com sucesso")) {
                    // Armazena o token JWT no localStorage
                    localStorage.setItem('access_token', data.access_token);
                    window.location.href = '/feed'; // Redireciona ao feed após a criação
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

    // Verifica se todos os campos foram preenchidos
    if (!username || !email || !senha || !confirmacaoSenha) {
        alert('Todos os campos devem ser preenchidos!');
        return;
    }

    // Verifica se as senhas coincidem
    if (senha !== confirmacaoSenha) {
        alert('As senhas não coincidem!');
        return;
    }

    // Chama a função para criar a conta
    criarConta(username, email, senha, confirmacaoSenha);
});

// Esconde o rótulo quando o campo for preenchido
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
