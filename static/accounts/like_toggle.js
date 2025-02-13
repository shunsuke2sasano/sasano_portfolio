document.addEventListener('DOMContentLoaded', () => {
  const likeButtons = document.querySelectorAll('.like-btn');

  likeButtons.forEach(button => {
    button.dataset.liked = "false";

    button.addEventListener('click', async () => {
      if (button.disabled) return;
      
      // data-profile-id を取得
      const profileId = button.dataset.profileId;
      if (!profileId) {
        console.error('Profile ID not found on the button.');
        return;
      }
      
      button.disabled = true;
      const likeToggleUrl = getLikeToggleUrl(profileId);

      try {
        const response = await fetch(likeToggleUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Data:', data);

        if (data.success) {
          button.dataset.liked = data.liked ? "true" : "false";

          if (data.liked) {
            button.textContent = `取消 👍 ${data.likes}`;
          } else {
            button.textContent = `いいね 👍 ${data.likes}`;
          }
        } else {
          console.error('Failed to toggle like:', data.error);
        }
      } catch (error) {
        console.error('Error occurred while toggling like:', error);
      } finally {
        button.disabled = false;
      }
    });
  });
});
