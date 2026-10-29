document.addEventListener('DOMContentLoaded', () => {
    // Esconder mensagens Flash automaticamente após 5 segundos
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // Confirmação para formulários de remoção de jogos
    const deleteForms = document.querySelectorAll('.form-deletar-jogo');
    deleteForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const nomeJogo = form.getAttribute('data-nome') || 'este jogo';
            const confirmacao = confirm(`Tem certeza que deseja excluir o jogo "${nomeJogo}"? Esta ação não poderá ser desfeita.`);
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });
});
