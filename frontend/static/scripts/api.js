function loginUser(email, senha) {
    const data = {
        email: email,
        senha: senha
    };

    // Envia os dados para a API Flask
    fetch('/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redireciona o usuário para o feed ou página principal após login bem-sucedido
            window.location.href = '/feed';
        } else {
            // Exibe um erro se o login falhar
            alert('E-mail ou senha incorretos!');
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        alert('Ocorreu um erro, tente novamente.');
    });
}

function criarConta(username, email, senha, confirmacaoSenha) {
    const data = {
        username: username,
        email: email,
        senha: senha,
        confirmacao_senha: confirmacaoSenha
    };

    // Envia os dados para a API Flask
    fetch('/api/auth/criarconta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redireciona o usuário para a página de login após conta criada
            window.location.href = '/homepage';
        } else {
            // Exibe um erro se a criação da conta falhar
            alert(data.message || 'Erro ao criar conta!');
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        alert('Ocorreu um erro, tente novamente.');
    });
}
