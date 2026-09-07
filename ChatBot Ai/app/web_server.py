from flask import Flask, request, jsonify
from flask_cors import CORS

from app.gemini_client import create_chat, generate_response

import json
import re


app = Flask(__name__)

# Allow the website to communicate with Flask
CORS(app)


# ==========================
# LOAD ENCOVA RESPONSES
# ==========================

with open("encova_responses.json", "r", encoding="utf-8") as file:

    encova_responses = json.load(file)


# ==========================
# SYSTEM PROMPT
# ==========================

system_prompt = "You are a helpful assistant."


# ==========================
# CREATE ONE CHAT SESSION
# ==========================

chat = create_chat(system_prompt)


# ==========================
# USER NAME
# ==========================

user_name = None


# ==========================
# HOME
# ==========================

@app.route("/")
def home():

    return "Chatbot backend is running!"


# ==========================
# FIND USER NAME
# ==========================

def find_name(message):

    global user_name

    # My name is Shahaan
    match = re.search(
        r"\bmy name is\s+([a-zA-Z]+)",
        message,
        re.IGNORECASE
    )

    if match:

        user_name = match.group(1).strip().capitalize()

        return (
            f"Nice to meet you, {user_name}! 👋 "
            f"I'll remember your name during this conversation."
        )


    # I am Shahaan / I'm Shahaan
    match = re.search(
        r"\b(?:i am|i'm)\s+([a-zA-Z]+)",
        message,
        re.IGNORECASE
    )

    if match:

        user_name = match.group(1).strip().capitalize()

        return (
            f"Nice to meet you, {user_name}! 👋 "
            f"I'll remember your name during this conversation."
        )


    # Call me Shahaan
    match = re.search(
        r"\bcall me\s+([a-zA-Z]+)",
        message,
        re.IGNORECASE
    )

    if match:

        user_name = match.group(1).strip().capitalize()

        return (
            f"Sure, {user_name}! 👋 "
            f"I'll remember your name during this conversation."
        )


    # What is my name?
    name_question_phrases = [
        "what is my name",
        "what's my name",
        "do you know my name",
        "remember my name",
        "what do you call me"
    ]

    if any(
        phrase in message.lower()
        for phrase in name_question_phrases
    ):

        if user_name:

            return f"Your name is {user_name}. 😊"

        return "You haven't told me your name yet."


    return None

# FIND SAVED RESPONSES

