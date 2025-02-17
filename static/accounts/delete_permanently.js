document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ delete_permanently.js が正常に読み込まれました！");

    // 完全削除ボタンをすべて取得
    document.querySelectorAll(".delete-permanently-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // ← これを追加してフォームの通常送信をキャンセル

            const accountId = this.dataset.id; // ボタンの data-id 取得
            console.log(`🛑 完全削除ボタンがクリックされました！アカウントID: ${accountId}`);

            if (!confirm("本当にこのアカウントを完全に削除しますか？")) {
                console.log("⛔ 削除キャンセルされました");
                return;
            }

            fetch(`/accounts/account_delete_permanently/${accountId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("meta[name='csrf-token']").content,
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())  // JSONレスポンスを取得
            .then(data => {
                console.log("🔄 削除レスポンス:", data);
                if (data.success) {
                    alert(data.message);
                    console.log(`✅ 削除成功: user-row-${accountId}`);
                    // 削除対象の行を削除
                    const row = document.getElementById(`user-row-${accountId}`);
                    if (row) {
                        row.remove();
                        console.log(`🗑️ アカウントID ${accountId} の行を削除しました。`);
                    } else {
                        console.error(`❌ user-row-${accountId} が見つかりません。`);
                    }
                } else {
                    console.error("❌ 削除エラー:", data.message);
                    alert("削除に失敗しました: " + data.message);
                }
            })
            .catch(error => console.error("⚠️ Fetchエラー:", error));
        });
    });
});

