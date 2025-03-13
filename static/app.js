class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const inputField = chatBox.querySelector('input');
        inputField.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const text1 = textField.value;

        if (text1 === "") {
            return;
        }

        const userMessage = { name: "User", message: text1 };
        this.messages.push(userMessage);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                const botMessage = { name: "Paynow", message: data.answer };
                this.messages.push(botMessage);
                this.updateChatText(chatbox);
                textField.value = '';
            })
            .catch((error) => {
                console.error('Error:', error);
                const errorMessage = { name: "Paynow", message: "Oops! Something went wrong." };
                this.messages.push(errorMessage);
                this.updateChatText(chatbox);
                textField.value = '';
            });
    }

    updateChatText(chatbox) {
        let html = '';
        this.messages.slice().reverse().forEach((item) => {
            if (item.name === "Paynow") {
                html += `<div class="messages__item messages__item--visitor">${item.message}</div>`;
            } else {
                html += `<div class="messages__item messages__item--operator">${item.message}</div>`;
            }
        });

        const chatMessages = chatbox.querySelector('.chatbox__messages');
        chatMessages.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();
