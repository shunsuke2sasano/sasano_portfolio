document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded fired");

    // CSRFトークンの取得
    const csrfTokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

    if (!csrfToken) {
        console.error("CSRF token not found in the DOM!");
        return;
    }

    // 復元ボタン
    const restoreButtons = document.querySelectorAll(".restore-btn");

    restoreButtons.forEach(button => {
        button.addEventListener("click", function () {
            const accountId = this.getAttribute("data-id");

            if (!accountId) {
                console.error("Account ID not found!");
                return;
            }

            fetch(`/accounts/account_restore/${accountId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        // ページをリロードして変更を反映
                        location.reload();
                    } else {
                        alert("復元に失敗しました: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    alert("復元処理中にエラーが発生しました。");
                });
        });
    });
});
