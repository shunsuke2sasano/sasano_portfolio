document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const accountId = this.getAttribute("data-id");  // `account.id` を取得

            if (!accountId) {
                console.error("Account ID not found!");
                return;
            }

            if (!confirm("本当にこのアカウントを完全に削除しますか？")) {
                return;
            }

            fetch(`/accounts/account_delete/${accountId}/`, {  // 修正
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("meta[name='csrf-token']").content,
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    location.reload();  // 画面をリロードして削除を反映
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
