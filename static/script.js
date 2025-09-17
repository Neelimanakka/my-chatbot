// Select elements
const chatBody = document.querySelector('.chat-body');
const messagesContainer = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');

// Toggle chat open/close
function toggleChat() {
    chatBody.classList.toggle('open');
}

// Add message to chat
function addMessage(text, sender) {
    const message = document.createElement('div');
    message.classList.add('message', sender);
    message.innerText = text;
    messagesContainer.appendChild(message);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return message;
}

// Typing indicator
function addTypingIndicator() {
    const typing = document.createElement('div');
    typing.classList.add('message', 'bot');
    typing.innerHTML = '<span class="typing">...</span>';
    messagesContainer.appendChild(typing);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return typing;
}

function removeTypingIndicator(typingElem) {
    messagesContainer.removeChild(typingElem);
}

// Display message letter by letter
function displayMessageLetterByLetter(messageElem, text) {
    let index = 0;
    messageElem.innerHTML = '';

    const interval = setInterval(() => {
        messageElem.innerHTML = text.slice(0, index + 1);
        index++;
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        if (index >= text.length) clearInterval(interval);
    }, 50);
}

// Send message function
function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    messageInput.value = '';

    const typingIndicator = addTypingIndicator();

    // ✅ Correct backend URL
    fetch("https://my-chatbot-backend.onrender.com/chat", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
        removeTypingIndicator(typingIndicator);
        if (data.reply) {
            const botMessage = addMessage('', 'bot');
            displayMessageLetterByLetter(botMessage, data.reply);
        } else {
            addMessage("❌ Something went wrong.", 'bot');
        }
    })
    .catch(err => {
        removeTypingIndicator(typingIndicator);
        addMessage("❌ Sorry, something went wrong.", 'bot');
        console.error('Error:', err);
    });
}

// Send message on Enter key
messageInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") sendMessage();
});
