document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded fired"); // イベント確認用ログ

    const toggleButtons = document.querySelectorAll(".toggle-status-btn");

    if (toggleButtons.length === 0) {
        console.error("No toggle buttons found!");
        return;
    }

    toggleButtons.forEach(button => {
        console.log("Registering click event for button:", button); // ボタン確認ログ
        button.addEventListener("click", function (event) {
            event.preventDefault(); // デフォルトの動作を無効化
            const userId = this.getAttribute("data-id");
            console.log("Button clicked. User ID:", userId); // クリック確認ログ

            const url = `/accounts/toggle_status/${userId}/`;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
            })
                .then(response => {
                    console.log("Response received:", response); // レスポンス確認ログ
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Data received:", data); // データ確認ログ
                    if (data.success) {
                        alert(data.message);
                        // ステータス表示を更新する
                        const statusCell = document.querySelector(`#account-row-${userId} td:nth-child(3)`);
                        if (statusCell) {
                            statusCell.textContent = data.is_active ? "有効" : "無効";
                        }
                        this.textContent = data.is_active ? "無効化" : "有効化"; // ボタンのラベル更新
                    } else {
                        alert("エラー: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error); // エラー確認ログ
                    alert("ステータス変更中にエラーが発生しました。");
                });
        });
    });
});

