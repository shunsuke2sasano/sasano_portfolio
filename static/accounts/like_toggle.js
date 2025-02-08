document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.getAttribute('data-user-id');
            fetch(likeToggleUrl, {
                method: 'POST',
                headers: { 
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ 'user_id': userId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.textContent = `👍 ${data.likes_count}`;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
