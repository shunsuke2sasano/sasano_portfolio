document.addEventListener("DOMContentLoaded", function () {
    const generalFields = document.querySelector(".general-fields");
    const accountTypeRadios = document.querySelectorAll("input[name='account_type']");
    const updateButton = document.querySelector("button[type='submit']"); // 更新ボタンを取得
    const form = document.querySelector("form"); // フォーム全体を取得
    const statusRadios = document.querySelectorAll("input[name='status']");
    
    // ステータスの変更イベント
    statusRadios.forEach(radio => {
        radio.addEventListener("change", function () {
            console.log(`ステータスが変更されました: ${this.value}`);
        });
    });
    // バリデーションエラーをクリアする関数
    function clearValidationErrors() {
        const errorMessages = document.querySelectorAll(".validation-error");
        errorMessages.forEach(error => {
            error.textContent = ""; // エラーメッセージを削除
        });
    }

    // 入力項目の表示/非表示を切り替える関数
    function toggleFields() {
        generalFields.style.display = accountTypeRadios[0].checked ? "block" : "none";
    }

    // ラジオボタンの変更時にバリデーションエラーを消去し、フィールド表示を更新
    accountTypeRadios.forEach(radio => {
        radio.addEventListener("change", function () {
            clearValidationErrors(); // エラー消去
            toggleFields(); // フィールドの切り替え
        });
    });

    // フォーム送信時にバリデーションエラーを消去
    if (form) {
        form.addEventListener("submit", function (event) {
            clearValidationErrors(); // エラー消去
            // フォーム送信を続行（デフォルト動作）
        });
    }

    // ページ初期表示時に適用
    toggleFields();
});

