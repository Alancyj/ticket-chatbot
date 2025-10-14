document.addEventListener("DOMContentLoaded", () => {

    // Variables
    const textarea = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const newChatBtn = document.getElementById("new-chat");
    const delChatBtn = document.getElementsByClassName("delete-chat");
    const chatList = document.getElementById("chat-list");
    const chatWindow = document.getElementById("chat-window");
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".sidebar");
    const container = document.querySelector(".container");

    // Collapse sidebar using menu button
    menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        container.classList.toggle("collapsed");
    });

    // Send message with [Enter] key, insert line break with [Shift+Enter] keys
    textarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendBtn.click();
        }
    });

    // Auto-resize text area if message is too long
    textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });

    // Scroll chat window to bottom
    function scrollToBottom() {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
    scrollToBottom();

    // Create new chat with new chat button on sidebar
    newChatBtn.addEventListener("click", async () => {
        const res = await fetch("/new_chat", { method: "POST" });
        const data = await res.json();
        window.location.href = `/chat/${data.chat_id}`;
    });

    // Delete chat with delete chat button on sidebar
    const delChatBtnArray = Array.from(delChatBtn)

    delChatBtnArray.forEach(function (elem) {
        elem.addEventListener("click", async () => {
            const res = await fetch("/delete_chat/" + elem.dataset.chat_id, { method: "DELETE" });
            const data = await res.json();

            if (data.chat_id == null) {
                window.location.href = `/`
            } else {
                window.location.href = `/chat/${data.chat_id}`;
                // window.location.href = `/`
            }

        })
    })


    // Send message
    sendBtn.addEventListener("click", async () => {
        const userMessage = textarea.value.trim();
        if (!userMessage) return;

        textarea.value = "";
        textarea.style.height = "auto";

        // Add user message to chat window
        const userDiv = document.createElement("div");
        userDiv.classList.add("message", "human");
        userDiv.innerHTML = `<p>${userMessage}</p>`;
        chatWindow.appendChild(userDiv);
        scrollToBottom();

        // Send message to backend
        const res = await fetch("/send_message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage }),
        });
        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Add chatbot message to chat window
        const aiDiv = document.createElement("div");
        aiDiv.classList.add("message", "ai");
        aiDiv.innerHTML = `<p>${data.reply}</p>`;
        chatWindow.appendChild(aiDiv);
        scrollToBottom();

        // Update sidebar in real time (naming chat "Chat N")
        let chatLink = chatList.querySelector(`a[href="/chat/${data.chat_id}"]`);
        if (!chatLink) {
            const li = document.createElement("li");
            chatLink = document.createElement("a");
            chatLink.href = `/chat/${data.chat_id}`;

            // Always assign the next number (highest)
            chatLink.textContent = data.chat_title;
            li.appendChild(chatLink);

            // Insert at the top (newest first)
            chatList.insertBefore(li, chatList.firstChild);
        }


    });
});