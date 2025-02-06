// アイテム追加処理
document.getElementById("add-item-btn").addEventListener("click", function () {
    const itemName = document.getElementById("new-item-name").value;
    const location = document.getElementById("new-item-location").value;
    const link = document.getElementById("new-item-link").value;

    // Ajaxリクエスト
    fetch("/add_item", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            item_name: itemName,
            location: location,
            link: link
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                const itemList = document.getElementById("item-list");
                const newItem = document.createElement("li");
                newItem.setAttribute("data-item-id", data.item_id);
                newItem.innerHTML = `
                <strong>${data.item_name}</strong>
                <p>場所: ${data.location}</p>
                <p>リンク: <a href="${data.link}" target="_blank">${data.link}</a></p>
                <button class="delete-item-btn" data-item-id="${data.item_id}">削除</button>
            `;
                itemList.appendChild(newItem);
                document.getElementById("new-item-name").value = '';
                document.getElementById("new-item-location").value = '';
                document.getElementById("new-item-link").value = '';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            alert("Error adding item.");
        });
});

// アイテム削除
document.getElementById("item-list").addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-item-btn")) {
        const itemId = event.target.getAttribute("data-item-id");
        if (confirm("本当に削除しますか？")) {
            fetch(`/delete_item/${itemId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        const itemElement = document.querySelector(`li[data-item-id="${itemId}"]`);
                        if (itemElement) {
                            itemElement.remove();
                        }
                        alert(data.message);
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    alert("削除中にエラーが発生しました: " + error);
                });
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const editButtons = document.querySelectorAll(".edit-item-btn");
    const saveEditButton = document.getElementById("save-edit-btn");
    const closeModalButton = document.getElementById("close-edit-modal-btn");
    const editModal = document.getElementById("edit-modal");

    // 編集ボタンのクリックイベント
    editButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const itemId = button.getAttribute("data-item-id");
            const itemElement = document.querySelector(`li[data-item-id="${itemId}"]`);

            // モーダルに現在の値をセット
            document.getElementById("edit-item-id").value = itemId;
            document.getElementById("edit-item-name").value = itemElement.querySelector("strong").textContent;
            document.getElementById("edit-item-location").value = itemElement.querySelector("p:nth-of-type(1)").textContent.replace("場所: ", "");
            document.getElementById("edit-item-link").value = itemElement.querySelector("p:nth-of-type(2) a").textContent;

            // モーダルを表示
            editModal.style.display = "block";
        });
    });

    // 保存ボタンのクリックイベント
    saveEditButton.addEventListener("click", async () => {
        const itemId = document.getElementById("edit-item-id").value;
        const name = document.getElementById("edit-item-name").value;
        const location = document.getElementById("edit-item-location").value;
        const link = document.getElementById("edit-item-link").value;

        try {
            const response = await fetch(`/edit_item/${itemId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, location, link }),
            });

            const data = await response.json();
            if (response.ok) {
                alert("アイテムが更新されました！");
                // ページをリロードして最新データを取得
                window.location.reload();
            } else {
                alert(`エラー: ${data.message}`);
            }
        } catch (error) {
            console.log("更新中にエラーが発生しました。");
            console.error(error);
        }
    });

    // モーダルを閉じるボタン
    closeModalButton.addEventListener("click", () => {
        editModal.style.display = "none";
    });
});



// 共有モーダルの表示
document.getElementById("share-item-btn").addEventListener("click", function () {
    document.getElementById("share-modal").style.display = "block";
});

// モーダルを閉じる
document.getElementById("close-modal-btn").addEventListener("click", function () {
    document.getElementById("share-modal").style.display = "none";
});

// Discordで共有及びJsonデータ整理
document.getElementById("share-discord-btn").addEventListener("click", function() {
    fetch("/run_discord_bot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => alert("エラーが発生しました: " + error));
});

// Gmailで共有
document.getElementById("share-gmail-btn").addEventListener("click", function () {
    const items = Array.from(document.querySelectorAll("#item-list li")).map(item => {
        const name = item.querySelector("strong").innerText;
        const location = item.querySelector("p:nth-of-type(1)").innerText.replace("場所: ", "");
        const link = item.querySelector("a").getAttribute("href");
        return `店名: ${name}, 場所: ${location}, リンク: ${link}`;
    });
    const subject = encodeURIComponent("おすすめ飲食店リスト");
    const body = encodeURIComponent(items.join("\n"));
    const mailtoUrl = `mailto:?subject=${subject}&body=${body}`;
    window.open(mailtoUrl, "_blank");
});
