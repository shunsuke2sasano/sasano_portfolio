document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded fired");

    // 削除ボタンの取得
    const deleteButtons = document.querySelectorAll(".delete-btn");

    // CSRFトークンの取得
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    if (!csrfToken) {
        console.error("CSRF token not found in the DOM!");
        return;
    }

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const userId = this.getAttribute("data-id");
            if (!userId) {
                console.error("User ID not found!");
                return;
            }

            if (!confirm("本当にこのアカウントを削除しますか？")) {
                return;
            }

            fetch(`/accounts/account_delete/${userId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        const row = document.getElementById(`account-row-${userId}`);
                        if (row) {
                            row.remove();
                        }
                    } else {
                        alert("削除に失敗しました: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    alert("削除処理中にエラーが発生しました。");
                });
        });
    });
});
