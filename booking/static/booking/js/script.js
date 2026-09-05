document.querySelectorAll('[data-confirm-cancel]').forEach((button) => {
    button.addEventListener('click', (event) => {
        if (!window.confirm('Cancel this booking?')) {
            event.preventDefault();
        }
    });
});
