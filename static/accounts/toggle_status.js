document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded fired");

    const toggleButtons = document.querySelectorAll(".toggle-status-btn");

    if (toggleButtons.length === 0) {
        console.error("No toggle buttons found!");
        return;
    }

    toggleButtons.forEach(button => {
        console.log("Registering click event for button:", button);
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const userId = this.getAttribute("data-id");
            console.log("Button clicked. User ID:", userId);

            const url = `/accounts/toggle_status/${userId}/`;
            console.log("Preparing to send fetch request to:", url);

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
            })
                .then(response => {
                    console.log("Response received:", response);
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Data received:", data);
                    if (data.success) {
                        alert(data.message);
                        const statusCell = document.querySelector(`#account-row-${userId}`).children[2];
                        if (statusCell) {
                            statusCell.textContent = data.is_active ? "有効" : "無効";
                        }
                        this.textContent = data.is_active ? "無効化" : "有効化";
                    } else {
                        alert("エラー: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    alert("ステータス変更中にエラーが発生しました。");
                });
        });
    });
});
