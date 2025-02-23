const API_BASE_URL = 'http://127.0.0.1:5000/api';
const accessToken = sessionStorage.getItem("access_token");
let currentPostId = null; // Variável global para armazenar o postId atual

document.addEventListener("DOMContentLoaded", function () {
    console.log("Token JWT: ", accessToken);

    // Verifica se o usuário está autenticado
    if (!accessToken) {
        alert("Você precisa estar logado para acessar o feed.");
        window.location.href = "homepage.html";
        return;
    }
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
    // Função para carregar as fotos do feed
    // Função para carregar as fotos do feed
    async function carregarFotos() {
        try {
            const response = await fetch(`${API_BASE_URL}/posts`, {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error('Erro ao carregar fotos');
            }

            const data = await response.json();
            console.log("Resposta da API:", data);

            const fotos = data.fotos;
            const photoGrid = document.getElementById('photo-grid');

            // Limpa o grid antes de adicionar as novas fotos
            photoGrid.innerHTML = '';

            // Para cada foto, carrega o número de curtidas
            for (const foto of fotos) {
                const photoItem = document.createElement('li');
                photoItem.className = 'photo-item';

                photoItem.innerHTML = `
                    <div class="photo-info" data-post-id="${foto.id}">
                        <div class="user-info">
                            <img src="static/style/img/fotoPerfil.png" alt="Foto de perfil" class="profile-image">
                            <p class="photo-username">${foto.usuario.username} (ID: ${foto.usuario.id})</p>
                        </div>
                        <p class="photo-caption">${foto.legenda}</p>
                        <div class="square-image">
                            <img src="${foto.imagem_url}" alt="Foto de ${foto.usuario.username}">
                        </div>
                        <p class="photo-timestamp">${foto.data_criacao}</p>
                        <div class="comments-section">
                            <button class="like-button" data-post-id="${foto.id}">
                                <img src="static/style/img/like.png" alt="Curtir">
                                <span class="like-count">0</span>
                            </button>
                            <button class="comments-button" data-post-id="${foto.id}">
                                Comentários
                            </button>
                        </div>
                    </div>
                `;

                photoGrid.appendChild(photoItem);

                // Carrega o número de curtidas para este post
                await atualizarContadorCurtidas(foto.id);
            }

            // Adiciona o evento de clique para curtir
            document.querySelectorAll('.like-button').forEach(button => {
                button.addEventListener('click', async (event) => {
                    event.stopPropagation();
                    const postId = button.getAttribute('data-post-id');
                    await curtirPost(postId);
                });
            });

            // Adiciona o evento de clique para abrir a tela de comentários
            document.querySelectorAll('.comments-button').forEach(button => {
                button.addEventListener('click', (event) => {
                    event.stopPropagation();
                    const postId = button.getAttribute('data-post-id');
                    abrirTelaComentarios(postId);
                });
            });

        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao carregar o feed. Tente novamente.');
        }
    }

    // Função para curtir um post
    async function curtirPost(postId) {
        try {
            const response = await fetch(`${API_BASE_URL}/post/${postId}/curtir`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error('Erro ao curtir o post');
            }

            const data = await response.json();
            console.log("Post curtido:", data);

            // Atualiza o contador de curtidas
            await atualizarContadorCurtidas(postId);

        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao curtir o post.');
        }
    }

    // Função para atualizar o contador de curtidas
    async function atualizarContadorCurtidas(postId) {
        try {
            const response = await fetch(`${API_BASE_URL}/post/${postId}/get_like`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error('Erro ao carregar o número de curtidas');
            }

            const data = await response.json();
            console.log("Resposta da API (curtidas):", data);

            // Acessa o número de curtidas corretamente
            const likeCount = data.total_curtidas;

            // Atualiza o contador de curtidas no botão
            const likeButton = document.querySelector(`.like-button[data-post-id="${postId}"] .like-count`);
            if (likeButton) {
                likeButton.innerText = likeCount;
            } else {
                console.error('Botão de curtir não encontrado para o post ID:', postId);
            }

        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao atualizar o contador de curtidas.');
        }
    }

    // Função para abrir a tela de comentários
    async function abrirTelaComentarios(postId) {
        currentPostId = postId;
        try {
            // Carrega os dados do post
            const postResponse = await fetch(`${API_BASE_URL}/post/${postId}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Accept": "application/json"
                }
            });

            if (!postResponse.ok) {
                throw new Error('Erro ao carregar os dados do post');
            }

            const postData = await postResponse.json();
            console.log("Dados do post:", postData);

            // Preenche as informações do post na tela semitransparente
            document.getElementById('post-profile-image').src = "static/style/img/fotoPerfil.png";
            document.getElementById('post-username').innerText = postData.usuario.username;
            document.getElementById('post-image').src = postData.imagem_url;
            document.getElementById('post-caption').innerText = postData.legenda;
            document.getElementById('post-timestamp').innerText = postData.data_criacao;

            // Atualiza o contador de curtidas
            await atualizarContadorCurtidas(postId);

            // Carrega os comentários do post
            const commentsResponse = await fetch(`${API_BASE_URL}/post/${postId}/comentarios`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Accept": "application/json"
                }
            });

            if (!commentsResponse.ok) {
                throw new Error('Erro ao carregar os comentários');
            }

            const commentsData = await commentsResponse.json();
            console.log("Comentários:", commentsData);

            // Renderiza os comentários na tela semitransparente
            const commentsList = document.getElementById('comments-list');
            commentsList.innerHTML = '';

            commentsData.comentarios.forEach(comentario => {
                const commentItem = document.createElement('div');
                commentItem.className = 'comment-item';
                commentItem.innerHTML = `
                    <p><strong>${comentario.usuario.username}</strong>: ${comentario.conteudo}</p>
                    <p class="comment-timestamp">${comentario.data_criacao}</p>
                `;
                commentsList.appendChild(commentItem);
            });

            // Exibe a tela semitransparente
            document.getElementById('overlay').style.display = 'flex';

        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao carregar os dados do post ou comentários.');
        }
    }

    // Função para fechar a tela semitransparente
    document.getElementById('close-overlay').addEventListener('click', () => {
        document.getElementById('overlay').style.display = 'none';
    });

    // Função para enviar um comentário
    document.getElementById('submit-comment').addEventListener('click', async () => {
        if (!currentPostId) {
            alert("Nenhum post selecionado.");
            return;
        }

        const commentInput = document.getElementById('comment-input').value;

        if (!commentInput) {
            alert("Por favor, digite um comentário.");
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/post/${currentPostId}/comentarios/create`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ conteudo: commentInput })
            });

            if (!response.ok) {
                throw new Error('Erro ao enviar o comentário');
            }

            const data = await response.json();
            console.log("Comentário enviado:", data);

            // Recarrega os comentários após o envio
            abrirTelaComentarios(currentPostId);

            // Atualiza o contador de curtidas
            await atualizarContadorCurtidas(currentPostId);

            // Limpa o campo de comentário
            document.getElementById('comment-input').value = '';

        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao enviar o comentário.');
        }
    });

    // Atualiza o contador de curtidas a cada minuto
    // Atualiza o contador de curtidas a cada minuto
    setInterval(async () => {
        const posts = document.querySelectorAll('.photo-info');
        for (const post of posts) {
            const postId = post.getAttribute('data-post-id');
            await atualizarContadorCurtidas(postId);
        }
    }, 120000); // 60000 milissegundos = 1 minuto

    // Carrega as fotos quando a página é carregada
    carregarFotos();
});