const API_BASE_URL = 'http://127.0.0.1:5000/api';
const accessToken = sessionStorage.getItem("access_token");
let currentPostId = null; 
let currentUserId = null; 
let isLiking = false; 

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}


const getUserProfile = async () => {
    console.log("Access Token:", accessToken);
    try {
        const response = await fetch(`${API_BASE_URL}/user/current`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            }
        });

        if (!response.ok) {
            window.location.href = "homepage.html";
            throw new Error("Erro ao buscar dados do usuário");
        }

        const data = await response.json();
        const userName = data.username;
        const userId = data.id;

        sessionStorage.setItem("user_id", userId);
        currentUserId = userId; 
        document.getElementById('user-name').innerText = userName;

        loadProfilePicture(userId);
        loadUserPosts(userId);

    } catch (error) {
        console.error("Erro:", error);
        alert("Não foi possível carregar os dados do usuário.");
    }
};


const loadUserPosts = async (userId) => {
    try {
        const response = await fetch(`${API_BASE_URL}/posts?user_id=${userId}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            }
        });

        if (!response.ok) {
            throw new Error("Erro ao carregar os posts do usuário");
        }

        const data = await response.json();
        const posts = data.fotos;

        renderPosts(posts);

    } catch (error) {
        console.error("Erro:", error);
        alert("Não foi possível carregar os posts do usuário.");
    }
};


const loadProfilePicture = async (usuario_id) => {
    try {
        const response = await fetch(`${API_BASE_URL}/foto_perfil/${usuario_id}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            }
        });

        if (!response.ok) {
            throw new Error("Erro ao buscar a foto de perfil");
        }

        const data = await response.json();

        
        if (data.foto_perfil_url) {
            document.getElementById('foto-perfil-usuario').src = data.foto_perfil_url;
        } else {
            document.getElementById('foto-perfil-usuario').src = "static/style/img/fotoPerfil.png";
        }

    } catch (error) {
        console.error("Erro ao carregar a foto de perfil:", error);
        
        document.getElementById('foto-perfil-usuario').src = "static/style/img/fotoPerfil.png";
    }
};


const renderPosts = (posts) => {
    const photoGrid = document.querySelector('.photo-grid');

    
    photoGrid.innerHTML = '';

    
    posts.forEach(post => {
        const photoItem = document.createElement('div');
        photoItem.className = 'photo-item';

        photoItem.innerHTML = `
            <div class="square-image" data-post-id="${post.id}">
                <img src="${post.imagem_url}" alt="Foto de ${post.usuario.username}">
            </div>
        `;

        photoGrid.appendChild(photoItem);
    });

    
    document.querySelectorAll('.square-image').forEach(image => {
        image.addEventListener('click', (event) => {
            const postId = image.getAttribute('data-post-id');
            abrirTelaComentarios(postId);
        });
    });
};

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

            window.location.href = "homepage.html";
        })
        .catch(error => {
            console.error("Erro durante o logout:", error);
            alert(error.message);
        });
    });
}




document.getElementById('trocar-foto-btn').addEventListener('click', () => {
    document.getElementById('overlay-foto-perfil').style.display = 'flex';
});


document.getElementById('fechar-overlay-foto-perfil').addEventListener('click', () => {
    document.getElementById('overlay-foto-perfil').style.display = 'none';
});


