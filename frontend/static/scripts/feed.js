document.addEventListener("DOMContentLoaded", function () {
    const accessToken = localStorage.getItem("access_token");
    console.log("Token JWT: ", accessToken);  // Adicionando log para depuração
    if (!accessToken) {
        alert("Você precisa estar logado para acessar o feed.");
        window.location.href = "/homepage"; // Redireciona para a página de login
        return;
    }

    // Verifica o perfil do usuário autenticado
    fetch("/perfil", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${accessToken}`, // Garante que o token é passado no cabeçalho
            "Content-Type": "application/json"
        }
    })
        .then(response => {
            console.log("Status da resposta:", response.status);
            if (!response.ok) {
                throw new Error("Erro de autenticação. Faça login novamente.");
            }
            return response.text(); // Perfil retorna HTML, não JSON
        })
        .then(html => {
            console.log("Perfil carregado com sucesso!");
        })
        .catch(error => {
            alert(error.message);
            localStorage.removeItem("access_token");
            window.location.href = "/homepage";
        });
});
