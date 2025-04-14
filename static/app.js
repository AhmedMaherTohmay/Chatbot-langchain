document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const messageInput = document.getElementById("message");
    const sendButton = document.getElementById("send-button");
    const chatboxToggle = document.getElementById("chatbox-toggle");
    const chatboxSupport = document.querySelector(".chatbox__support");

    // Toggle chat window visibility
    chatboxToggle.addEventListener("click", () => {
        chatboxSupport.classList.toggle("chatbox--active");
    });

    // Send message when the send button is clicked
    sendButton.addEventListener("click", async (event) => {
        event.preventDefault();
        await sendMessage();
    });

    // Send message when Enter key is pressed
    messageInput.addEventListener("keyup", async (event) => {
        if (event.key === "Enter") {
            await sendMessage();
        }
    });

    // Function to send a message
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Add the user's message to the chat log (aligned to the right)
        chatLog.innerHTML += `<div class="messages__item messages__item--visitor">${message}</div>`;
        messageInput.value = "";

        // Send the message to the server
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ messages: [{ role: "user", content: message }] }),
        });

        // Stream the response from the server
        const decoder = new TextDecoder();
        const reader = response.body.getReader();

        // Create a new element for the model's response (aligned to the left)
        const modelResponse = document.createElement("div");
        modelResponse.className = "messages__item messages__item--operator";
        chatLog.appendChild(modelResponse);

        // Function to add a delay
        const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

        // Read and display the streamed response with a delay
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const data = chunk.split('\n\n').filter(Boolean); // Split by double newlines to handle multiple SSE events

            for (const event of data) {
                if (event.startsWith('data: ')) {
                    const jsonData = JSON.parse(event.slice(6)); // Remove 'data: ' and parse JSON
                    const responseText = jsonData.response;

                    // Append the response character by character with a delay
                    for (let i = 0; i < responseText.length; i++) {
                        modelResponse.textContent += responseText[i];
                        await delay(30); // Adjust the delay time (in milliseconds) as needed
                        chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
                    }
                }
            }
        }
    }
});