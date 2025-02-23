const API_BASE_URL = 'http://127.0.0.1:5000/api';
const accessToken = sessionStorage.getItem("access_token");

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
                "Authorization": `Bearer ${accessToken}`,  // Envia o token JWT no cabeçalho
            }
        });

        if (!response.ok) {
            throw new Error("Erro ao buscar dados do usuário");
        }

        const data = await response.json();
        const userName = data.username;  // Acessando o nome de usuário diretamente do JSON
        const userId = data.id;  // Acessando o ID do usuário

        // Armazena o ID do usuário no sessionStorage
        sessionStorage.setItem("user_id", userId);

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
                "Authorization": `Bearer ${accessToken}`,  // Envia o token JWT no cabeçalho
            }
        });

        if (!response.ok) {
            throw new Error("Erro ao carregar os posts do usuário");
        }

        const data = await response.json();
        const posts = data.fotos;  // Acessa a lista de posts

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
            <div class="square-image">
                <img src="${post.imagem_url}" alt="Foto de ${post.usuario.username}">
            </div>
            <p class="photo-caption">${post.legenda}</p>
        `;

        photoGrid.appendChild(photoItem);
    });
};

// Chama a função para carregar o perfil
getUserProfile();

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

// Função para mostrar a tela semitransparente
const overlay = document.getElementById('overlay');
const publicarBtn = document.getElementById('publicar-btn');
const fecharOverlayBtn = document.getElementById('fechar-overlay');

// Mostrar a tela semitransparente ao clicar no botão "Publicar"
publicarBtn.addEventListener('click', () => {
    overlay.style.display = 'flex';  // Exibe a tela semitransparente
});

// Fechar a tela semitransparente ao clicar no botão "Fechar"
fecharOverlayBtn.addEventListener('click', () => {
    overlay.style.display = 'none';  // Oculta a tela semitransparente
});

// Lógica para enviar a foto e a legenda para o backend
const publicarForm = document.getElementById('publicar-form');
publicarForm.addEventListener('submit', async (event) => {
    event.preventDefault();  // Impede o comportamento padrão do formulário

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
                "Authorization": `Bearer ${accessToken}`,  // Envia o token JWT no cabeçalho
                // NÃO defina "Content-Type" manualmente, o navegador fará isso automaticamente
            },
            body: formData,  // Envia o FormData
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