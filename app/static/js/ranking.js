function enviarRequisicao(url, data, sucessoCallback, erroCallback) {
    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: sucessoCallback,
        error: erroCallback || function() {
            alert('Erro ao processar a requisição.');
        }
    });
}

function atualizarMudancas() {
    const codigosParaRemover = [];
    const codigosParaReconsiderar = [];

    document.querySelectorAll('.remove-checkbox:checked').forEach(checkbox => {
        codigosParaRemover.push(checkbox.getAttribute('data-id'));
    });

    document.querySelectorAll('.reconsider-checkbox:checked').forEach(checkbox => {
        codigosParaReconsiderar.push(checkbox.getAttribute('data-id'));
    });

    if (codigosParaRemover.length > 0) {
        enviarRequisicao('/remover_imovel', { codigo: codigosParaRemover }, function(response) {
            console.log("Remoção bem-sucedida:", response.message);
            location.reload();
        });
    }

    if (codigosParaReconsiderar.length > 0) {
        enviarRequisicao('/reconsiderar_imovel', { codigo: codigosParaReconsiderar }, function(response) {
            console.log("Reconsideração bem-sucedida:", response.message);
            location.reload();
        });
    }

    if (codigosParaRemover.length === 0 && codigosParaReconsiderar.length === 0) {
        alert('Nenhum imóvel selecionado para atualizar.');
        location.reload();
    }
}

function toggleFavorite(link) {
    fetch('/toggle_favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ link: link })
    })
    .then(response => {
        if (response.ok) {
            console.log('Favorito atualizado com sucesso');
        } else {
            console.error('Erro ao atualizar favorito');
        }
    })
    .catch(error => {
        console.error('Erro de conexão:', error);
    });
}

function saveNotes(codigo) {
    const anotacoes = document.getElementById(`notes${codigo}`).value;

    $.ajax({
        url: '/save_notes',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 
            codigo: codigo,  
            fonte: $(`.favorite[data-id="${codigo}"]`).data('link'),  // Pega o link da coluna "Fonte"
            comentario: anotacoes 
        }),
        success: function(response) {
            console.log('Anotações salvas com sucesso:', response.message);

            const successMessage = document.getElementById(`note-success-${codigo}`);
            successMessage.classList.remove('d-none');
            
            setTimeout(() => {
                successMessage.classList.add('d-none');
            }, 3000);
        },
        error: function() {
            alert('Erro ao salvar as anotações.');
        }
    });
}

function fetchNotes(codigo) {
    const link = $(`.favorite[data-id="${codigo}"]`).data('link');
    console.log("Link recebido para anotações:", link);

    fetch(`/get_notes?fonte=${encodeURIComponent(link)}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`notes${codigo}`).value = data.comentario || "";
        console.log('Anotações carregadas com sucesso:', data.comentario);
    })
    .catch(error => {
        console.error('Erro ao carregar as anotações:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // Função para abrir e fechar o menu dropdown
    const menuToggle = document.querySelector('.navbar .material-icons.menu-icon');
    const menuDropdown = document.querySelector('.dropdown-menu');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function (event) {
            menuDropdown.classList.toggle('show');
            event.stopPropagation();  // Evita que o clique no menu feche imediatamente
        });
    }

    // Fecha o menu ao clicar fora
    document.addEventListener('click', function(event) {
        if (!menuDropdown.contains(event.target) && !menuToggle.contains(event.target)) {
            menuDropdown.classList.remove('show');
        }
    });

    // Função para o ícone de atualizar (Agora faz o que é necessário)
    const refreshIcon = document.querySelector('.navbar .material-icons.refresh-icon');
    
    if (refreshIcon) {
        refreshIcon.addEventListener('click', function () {
            atualizarMudancas(); // Chama a função que você já tem para remover apartamentos
        });
    }

    // Recarregar favoritos
    fetch('/get_favorites')
    .then(response => response.json())
    .then(favorites => {
        const favoriteIcons = document.querySelectorAll('.favorite');

        favoriteIcons.forEach(icon => {
            if (favorites.includes(icon.getAttribute('data-link'))) {
                icon.innerText = 'favorite';
                icon.style.color = '#ff1744';
            }

            icon.addEventListener('click', handleFavoriteClick);
        });
    });
});

function handleFavoriteClick(event) {
    const favorite = event.currentTarget;
    const isFavorite = favorite.innerText === 'favorite';
    favorite.innerText = isFavorite ? 'favorite_border' : 'favorite';
    favorite.style.color = isFavorite ? '#ffffff' : '#ff1744';

    toggleFavorite(favorite.getAttribute('data-link'));
}