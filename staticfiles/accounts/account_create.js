document.addEventListener("DOMContentLoaded", function () {
    const restoreButtons = document.querySelectorAll(".restore-btn");

    restoreButtons.forEach(button => {
        button.addEventListener("click", function () {
            const userId = this.getAttribute("data-id");
            if (!userId) {
                console.error("User ID not found!");
                return;
            }

            fetch(`/accounts/account_restore/${userId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
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

