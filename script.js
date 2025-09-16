// Select elements
const chatBody = document.querySelector('.chat-body');
const messagesContainer = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');

// Toggle chat open/close
function toggleChat() {
    chatBody.classList.toggle('open');
}

// Add a message to chat
function addMessage(text, sender) {
    const message = document.createElement('div');
    message.classList.add('message', sender);
    message.innerText = text;
    messagesContainer.appendChild(message);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return message;
}

// Show typing indicator
function addTypingIndicator() {
    const typing = document.createElement('div');
    typing.classList.add('message', 'bot');
    typing.innerHTML = '<span class="typing">...</span>';
    messagesContainer.appendChild(typing);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return typing;
}

// Remove typing indicator
function removeTypingIndicator(typingElem) {
    messagesContainer.removeChild(typingElem);
}

// Display message letter by letter

function displayMessageLetterByLetter(messageElem, text) {
    let index = 0;
    messageElem.innerHTML = ''; // use innerHTML for formatting

    // Convert *bold* text to <b>bold</b>
    text = text.replace(/\\(.?)\\*/g, '<b>$1</b>');

    // Convert #### text to green span
    text = text.replace(/###\s*(.*?)(\n|$)/g, '<span class="green-text">$1</span>$2');

    // Letter by letter display
    const interval = setInterval(() => {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = text.slice(0, index + 1);
        messageElem.innerHTML = tempDiv.innerHTML;

        index++;
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        if (index >= text.length) {
            clearInterval(interval);
        }
    }, 50); // 50ms per character
}



// Send message function
function sendMessage() {
    const text = messageInput.value.trim();
    if (text === '') return;

    // Add user's message
    addMessage(text, 'user');
    messageInput.value = '';

    // Show bot typing
    const typingIndicator = addTypingIndicator();

    // Fetch response from backend
    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator(typingIndicator);
            const botMessage = addMessage('', 'bot');
            displayMessageLetterByLetter(botMessage, data.reply);
        })
        .catch(error => {
            removeTypingIndicator(typingIndicator);
            addMessage("Sorry, something went wrong.", 'bot');
            console.error('Error:', error);
        });
}



// Send message on Enter key press
messageInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});