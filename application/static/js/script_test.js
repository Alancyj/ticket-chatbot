document.addEventListener("DOMContentLoaded", () => {

    // ===============================
    // Variables
    // ===============================
    const textarea = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const newChatBtn = document.getElementById("new-chat");
    const chatList = document.getElementById("chat-list");
    const chatWindow = document.getElementById("chat-window");
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".sidebar");
    const container = document.querySelector(".container");

    chatList.addEventListener("click", async (e) => {
      const btn = e.target.closest(".delete-chat");
      if (!btn) return;

      const chatId = btn.dataset.chatId;

      // Refresh chat
      if (btn.classList.contains("refresh-chat")) {
          const res = await fetch(`/reset_chat/${chatId}`, {
              method: "POST",
          });
          const data = await res.json();
          window.location.href = `/chat/${data.chat_id}`;
          return;
      }

      // Delete chat
      const res = await fetch(`/delete_chat/${chatId}`, {
          method: "DELETE",
      });
      const data = await res.json();

      window.location.href = data.chat_id
          ? `/chat/${data.chat_id}`
          : `/`;
  });


  // ===============================
  // Sidebar collapse
  // ===============================
  menuToggle.addEventListener("click", () => {
      sidebar.classList.toggle("collapsed");
      container.classList.toggle("collapsed");
  });


  // ===============================
  // System status popup
  // ===============================
  const systemPopup = document.getElementById("system-status-popup");

  async function updateSystemStatus() {
      try {
          const res = await fetch("/system_status");
          const data = await res.json();
          systemPopup.textContent = `System performance: ${data.status}`;
      } catch (err) {
          systemPopup.textContent = "System performance: Error ❌";
          console.error(err);
      }
  }

  // Run immediately and then every 60 seconds
  updateSystemStatus();
  setInterval(updateSystemStatus, 60000);


  // ===============================
  // Enter to send message
  // ===============================
  textarea.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          sendBtn.click();
      }
  });

  // ===============================
  // Auto-resize textarea
  // ===============================
  textarea.addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
  });

  // ===============================
  // Scroll chat to bottom
  // ===============================
  function scrollToBottom() {
      chatWindow.scrollTop = chatWindow.scrollHeight;
  }
  scrollToBottom();

  // ===============================
  // Create new chat
  // ===============================
  newChatBtn.addEventListener("click", async () => {
      const res = await fetch("/new_chat", { method: "POST" });
      const data = await res.json();
      window.location.href = `/chat/${data.chat_id}`;
  });

  // ===============================
  // 🔥 SINGLE CHAT BUTTON LOGIC
  // ===============================
  function updateSingleChatButton() {
      const chatItems = chatList.querySelectorAll("li");
      if (chatItems.length !== 1) return;

      const btn = chatItems[0].querySelector(".delete-chat");
      if (!btn) return;

      const hasUserMessages = btn.dataset.hasUserMessages === "true";

      // ---- SHOW DELETE BUTTON ----
      if (hasUserMessages && btn.classList.contains("refresh-chat")) {
          btn.innerHTML = "&#x2716;";
          btn.classList.remove("refresh-chat");

          // const deleteBtn = btn.cloneNode(true);
          // btn.replaceWith(deleteBtn);

          // deleteBtn.addEventListener("click", async () => {
          //     const res = await fetch(
          //         "/delete_chat/" + deleteBtn.dataset.chat_id,
          //         { method: "DELETE" }
          //     );
          //     const data = await res.json();
          //     window.location.href = data.chat_id
          //         ? `/chat/${data.chat_id}`
          //         : `/`;
          // });
      }

      // ---- SHOW REFRESH BUTTON ----
      if (!hasUserMessages && !btn.classList.contains("refresh-chat")) {
          btn.innerHTML = "&#128472;";
          btn.classList.add("refresh-chat");

          // const refreshBtn = btn.cloneNode(true);
          // btn.replaceWith(refreshBtn);

          // refreshBtn.addEventListener("click", async () => {
          //     const chatId = refreshBtn.dataset.chatId;
          //     const res = await fetch(`/reset_chat/${chatId}`, {
          //         method: "POST",
          //     });
          //     const data = await res.json();
          //     window.location.href = `/chat/${data.chat_id}`;
          // });
      }
  }

  // Run once on page load
  updateSingleChatButton();

  // // ===============================
  // // Delete chat buttons (normal case)
  // // ===============================
  // document.querySelectorAll(".delete-chat").forEach(btn => {
  //     btn.addEventListener("click", async () => {
  //         const res = await fetch(
  //             "/delete_chat/" + btn.dataset.chat_id,
  //             { method: "DELETE" }
  //         );
  //         const data = await res.json();
  //         window.location.href = data.chat_id
  //             ? `/chat/${data.chat_id}`
  //             : `/`;
  //     });
  // });

  // ===============================
  // Send message
  // ===============================
  sendBtn.addEventListener("click", async () => {
      const userMessage = textarea.value.trim();
      if (!userMessage) return;

      textarea.value = "";
      textarea.style.height = "auto";

      // ---- Add user message to UI ----
      const userDiv = document.createElement("div");
      userDiv.classList.add("message", "human");
      userDiv.innerHTML = `<p>${userMessage}</p>`;
      chatWindow.appendChild(userDiv);
      scrollToBottom();

      // ---- Send to backend ----
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

      // ---- Add AI reply ----
      const aiDiv = document.createElement("div");
      aiDiv.classList.add("message", "ai");
      aiDiv.innerHTML = `<p>${data.reply}</p>`;
      chatWindow.appendChild(aiDiv);
      scrollToBottom();

      // ===============================
      // 🔥 IMPORTANT PART
      // Mark chat as having user messages
      // ===============================
      const currentChatBtn = chatList.querySelector(
          `.delete-chat[data-chat-id="${data.chat_id}"]`
      );

      if (currentChatBtn) {
          currentChatBtn.dataset.hasUserMessages = "true";
      }

      // Re-check refresh/delete logic instantly
      updateSingleChatButton();
  });

});