const API_BASE_URL = 'http://127.0.0.1:5000/api';
const accessToken = sessionStorage.getItem("access_token");
let currentPostId = null; // Variável global para armazenar o postId atual
let currentUserId = null; // Variável global para armazenar o ID do usuário logado

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

// Função para obter o perfil do usuário atual
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
            throw new Error("Erro ao buscar dados do usuário");
        }

        const data = await response.json();
        const userName = data.username;
        const userId = data.id;

        // Armazena o ID do usuário no sessionStorage
        sessionStorage.setItem("user_id", userId);
        currentUserId = userId; // Atualiza a variável global

        // Preenche o nome do usuário na página
        document.getElementById('user-name').innerText = userName;

        // Carrega os posts do usuário
        loadUserPosts(userId);

    } catch (error) {
        console.error("Erro:", error);
        alert("Não foi possível carregar os dados do usuário.");
    }
};

// Função para carregar os posts do usuário
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

        // Renderiza os posts na página
        renderPosts(posts);

    } catch (error) {
        console.error("Erro:", error);
        alert("Não foi possível carregar os posts do usuário.");
    }
};

// Função para renderizar os posts na página
const renderPosts = (posts) => {
    const photoGrid = document.querySelector('.photo-grid');

    // Limpa o conteúdo atual
    photoGrid.innerHTML = '';

    // Adiciona cada post ao grid
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

    // Adiciona o evento de clique para abrir a tela de comentários
    document.querySelectorAll('.square-image').forEach(image => {
        image.addEventListener('click', (event) => {
            const postId = image.getAttribute('data-post-id');
            abrirTelaComentarios(postId);
        });
    });
};

// Função para abrir a tela de comentários
const abrirTelaComentarios = async (postId) => {
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
        document.getElementById('overlay-comentarios').style.display = 'flex';

    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao carregar os dados do post ou comentários.');
    }
};

// Fechar a tela de comentários
document.getElementById('close-overlay-comentarios').addEventListener('click', () => {
    document.getElementById('overlay-comentarios').style.display = 'none';
});

// Configura o evento de mudança para o input de arquivo
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

// Função para mostrar a tela semitransparente de publicação
const overlay = document.getElementById('overlay');
const publicarBtn = document.getElementById('publicar-btn');
const fecharOverlayBtn = document.getElementById('fechar-overlay');

// Mostrar a tela semitransparente ao clicar no botão "Publicar"
publicarBtn.addEventListener('click', () => {
    overlay.style.display = 'flex';
});

// Fechar a tela semitransparente ao clicar no botão "Fechar"
fecharOverlayBtn.addEventListener('click', () => {
    overlay.style.display = 'none';
});

// Lógica para enviar a foto e a legenda para o backend
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

// Chama a função para carregar o perfil
getUserProfile();