const trocarFotoForm = document.getElementById('trocar-foto-form');
trocarFotoForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const fotoPerfil = document.getElementById('foto-perfil').files[0];

    if (!fotoPerfil) {
        alert("Por favor, selecione uma foto para fazer o upload.");
        return;
    }

    // Cria um objeto FormData para enviar a imagem como arquivo binário
    const formData = new FormData();
    formData.append('foto', fotoPerfil);

    try {
        const response = await fetch(`${API_BASE_URL}/foto_perfil/upload`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Erro ao enviar a foto de perfil.");
        }

        const data = await response.json();
        alert(data.message || "Foto de perfil atualizada com sucesso!");

        // Atualiza a foto de perfil na interface do usuário
        await loadProfilePicture(currentUserId);

        // Limpa o formulário após o envio
        trocarFotoForm.reset();
        document.getElementById('thumbnail-perfil').src = '';
        document.getElementById('file-selected-image-perfil').style.display = 'none';

        // Fecha a tela semitransparente após o envio
        document.getElementById('overlay-foto-perfil').style.display = 'none';

    } catch (error) {
        console.error("Erro:", error);
        alert("Não foi possível atualizar a foto de perfil.");
    }
});


document.getElementById('foto-perfil').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('thumbnail-perfil').src = e.target.result;
            document.getElementById('file-selected-image-perfil').style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        document.getElementById('thumbnail-perfil').src = '';
        document.getElementById('file-selected-image-perfil').style.display = 'none';
    }
});





const fileInput = document.getElementById('foto');
const thumbnailImage = document.getElementById('thumbnail');
const fileSelectedImage = document.getElementById('file-selected-image');

fileInput.addEventListener('change', (event) => {
    if (event.target.files.length > 0) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
            thumbnailImage.src = e.target.result;
            fileSelectedImage.style.display = 'block';
        };

        reader.readAsDataURL(file);
    } else {
        thumbnailImage.src = '';
        fileSelectedImage.style.display = 'none';
    }
});


const overlay = document.getElementById('overlay');
const publicarBtn = document.getElementById('publicar-btn');
const fecharOverlayBtn = document.getElementById('fechar-overlay');


publicarBtn.addEventListener('click', () => {
    overlay.style.display = 'flex';
});


fecharOverlayBtn.addEventListener('click', () => {
    overlay.style.display = 'none';
});


const publicarForm = document.getElementById('publicar-form');
publicarForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const legenda = document.getElementById('legenda').value;
    const foto = document.getElementById('foto').files[0];

    if (!foto) {
        alert("Por favor, selecione uma foto para fazer o upload.");
        return;
    }

    // Cria um objeto FormData para enviar a imagem como arquivo binário
    const formData = new FormData();
    formData.append('legenda', legenda);
    formData.append('foto', foto);
    try {
        const response = await fetch(`${API_BASE_URL}/posts/create`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Erro ao publicar a foto.");
        }

        const data = await response.json();
        alert(data.message || "Foto publicada com sucesso!");

        // Limpa o formulário após o envio
        publicarForm.reset();
        thumbnailImage.src = '';
        fileSelectedImage.style.display = 'none';

        // Fecha a tela semitransparente após o envio
        overlay.style.display = 'none';

        // Recarrega os posts do usuário após a publicação
        const userId = sessionStorage.getItem("user_id");
        loadUserPosts(userId);

    } catch (error) {
        console.error("Erro:", error);
        alert("Não foi possível publicar a foto.");
    }
});

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

        const fotoPerfilUrl = postData.usuario.foto_perfil_url || "static/style/img/fotoPerfil.png";

        document.getElementById('post-profile-image').src = fotoPerfilUrl;
        document.getElementById('post-username').innerText = postData.usuario.username;
        document.getElementById('post-image').src = postData.imagem_url;
        document.getElementById('post-caption').innerText = postData.legenda;
        document.getElementById('post-timestamp').innerText = postData.data_criacao;

        // Atualiza o contador de curtidas e o ícone de curtida
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

        // Atualiza o botão de curtida
        const likeButtonOverlay = document.querySelector('#overlay-comentarios .like-button');
        if (likeButtonOverlay) {
            likeButtonOverlay.setAttribute('data-post-id', postId); // Define o data-post-id dinamicamente
            likeButtonOverlay.removeEventListener('click', handleLikeClick); // Remove o evento anterior
            likeButtonOverlay.addEventListener('click', handleLikeClick); // Adiciona o novo evento

            // Atualiza o ícone de curtida imediatamente
            const usuarioCurtiu = await verificarSeUsuarioCurtiu(postId);
            const likeImage = likeButtonOverlay.querySelector('img');
            likeImage.src = usuarioCurtiu ? "static/style/img/like.png" : "static/style/img/nolike.png";
        } else {
            console.error("Botão de like não encontrado na tela de comentários.");
        }

        // Exibe a tela semitransparente
        document.getElementById('overlay-comentarios').style.display = 'flex';

    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao carregar os dados do post ou comentários.');
    }
}

