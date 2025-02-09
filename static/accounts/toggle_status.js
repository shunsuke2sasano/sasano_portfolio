document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded fired");

    // すべてのトグルボタンを取得
    const toggleButtons = document.querySelectorAll(".toggle-status-btn");

    // トグルボタンが見つからない場合はエラーメッセージを表示して終了
    if (toggleButtons.length === 0) {
        console.error("No toggle buttons found!");
        return;
    }

    // CSRFトークンの取得
    const csrfTokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    if (!csrfTokenElement) {
        console.error("CSRF token not found in the DOM!");
        return;
    }
    const csrfToken = csrfTokenElement.value;

    // 各ボタンにクリックイベントを登録
    toggleButtons.forEach(button => {
        console.log("Registering click event for button:", button);

        button.addEventListener("click", function (event) {
            event.preventDefault();

            // ボタンからユーザーIDを取得
            const userId = this.getAttribute("data-id");
            if (!userId) {
                console.error("User ID not found on button:", this);
                return;
            }
            console.log("Button clicked. User ID:", userId);

            // APIリクエストのURLを構築
            const url = `/accounts/toggle_status/${userId}/`;
            console.log("Preparing to send fetch request to:", url);

            // 非同期リクエストを送信
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
            })
                .then(response => {
                    console.log("Response received:", response);

                    // レスポンスがエラーの場合は例外をスロー
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Data received:", data);

                    if (data.success) {
                        // 成功した場合、UIを更新
                        alert(data.message);

                        // ユーザーのステータス表示を更新
                        const statusCell = document.querySelector(`#account-row-${userId} .status-cell`);
                        if (statusCell) {
                            statusCell.textContent = data.is_active ? "有効" : "無効";
                        }

                        // ボタンのテキストを更新
                        this.textContent = data.is_active ? "無効化" : "有効化";
                    } else {
                        alert("エラー: " + data.message);
                    }
                })
                .catch(error => {
                    // エラーハンドリング
                    console.error("Fetch error:", error);
                    alert("ステータス変更中にエラーが発生しました。");
                });
        });
    });
});
