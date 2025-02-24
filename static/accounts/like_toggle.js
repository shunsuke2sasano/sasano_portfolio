document.addEventListener('DOMContentLoaded', () => {
  const likeButtons = document.querySelectorAll('.like-btn');

  likeButtons.forEach(button => {
    button.addEventListener('click', async () => {
      // data-profile-id を取得
      const profileId = button.dataset.profileId;
      if (!profileId) {
        console.error('Profile ID not found on the button.');
        return;
      }
      
      button.disabled = true;
      // URL生成（例: /accounts/like_toggle/<id>/）
      const likeToggleUrl = `/accounts/like_toggle/${profileId}/`;
      const csrfToken = "{{ csrf_token|safe }}";  // テンプレート側で埋め込む

      try {
        const response = await fetch(likeToggleUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({}),
        });

        if (!response.ok) {
          // 403の場合、ログインページにリダイレクトする
          if (response.status === 403) {
            const data = await response.json();
            if (data.redirect) {
              window.location.href = data.redirect;
              return;
            }
          }
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('Data:', data);

        if (data.success) {
          if (data.liked) {
            button.textContent = `取消 👍 ${data.likes}`;
          } else {
            button.textContent = `いいね 👍 ${data.likes}`;
          }
        } else {
          alert('Failed to toggle like: ' + data.message);
        }
      } catch (error) {
        console.error('Error occurred while toggling like:', error);
      } finally {
        button.disabled = false;
      }
    });
  });
});