async function handleLikeClick(event) {
    event.stopPropagation();
    const postId = event.currentTarget.getAttribute('data-post-id');
    const likeButton = event.currentTarget;

    // Altera o estado visual do botão imediatamente
    const likeImage = likeButton.querySelector('img');
    const usuarioCurtiu = likeImage.src.includes("like.png");
    likeImage.src = usuarioCurtiu ? "static/style/img/nolike.png" : "static/style/img/like.png";

    await curtirPost(postId);
}

document.getElementById('close-overlay-comentarios').addEventListener('click', () => {
    document.getElementById('overlay-comentarios').style.display = 'none';
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

        // Limpa o campo de comentário
        document.getElementById('comment-input').value = '';

    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao enviar o comentário.');
    }
});


document.getElementById('delete-post').addEventListener('click', async () => {
    if (!currentPostId) {
        alert("Nenhum post selecionado.");
        return;
    }

    const confirmacao = confirm("Tem certeza que deseja excluir este post?");
    if (!confirmacao) {
        return; // Cancela a exclusão se o usuário não confirmar
    }

    try {
        const response = await fetch(`${API_BASE_URL}/post/${currentPostId}/delete`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Erro ao excluir o post");
        }

        const data = await response.json();
        alert(data.message || "Post excluído com sucesso");

        // Fecha a tela de comentários após a exclusão
        document.getElementById('overlay-comentarios').style.display = 'none';

        // Recarrega os posts do usuário após a exclusão
        const userId = sessionStorage.getItem("user_id");
        loadUserPosts(userId);
    } catch (error) {
        console.error("Erro:", error);
        alert(error.message || "Erro ao excluir o post");
    }
});


async function curtirPost(postId) {
    if (isLiking) return; // Ignora cliques adicionais enquanto uma requisição está em andamento
    isLiking = true;

    const likeButton = document.querySelector(`.like-button[data-post-id="${postId}"]`);
    if (likeButton) {
        likeButton.disabled = true; // Desabilita o botão
    }

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
    } finally {
        isLiking = false; // Libera o controle
        if (likeButton) {
            likeButton.disabled = false; // Reabilita o botão
        }
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

        const likeCount = data.total_curtidas;

        // Verifica se o usuário atual curtiu o post
        const usuarioCurtiu = await verificarSeUsuarioCurtiu(postId);

        // Atualiza o contador de curtidas no botão de like
        const likeButton = document.querySelector('#overlay-comentarios .like-button');
        if (likeButton) {
            const likeImage = likeButton.querySelector('img');
            const likeCountSpan = likeButton.querySelector('.like-count');

            // Atualiza o ícone de curtida
            likeImage.src = usuarioCurtiu ? "static/style/img/like.png" : "static/style/img/nolike.png";

            // Atualiza o contador de curtidas
            if (likeCountSpan) {
                likeCountSpan.innerText = likeCount; // Garante que o valor seja atualizado
            } else {
                console.error("Elemento .like-count não encontrado.");
            }
        } else {
            console.error("Botão de like não encontrado.");
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

        // Verifica se o usuário atual está na lista de usuários que curtiram o post
        const usuarioCurtiu = data.usuarios_curtiu.some(usuario => usuario.id === currentUserId);
        return usuarioCurtiu;
    } catch (error) {
        console.error('Erro ao verificar se o usuário curtiu:', error);
        return false;
    }
}

getUserProfile();