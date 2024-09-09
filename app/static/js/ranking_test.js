function atualizarMudancas() {
    const codigosParaRemover = [];
    const codigosParaReconsiderar = [];

    // Coleta os códigos dos imóveis marcados para remoção
    document.querySelectorAll('.remove-checkbox:checked').forEach(checkbox => {
        codigosParaRemover.push(checkbox.getAttribute('data-id'));
    });

    // Coleta os códigos dos imóveis marcados para reconsideração
    document.querySelectorAll('.reconsider-checkbox:checked').forEach(checkbox => {
        codigosParaReconsiderar.push(checkbox.getAttribute('data-id'));
    });



    // Executa a remoção se houver códigos para remover
    if (codigosParaRemover.length > 0) {
        $.ajax({
            url: '/remover_imovel',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ codigo: codigosParaRemover }),  // Ajustado para enviar como lista sob uma chave 'codigo'
            success: function(response) {
                console.log("Remoção bem-sucedida:", response.message);
                location.reload();  // Recarrega a página após sucesso
            },
            error: function() {
                alert('Erro ao remover os imóveis.');
            }
        });
    }

    
    // Executa a reconsideração se houver códigos para reconsiderar
    if (codigosParaReconsiderar.length > 0) {
        $.ajax({
            url: '/reconsiderar_imovel',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ codigo: codigosParaReconsiderar }),  // Ajustado para enviar como lista sob uma chave 'codigo'
            success: function(response) {
                console.log("Reconsideração bem-sucedida:", response.message);
                location.reload();  // Recarrega a página após sucesso
            },
            error: function() {
                alert('Erro ao reconsiderar os imóveis.');
            }
        });
    }

    // Se não houver nenhum código para processar, simplesmente recarrega a página
    if (codigosParaRemover.length === 0 && codigosParaReconsiderar.length === 0) {
        alert('Nenhum imóvel selecionado para atualizar.');
        location.reload();  // Recarrega a página para refrescar o estado
    }
}