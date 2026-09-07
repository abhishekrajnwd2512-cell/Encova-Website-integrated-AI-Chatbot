const aiButton = document.querySelector(".ai-button");
const chatbot = document.getElementById("chatbot");
const closeChat = document.getElementById("close-chat");

const chatInput = document.getElementById("chat-input");
const sendMessage = document.getElementById("send-message");
const chatbotBody = document.querySelector(".chatbot-body");

const newConversation =
    document.getElementById("new-conversation");


// ==========================
// CONVERSATION STATE
// ==========================

let conversationReset = false;


// ==========================
// INITIAL BOT MESSAGE
// ==========================

const initialMessage = `
    <div class="bot-message">

        <div class="message-icon">
            ✦
        </div>

        <div class="message-content">

            <p>Hello! 👋</p>

            <p>
                I'm Encova AI. How can I help you today?
            </p>

        </div>

    </div>
`;


// ==========================
// SCROLL CHAT TO BOTTOM
// ==========================

function scrollToBottom() {

    chatbotBody.scrollTo({
        top: chatbotBody.scrollHeight,
        behavior: "smooth"
    });

}


// ==========================
// SHOW TYPING INDICATOR
// ==========================

function showTypingIndicator() {

    const typingIndicator =
        document.createElement("div");

    typingIndicator.classList.add(
        "ai-message",
        "typing-indicator"
    );

    typingIndicator.innerHTML = `
        <div class="message-icon">
            ✦
        </div>

        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    chatbotBody.appendChild(typingIndicator);

    scrollToBottom();

    return typingIndicator;
}


// ==========================
// RESET BACKEND CONVERSATION
// ==========================

async function resetConversation() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/new-conversation",
            {
                method: "POST"
            }
        );

        if (!response.ok) {

            throw new Error(
                "Failed to reset conversation"
            );

        }

        console.log(
            "Conversation automatically reset."
        );

    } catch (error) {

        console.error(
            "Error resetting conversation:",
            error
        );

    }
}


// ==========================
// OPEN CHATBOT
// ==========================

aiButton.addEventListener("click", () => {

    conversationReset = false;

    chatbot.classList.add("active");

    chatInput.focus();

});


// ==========================
// CLOSE CHATBOT
// ==========================

closeChat.addEventListener("click", async () => {

    // Mark conversation as reset
    conversationReset = true;

    // Close chatbot
    chatbot.classList.remove("active");

    // Clear input
    chatInput.value = "";

    // Reset backend
    await resetConversation();

    // Reset visible chat
    chatbotBody.innerHTML = initialMessage;

});


// ==========================
// SEND MESSAGE
// ==========================

sendMessage.addEventListener("click", async () => {

    const message = chatInput.value.trim();

    // Don't send empty messages
    if (message === "") {

        return;

    }

    // A new message means this is an active conversation
    conversationReset = false;


    // ==========================
    // SHOW USER MESSAGE
    // ==========================

    const userMessage =
        document.createElement("div");

    userMessage.classList.add("user-message");


    const userMessageContent =
        document.createElement("div");

    userMessageContent.classList.add(
        "user-message-content"
    );


    const userText =
        document.createElement("p");

    userText.textContent = message;


    userMessageContent.appendChild(userText);

    userMessage.appendChild(userMessageContent);

    chatbotBody.appendChild(userMessage);


    // Scroll to newest message
    scrollToBottom();


    // Clear input
    chatInput.value = "";


    // Show typing indicator
    const typingIndicator =
        showTypingIndicator();


    // ==========================
    // SEND MESSAGE TO FLASK
    // ==========================

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to get AI response"
            );

        }


        const data =
            await response.json();


        // ==========================
        // CHECK IF CHAT WAS RESET
        // ==========================

        if (conversationReset) {

            typingIndicator.remove();

            return;

        }


        // Remove typing indicator
        typingIndicator.remove();


        // ==========================
        // SHOW AI RESPONSE
        // ==========================

        const aiMessage =
            document.createElement("div");

        aiMessage.classList.add("ai-message");


        const aiMessageContent =
            document.createElement("div");

        aiMessageContent.classList.add(
            "ai-message-content"
        );


        const aiText =
            document.createElement("p");

        aiText.textContent = data.response;


        aiMessageContent.appendChild(aiText);

        aiMessage.appendChild(aiMessageContent);

        chatbotBody.appendChild(aiMessage);


        // Scroll to newest AI message
        scrollToBottom();


    } catch (error) {

        // Don't show an error if the conversation
        // was already closed/reset
        if (conversationReset) {

            return;

        }


        if (
            typingIndicator &&
            typingIndicator.parentNode
        ) {

            typingIndicator.remove();

        }


        console.error(
            "Chatbot Error:",
            error
        );


        // ==========================
        // ERROR MESSAGE
        // ==========================

        const aiMessage =
            document.createElement("div");

        aiMessage.classList.add("ai-message");


        const aiMessageContent =
            document.createElement("div");

        aiMessageContent.classList.add(
            "ai-message-content"
        );


        const aiText =
            document.createElement("p");

        aiText.textContent =
            "Sorry, I couldn't connect to the AI right now.";


        aiMessageContent.appendChild(aiText);

        aiMessage.appendChild(aiMessageContent);

        chatbotBody.appendChild(aiMessage);


        scrollToBottom();

    }

});


// ==========================
// SEND MESSAGE WITH ENTER
// ==========================

chatInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage.click();

    }

});


// ==========================
// NEW CONVERSATION
// ==========================

newConversation.addEventListener("click", async () => {

    // Mark current conversation as reset
    conversationReset = true;


    // Reset backend
    await resetConversation();


    // Clear chat window
    chatbotBody.innerHTML = initialMessage;


    // Clear input
    chatInput.value = "";


    // Scroll to top
    chatbotBody.scrollTo({
        top: 0,
        behavior: "smooth"
    });


    // Start fresh conversation
    conversationReset = false;


    // Focus input
    chatInput.focus();


    console.log(
        "New conversation started!"
    );

});