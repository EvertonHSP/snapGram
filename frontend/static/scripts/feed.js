const API_BASE_URL = 'http://127.0.0.1:5000/api';

document.addEventListener("DOMContentLoaded", function () {
    const accessToken = localStorage.getItem("access_token");
    console.log("Token JWT: ", accessToken);

    const perfilButton = document.querySelector(".top-left");
    if (perfilButton) {
        perfilButton.addEventListener("click", function (event) {
            event.preventDefault();

            if (!accessToken) {
                alert("Você precisa estar logado para acessar o perfil.");
                window.location.href = "homepage.html";
                return;
            }

            fetch(`${API_BASE_URL}/user/current`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,  // Envia o token JWT no cabeçalho
                }
            })
                .then(response => {
                    console.log("Status da resposta:", response.status);
                    if (!response.ok) {
                        throw new Error("Erro de autenticação. Faça login novamente.");
                    }
                    return response.json();  // Converte a resposta para JSON
                })
                .then(data => {
                    console.log("Dados do usuário:", data);

                    // Redireciona para a página de perfil
                    window.location.href = 'perfil.html';
                })
                .catch(error => {
                    alert(error.message);
                    localStorage.removeItem("access_token");  // Remove o token inválido
                    window.location.href = 'homepage.html';
                });
        });
    }
});