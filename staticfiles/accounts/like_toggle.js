document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const userId = button.dataset.userId; // ボタンに設定された data-user-id を取得
            if (!userId) {
                console.error('User ID not found on the button.');
                return;
            }

            const likeToggleUrl = `/accounts/like_toggle/${userId}/`; // DjangoビューのURL

            try {
                // Fetch APIで非同期リクエスト
                const response = await fetch(likeToggleUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken, // DjangoのCSRFトークン
                    },
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();

                if (data.success) {
                    // ボタンのテキストを更新
                    button.textContent = `👍 ${data.likes}`;
                } else {
                    console.error('Failed to toggle like:', data.error);
                }
            } catch (error) {
                console.error('Error occurred while toggling like:', error);
            }
        });
    });
});