def find_saved_response(message):

    # ==========================
    # CLEAN MESSAGE
    # ==========================

    message = message.lower().strip()

    # Remove punctuation
    message = re.sub(r"[^\w\s]", "", message)

    # Create word list
    words = message.split()


    # ==========================
    # GREETINGS
    # ==========================

    greeting_words = [
        "hi",
        "hello",
        "hey",
        "hiya",
        "greetings"
    ]

    # If the message is mainly a greeting
    if any(word in words for word in greeting_words):

        return encova_responses["greetings"]["hi"]


    # ==========================
    # SERVICES
    # ==========================

    service_words = [
        "service",
        "services",
        "offer",
        "offers",
        "provide",
        "provides",
        "providing",
        "do",
        "does",
        "help",
        "helps"
    ]

    service_context_words = [
        "encova",
        "company",
        "you",
        "your"
    ]

    has_service_word = any(
        word in words
        for word in service_words
    )

    has_service_context = any(
        word in words
        for word in service_context_words
    )

    if has_service_word and has_service_context:

        return encova_responses["services"][
            "what services does encova provide"
        ]


    # ==========================
    # COMPANY INFORMATION
    # ==========================

    company_phrases = [
        "what is encova",
        "what is encova solutions",
        "tell me about encova",
        "tell me about encova solutions",
        "about encova",
        "about your company",
        "what does encova do",
        "what does encova solutions do",
        "what can encova do",
        "what can encova solutions do",
        "what kind of company is encova",
        "what type of company is encova",
        "tell me about the company"
    ]

    if any(
        phrase in message
        for phrase in company_phrases
    ):

        return encova_responses["company"][
            "what is encova"
        ]


    # ==========================
    # OFFICE DAYS
    # ==========================

    office_day_words = [
        "days",
        "weekdays",
        "weekday",
        "working",
        "operate",
        "operates",
        "operation"
    ]

    office_context_words = [
        "office",
        "open",
        "work",
        "working",
        "operate",
        "operates",
        "encova",
        "company",
        "you",
        "your"
    ]

    has_day_word = any(
        word in words
        for word in office_day_words
    )

    has_office_context = any(
        word in words
        for word in office_context_words
    )

    if has_day_word and has_office_context:

        return encova_responses["office"][
            "what days are you open"
        ]


    # ==========================
    # OFFICE TIMINGS
    # ==========================

    office_time_words = [
        "timing",
        "timings",
        "hours",
        "hour",
        "time",
        "open",
        "close",
        "opens",
        "closes"
    ]

    office_time_context_words = [
        "office",
        "you",
        "your",
        "we",
        "working",
        "encova"
    ]

    has_time_word = any(
        word in words
        for word in office_time_words
    )

    has_time_context = any(
        word in words
        for word in office_time_context_words
    )

    if has_time_word and has_time_context:

        return encova_responses["office"][
            "what are your office timings"
        ]


    # ==========================
    # LOCATION
    # ==========================

    location_words = [
        "where",
        "location",
        "located",
        "address",
        "based"
    ]

    location_context_words = [
        "encova",
        "office",
        "company",
        "you",
        "your"
    ]

    has_location_word = any(
        word in words
        for word in location_words
    )

    has_location_context = any(
        word in words
        for word in location_context_words
    )

    if has_location_word and has_location_context:

        return encova_responses["location"][
            "where is encova located"
        ]


    # ==========================
    # CEO
    # ==========================

    ceo_words = [
        "ceo",
        "chief",
        "executive"
    ]

    if (
        "ceo" in words
        or "chief executive" in message
        or "chief executive officer" in message
    ):

        return encova_responses["people"][
            "who is the ceo"
        ]

    # ==========================
    # LEADERSHIP / PEOPLE
    # ==========================

    leadership_phrases = [
        "who runs encova",
        "who runs encova solutions",
        "who is in charge of encova",
        "who is in charge of encova solutions",
        "who leads encova",
        "who leads encova solutions",
        "who manages encova",
        "who manages encova solutions"
    ]

    if any(
        phrase in message
        for phrase in leadership_phrases
    ):

        return encova_responses["people"][
            "who is the ceo"
        ]

    # ==========================
    # CO-FOUNDER
    # ==========================

    cofounder_phrases = [
        "co founder",
        "cofounder",
        "founder",
        "founded"
    ]

    if any(
        phrase in message
        for phrase in cofounder_phrases
    ):

        return encova_responses["people"][
            "who is the co founder"
        ]


    # ==========================
    # NO MATCH
    # ==========================

    return None

# ==========================
# SEND MESSAGE
# ==========================

@app.route("/chat", methods=["POST"])
def chat_endpoint():

    global chat

    data = request.get_json()

    message = data.get("message")


    if not message:

        return jsonify({
            "error": "Message is required"
        }), 400


    # ==========================
    # CHECK NAME FIRST
    # ==========================

    name_response = find_name(message)

    if name_response:

        return jsonify({
            "response": name_response,
            "source": "memory"
        })


    # ==========================
    # CHECK SAVED ENCOVA RESPONSES
    # ==========================

    saved_response = find_saved_response(message)


    if saved_response:

        return jsonify({
            "response": saved_response,
            "source": "saved"
        })


    # ==========================
    # IF NOT FOUND → GEMINI
    # ==========================

    response = generate_response(
        chat,
        message
    )


    return jsonify({
        "response": response,
        "source": "gemini"
    })


# ==========================
# NEW CONVERSATION
# ==========================

@app.route("/new-conversation", methods=["POST"])
def new_conversation():

    global chat
    global user_name


    # Create a completely fresh Gemini chat
    chat = create_chat(system_prompt)


    # Forget user's name
    user_name = None


    return jsonify({
        "message": "Conversation has been reset"
    })


# ==========================
# RUN SERVER
# ==========================

if __name__ == "__main__":

    app.run(debug=True)