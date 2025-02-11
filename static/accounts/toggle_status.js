document.addEventListener("DOMContentLoaded", function () {
    const toggleButtons = document.querySelectorAll(".toggle-status-btn");

    toggleButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const accountId = button.getAttribute("data-id");
            const url = `/accounts/toggle_status/${accountId}/`;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        alert(data.message);
                        // ボタンの表示を切り替える
                        location.reload();
                    } else {
                        alert("エラー: " + data.message);
                    }
                })
                .catch((error) => {
                    console.error("エラーが発生しました:", error);
                    alert("ステータス変更処理中に問題が発生しました。");
                });
        });
    });
});

