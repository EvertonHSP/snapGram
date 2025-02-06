document.addEventListener("DOMContentLoaded", function () {
    const accessToken = localStorage.getItem("access_token");
    console.log("Token JWT: ", accessToken);


    const perfilButton = document.querySelector(".top-left");
    if (perfilButton) {
        perfilButton.addEventListener("click", function (event) {
            event.preventDefault();

            if (!accessToken) {
                alert("Você precisa estar logado para acessar o perfil.");
                window.location.href = "/homepage";
                return;
            }

            fetch("/perfil", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,  // Envia o token JWT no cabeçalho
                    "Content-Type": "application/json"
                }
            })
                .then(response => {
                    console.log("Status da resposta:", response.status);
                    if (!response.ok) {
                        throw new Error("Erro de autenticação. Faça login novamente.");
                    }
                    return response.text();
                })
                .then(html => {

                    document.body.innerHTML = html;
                    console.log("Perfil carregado com sucesso!");
                })
                .catch(error => {
                    alert(error.message);
                    localStorage.removeItem("access_token");  // Remove o token inválido
                    window.location.href = "/homepage";
                });
        });
    }
});