document.addEventListener("DOMContentLoaded", () => {

    // VARIABLES
    const textarea = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const newChatBtn = document.getElementById("new-chat");
    const chatList = document.getElementById("chat-list");
    const chatWindow = document.getElementById("chat-window");
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".sidebar");
    const container = document.querySelector(".container");
    const branding = document.getElementById("branding");
    const linksInMessage = document.getElementsByClassName("link-in-message");

    // alternating refresh and delete chat buttons depending on context
    chatList.addEventListener("click", async (e) => {
        const btn = e.target.closest(".delete-chat");
        if (!btn) return;

        const chatId = btn.dataset.chatId;

        // refresh chat
        if (btn.classList.contains("refresh-chat")) {
            const res = await fetch(`/reset_chat/${chatId}`, {
                method: "POST",
            });
            const data = await res.json();
            window.location.href = `/chat/${data.chat_id}`;
            return;
        }

        // delete chat
        const res = await fetch(`/delete_chat/${chatId}`, {
            method: "DELETE",
        });
        const data = await res.json();

        window.location.href = data.chat_id
            ? `/chat/${data.chat_id}`
            : `/`;
    });


    // collapse sidebar
    menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        container.classList.toggle("collapsed");
        branding.classList.toggle('hidden');
    });


    // popup to show system status (eg. Normal)
    const systemPopup = document.getElementById("system-status-popup");

    async function updateSystemStatus() {
        try {
            const res = await fetch("/system_status");
            const data = await res.json();
            systemPopup.textContent = `PBS status: ${data.status}`;
        } catch (err) {
            systemPopup.textContent = "PBS status: Error ❌";
            console.error(err);
        }
    }

    // run immediately, then every 60s
    updateSystemStatus();
    setInterval(updateSystemStatus, 60000);

    // allow only one faq accordion to be open at a time
    const faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach((item) => {
        item.addEventListener("toggle", () => {
            if (item.open) {
                faqItems.forEach((other) => {
                    if (other !== item) {other.removeAttribute("open");}
                });
            }
        });
    });

    if (textarea && sendBtn) {
        // click enter key to send message
        textarea.addEventListener("keydown", function (e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendBtn.click();
            }
        });

        // auto resize input text area
        textarea.addEventListener("input", function () {
            this.style.height = "auto";
            this.style.height = this.scrollHeight + "px";
        });

        // send message
        sendBtn.addEventListener("click", async () => {
            const userMessage = textarea.value.trim();
            if (!userMessage) return;

            textarea.value = "";
            textarea.style.height = "auto";

            // adding user message to UI
            const userDiv = document.createElement("div");
            userDiv.classList.add("message", "human");
            userDiv.innerHTML = `<p>${userMessage}</p>`;
            chatWindow.appendChild(userDiv);
            scrollToBottom();

            // sending to backend
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

            // adding AI reply to UI
            const aiDiv = document.createElement("div");
            aiDiv.classList.add("message", "ai");
            aiDiv.innerHTML = `<p>${data.reply}</p>`;
            chatWindow.appendChild(aiDiv);
            scrollToBottom();

            // marking chat as 'hasUserMessages' for delete button
            const currentChatBtn = chatList.querySelector(
                `.delete-chat[data-chat-id="${data.chat_id}"]`
            );

            if (currentChatBtn) {
                currentChatBtn.dataset.hasUserMessages = "true";
            }

            // re-check refresh/delete logic immediately
            updateSingleChatButton();
        });
    }

    if (chatWindow) {
        // scroll chat to bottom
        function scrollToBottom() {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
        scrollToBottom();
    }

    // create new chat
    if (newChatBtn) {
        newChatBtn.addEventListener("click", async () => {
            const res = await fetch("/new_chat", { method: "POST" });
            const data = await res.json();
            window.location.href = `/chat/${data.chat_id}`;
        });
    } 

    // context for changing refresh / delete chat button
    function updateSingleChatButton() {
        const chatItems = chatList.querySelectorAll("li");
        if (chatItems.length !== 1) return;

        const btn = chatItems[0].querySelector(".delete-chat");
        if (!btn) return;

        const hasUserMessages = btn.dataset.hasUserMessages === "true";

        // show delete button
        if (hasUserMessages && btn.classList.contains("refresh-chat")) {
            btn.innerHTML = "&#x2716;";
            btn.classList.remove("refresh-chat");
        }

        // show refresh button
        if (!hasUserMessages && !btn.classList.contains("refresh-chat")) {
            btn.innerHTML = "&#128472;";
            btn.classList.add("refresh-chat");
        }
    }

    // run once on page load
    updateSingleChatButton();

    // Add in code for clicking link in message
    // Loops through all the links and add listener
    const linksInMessageArray = Array.from(linksInMessage)
    linksInMessageArray.forEach(function (elem) {
        elem.addEventListener("click", async () => {
            // Listener -> Populate Message Box -> Click Send Btn
            setTimeout(() => {
                textarea.value = elem.textContent;
            }, 100);

            setTimeout(() => {
                sendBtn.click();
            }, 500);

        })
    })

});