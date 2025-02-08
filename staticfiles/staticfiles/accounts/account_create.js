document.addEventListener('DOMContentLoaded', function () {
    const generalRadio = document.getElementById('generalRadio');
    const adminRadio = document.getElementById('adminRadio');
    const generalFields = document.getElementById('generalFields');
    const adminFields = document.getElementById('adminFields');

    // フィールドの有効/無効を切り替える関数
    function toggleFields() {
        if (generalRadio.checked) {
            generalFields.style.display = 'block';
            adminFields.style.display = 'none';

            // 無効化/有効化
            generalFields.querySelectorAll('input, select, textarea').forEach(field => field.disabled = false);
            adminFields.querySelectorAll('input, select, textarea').forEach(field => field.disabled = true);
        } else if (adminRadio.checked) {
            generalFields.style.display = 'none';
            adminFields.style.display = 'block';

            // 無効化/有効化
            generalFields.querySelectorAll('input, select, textarea').forEach(field => field.disabled = true);
            adminFields.querySelectorAll('input, select, textarea').forEach(field => field.disabled = false);
        }
    }

    // 初期化（ページロード時に適用）
    toggleFields();

    // ラジオボタンの変更イベントでフォームを切り替える
    generalRadio.addEventListener('change', toggleFields);
    adminRadio.addEventListener('change', toggleFields);
});
