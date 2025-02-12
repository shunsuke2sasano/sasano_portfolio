document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded fired");

    const deleteButtons = document.querySelectorAll(".delete-btn");

    const csrfTokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

    deleteButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            const userId = this.getAttribute("data-id");
            if (!userId) {
                console.error("User ID not found on button:", this);
                return;
            }

            const url = `/accounts/account_delete/${userId}/`;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
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
                        // 対象行を削除
                        const row = document.querySelector(`#account-row-${userId}`);
                        if (row) {
                            row.remove();
                        }
                        alert(data.message);
                    } else {
                        alert("エラー: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    alert("削除処理中にエラーが発生しました。");
                });
        });
    });
});
