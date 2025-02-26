const API_BASE_URL = 'http://127.0.0.1:5000/api';
const accessToken = sessionStorage.getItem("access_token");
let currentPostId = null; 
let currentUserId = null;

document.addEventListener("DOMContentLoaded", function () {
    console.log("Token JWT: ", accessToken);

    
    if (!accessToken) {
        alert("Você precisa estar logado para acessar o feed.");
        window.location.href = "homepage.html";
        return;
    }

    obterUsuarioAtual();

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
                    "Authorization": `Bearer ${accessToken}`,
                }
            })
                .then(response => {
                    console.log("Status da resposta:", response.status);
                    if (!response.ok) {
                        throw new Error("Erro de autenticação. Faça login novamente.");
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Dados do usuário:", data);
                    window.location.href = 'perfil.html';
                })
                .catch(error => {
                    alert(error.message);
                    localStorage.removeItem("access_token");
                    window.location.href = 'homepage.html';
                });
        });
    }





    const sairButton = document.querySelector(".top-right");
    if (sairButton) {
        sairButton.addEventListener("click", function (event) {
            event.preventDefault(); 

            const accessToken = sessionStorage.getItem("access_token");

            if (!accessToken) {
                
                window.location.href = "homepage.html";
                return;
            }

            
            fetch(`${API_BASE_URL}/auth/logout`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                }
            })
            .then(response => {
                console.log("Status da resposta:", response.status);

                if (!response.ok) {
                    throw new Error("Erro ao sair da conta, tente novamente.");
                }

                return response.json();
            })
            .then(data => {
                console.log("Dados do usuário:", data);

                
                sessionStorage.removeItem("access_token");

                
                window.location.href = "homepage.html";
            })
            .catch(error => {
                console.error("Erro durante o logout:", error);
                alert(error.message);
            });
        });
    }






    async function obterUsuarioAtual() {
        try {
            const response = await fetch(`${API_BASE_URL}/user/current`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Erro ao obter dados do usuário");
            }

            const data = await response.json();
            currentUserId = data.id; 
            console.log("ID do usuário logado:", currentUserId);
        } catch (error) {
            console.error("Erro ao obter ID do usuário:", error);
        }
    }


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

            
            photoGrid.innerHTML = '';

            
            for (const foto of fotos) {
                const photoItem = document.createElement('li');
                photoItem.className = 'photo-item';

                
                const fotoPerfilUrl = foto.usuario.foto_perfil_url || "static/style/img/fotoPerfil.png";

                photoItem.innerHTML = `
                <div class="photo-info" data-post-id="${foto.id}">
                    <div class="user-info">
                        <img src="${fotoPerfilUrl}" alt="Foto de perfil" class="profile-image">
                        <p class="photo-username">${foto.usuario.username} (ID: ${foto.usuario.id})</p>
                    </div>
                    <p class="photo-caption">${foto.legenda}</p>
                    <div class="square-image">
                        <img src="${foto.imagem_url}" alt="Foto de ${foto.usuario.username}">
                    </div>
                    <p class="photo-timestamp">${foto.data_criacao}</p>
                    <div class="comments-section">
                        <button class="like-button" data-post-id="${foto.id}">
                            <img src="static/style/img/nolike.png" alt="Curtir">
                            <span class="like-count">0</span>
                        </button>
                        <button class="comments-button" data-post-id="${foto.id}">
                            Comentários
                        </button>
                    </div>
                </div>
            `;

                photoGrid.appendChild(photoItem);

                
                await atualizarContadorCurtidas(foto.id);
            }

           
            document.querySelectorAll('.like-button').forEach(button => {
                button.addEventListener('click', async (event) => {
                    event.stopPropagation();
                    const postId = button.getAttribute('data-post-id');
                    await curtirPost(postId);
                });
            });

            
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

   
    async function curtirPost(postId) {
        try {
            const response = await fetch(`${API_BASE_URL}/post/${postId}/curtir`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                }
            });

            const data = await response.json();

            if (!response.ok) {
                if (data.message === "Você já curtiu este post") {
                    console.log("Post já curtido. Removendo curtida...");
                    await descurtirPost(postId);
                } else {
                    throw new Error(data.message || "Erro ao curtir");
                }
            } else {
                console.log("Post curtido:", data);
                await atualizarContadorCurtidas(postId);
            }
        } catch (error) {
            console.error("Erro:", error);
            alert("Erro ao curtir o post.");
        }
    }

    async function descurtirPost(postId) {
        try {
            const response = await fetch(`${API_BASE_URL}/post/${postId}/curtir`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Erro ao remover curtida");
            }

            console.log("Curtida removida");
            await atualizarContadorCurtidas(postId);
        } catch (error) {
            console.error("Erro:", error);
            alert("Erro ao remover a curtida.");
        }
    }


    
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

            // Verifica se o usuário atual curtiu o post
            const usuarioCurtiu = await verificarSeUsuarioCurtiu(postId);

            // Atualiza o contador de curtidas no feed
            const likeButtonFeed = document.querySelector(`.like-button[data-post-id="${postId}"]`);
            if (likeButtonFeed) {
                const likeImageFeed = likeButtonFeed.querySelector('img');
                const likeCountFeed = likeButtonFeed.querySelector('.like-count');

                likeImageFeed.src = usuarioCurtiu ? "static/style/img/like.png" : "static/style/img/nolike.png";
                likeCountFeed.innerText = likeCount;
            }

            // Atualiza o contador de curtidas na tela semitransparente
            const likeButtonOverlay = document.querySelector(`#overlay-like-button`);
            if (likeButtonOverlay && currentPostId === postId) {
                const likeImageOverlay = likeButtonOverlay.querySelector('img');
                const likeCountOverlay = likeButtonOverlay.querySelector('.like-count');

                likeImageOverlay.src = usuarioCurtiu ? "static/style/img/like.png" : "static/style/img/nolike.png";
                likeCountOverlay.innerText = likeCount;
            }

        } catch (error) {
            console.error('Erro:', error);
        }
    }

    async function verificarSeUsuarioCurtiu(postId) {
        try {
            const response = await fetch(`${API_BASE_URL}/post/${postId}/get_like`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error('Erro ao verificar curtida');
            }

            const data = await response.json();

            
            const usuarioCurtiu = data.usuarios_curtiu.some(usuario => usuario.id === currentUserId);
            return usuarioCurtiu;
        } catch (error) {
            console.error('Erro ao verificar se o usuário curtiu:', error);
            return false;
        }
    }

    
    async function abrirTelaComentarios(postId) {
        currentPostId = postId;
        try {
            
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

            const fotoPerfilUrl = postData.usuario.foto_perfil_url || "static/style/img/fotoPerfil.png";

            document.getElementById('post-profile-image').src = fotoPerfilUrl;
            document.getElementById('post-username').innerText = postData.usuario.username;
            document.getElementById('post-image').src = postData.imagem_url;
            document.getElementById('post-caption').innerText = postData.legenda;
            document.getElementById('post-timestamp').innerText = postData.data_criacao;

            
            await atualizarContadorCurtidas(postId);

            
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

            
            const likeButtonOverlay = document.getElementById('overlay-like-button');
            if (likeButtonOverlay) {
                
                likeButtonOverlay.replaceWith(likeButtonOverlay.cloneNode(true));
                const newLikeButtonOverlay = document.getElementById('overlay-like-button');

                
                newLikeButtonOverlay.setAttribute('data-post-id', postId);

                
                newLikeButtonOverlay.addEventListener('click', async (event) => {
                    event.stopPropagation();
                    await curtirPost(postId);
                });
            }

            
            document.getElementById('overlay').style.display = 'flex';

        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao carregar os dados do post ou comentários.');
        }
    }

    
    document.getElementById('close-overlay').addEventListener('click', () => {
        document.getElementById('overlay').style.display = 'none';
    });

    
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

    
    setInterval(async () => {
        const posts = document.querySelectorAll('.photo-info');
        for (const post of posts) {
            const postId = post.getAttribute('data-post-id');
            await atualizarContadorCurtidas(postId);
        }
    }, 60000); 

    
    carregarFotos();
});