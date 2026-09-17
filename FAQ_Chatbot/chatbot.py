import tkinter as tk
from tkinter import scrolledtext
import re
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# NLP SETUP
# =========================================================

stemmer = PorterStemmer()


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    words = text.split()

    words = [
        stemmer.stem(word)
        for word in words
    ]

    return " ".join(words)


# =========================================================
# FAQ DATA
# =========================================================

faqs = [

    {
        "question": "What is Artificial Intelligence?",
        "answer":
        "Artificial Intelligence is a field of computer science "
        "that enables machines to perform tasks that normally "
        "require human intelligence."
    },

    {
        "question": "What is Machine Learning?",
        "answer":
        "Machine Learning is a branch of AI that allows computers "
        "to learn patterns from data and make predictions or decisions."
    },

    {
        "question": "What is Python?",
        "answer":
        "Python is a popular programming language widely used in "
        "Artificial Intelligence, Machine Learning, data science, "
        "and software development."
    },

    {
        "question": "What is NLP?",
        "answer":
        "NLP stands for Natural Language Processing. It helps computers "
        "understand, process, and respond to human language."
    },

    {
        "question": "What is Deep Learning?",
        "answer":
        "Deep Learning is a part of Machine Learning that uses "
        "neural networks with multiple layers to learn complex "
        "patterns from data."
    },

    {
        "question": "What is a Chatbot?",
        "answer":
        "A chatbot is a software application that communicates "
        "with users through text or voice and provides automated responses."
    },

    {
        "question": "What is Supervised Learning?",
        "answer":
        "Supervised learning trains a model using labeled data, "
        "where the correct output is already known."
    },

    {
        "question": "What is Unsupervised Learning?",
        "answer":
        "Unsupervised learning finds patterns or groups in data "
        "without using predefined labels."
    },

    {
        "question": "What is a Neural Network?",
        "answer":
        "A neural network is a machine learning model inspired by "
        "the human brain and consists of interconnected layers "
        "of artificial neurons."
    },

    {
        "question": "What is Computer Vision?",
        "answer":
        "Computer vision is an AI field that enables computers "
        "to understand and analyze images and videos."
    }
]


# =========================================================
# FAQ QUESTIONS
# =========================================================

faq_questions = [
    faq["question"]
    for faq in faqs
]


# =========================================================
# PROCESSED FAQ QUESTIONS
# =========================================================

processed_questions = [
    preprocess(question)
    for question in faq_questions
]


# =========================================================
# TF-IDF MODEL
# =========================================================
# Stop words remove common words such as:
# what, is, a, the
# This helps the model focus on important topic words.

vectorizer = TfidfVectorizer(
    stop_words="english"
)


faq_vectors = vectorizer.fit_transform(
    processed_questions
)


# =========================================================
# RESPONSE SYSTEM
# =========================================================

def get_response(user_question):

    if not user_question.strip():
        return "Please enter a question."

    question = user_question.lower()


    # -----------------------------------------------------
    # SPELLING CORRECTIONS
    # -----------------------------------------------------

    corrections = {

        "pyhton": "python",
        "pythn": "python",
        "pyton": "python",

        "machne learning": "machine learning",
        "machin learning": "machine learning",
        "machin learnin": "machine learning",

        "artifical intelligence": "artificial intelligence",
        "artificial inteligence": "artificial intelligence",
        "artifical inteligence": "artificial intelligence",

        "chatbt": "chatbot",
        "chat bot": "chatbot",

        "neural netwrok": "neural network",
        "neural netwrk": "neural network",

        "deep lerning": "deep learning",

        "computr vision": "computer vision"
    }


    for wrong, correct in corrections.items():

        question = question.replace(
            wrong,
            correct
        )


    # -----------------------------------------------------
    # PREPROCESS USER QUESTION
    # -----------------------------------------------------

    processed_user_question = preprocess(
        question
    )


    # -----------------------------------------------------
    # CONVERT USER QUESTION INTO TF-IDF VECTOR
    # -----------------------------------------------------

    user_vector = vectorizer.transform(
        [processed_user_question]
    )


    # -----------------------------------------------------
    # CALCULATE COSINE SIMILARITY
    # -----------------------------------------------------

    similarity_scores = cosine_similarity(
        user_vector,
        faq_vectors
    )[0]


    # -----------------------------------------------------
    # FIND MOST SIMILAR FAQ
    # -----------------------------------------------------

    best_match_index = similarity_scores.argmax()

    best_score = similarity_scores[
        best_match_index
    ]


    # -----------------------------------------------------
    # SIMILARITY THRESHOLD
    # -----------------------------------------------------
    # If similarity is too low, the question is unrelated.

    if best_score < 0.20:

        return (
            "Sorry, I couldn't find a suitable answer.\n\n"
            "Try asking about AI, Machine Learning, Python, NLP, "
            "Deep Learning, Chatbots, Supervised Learning, "
            "Unsupervised Learning, Neural Networks or Computer Vision."
        )


    # -----------------------------------------------------
    # RETURN BEST MATCHING ANSWER
    # -----------------------------------------------------

    return faqs[
        best_match_index
    ]["answer"]


# =========================================================
# SEND MESSAGE
# =========================================================

def send_message(event=None):

    user_question = entry.get().strip()


    if not user_question:
        return


    chat_area.config(
        state=tk.NORMAL
    )


    # User message
    chat_area.insert(
        tk.END,
        "YOU\n",
        "user_label"
    )


    chat_area.insert(
        tk.END,
        user_question + "\n\n",
        "user_message"
    )


    # AI response
    response = get_response(
        user_question
    )


    chat_area.insert(
        tk.END,
        "AI ASSISTANT\n",
        "bot_label"
    )


    chat_area.insert(
        tk.END,
        response + "\n\n",
        "bot_message"
    )


    chat_area.config(
        state=tk.DISABLED
    )


    entry.delete(
        0,
        tk.END
    )


    chat_area.see(
        tk.END
    )


# =========================================================
# CLEAR CHAT
# =========================================================

def clear_chat():

    chat_area.config(
        state=tk.NORMAL
    )


    chat_area.delete(
        "1.0",
        tk.END
    )


    chat_area.insert(
        tk.END,
        "AI ASSISTANT\n",
        "bot_label"
    )


    chat_area.insert(
        tk.END,
        "Hello! 👋\n\n"
        "Welcome to the AI FAQ Assistant.\n"
        "Ask me anything about Artificial Intelligence.\n\n",
        "bot_message"
    )


    chat_area.config(
        state=tk.DISABLED
    )


    entry.focus()


# =========================================================
# QUICK QUESTION
# =========================================================

def quick_question(question):

    entry.delete(
        0,
        tk.END
    )


    entry.insert(
        0,
        question
    )


    send_message()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()


root.title(
    "AI FAQ Assistant"
)


root.geometry(
    "920x560"
)


root.minsize(
    760,
    520
)


# =========================================================
# COLORS
# =========================================================

BLACK = "#111111"

DARK_BLACK = "#181818"

MAROON = "#800000"

DARK_MAROON = "#5A0000"

LIGHT_MAROON = "#A52A2A"

WHITE = "#FFFFFF"

LIGHT_TEXT = "#EAEAEA"

GRAY = "#BDBDBD"

INPUT_BG = "#242424"


root.configure(
    bg=BLACK
)


# =========================================================
# ROOT GRID
# =========================================================

root.grid_rowconfigure(
    1,
    weight=1
)

root.grid_columnconfigure(
    0,
    weight=1
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=BLACK,
    height=75
)


header.grid(
    row=0,
    column=0,
    sticky="ew"
)


header.grid_propagate(
    False
)


title_label = tk.Label(
    header,
    text="AI FAQ ASSISTANT",
    font=("Segoe UI", 20, "bold"),
    bg=BLACK,
    fg=WHITE
)


title_label.pack(
    pady=(10, 0)
)


subtitle_label = tk.Label(
    header,
    text="Intelligent Question Answering System",
    font=("Segoe UI", 9),
    bg=BLACK,
    fg=GRAY
)


subtitle_label.pack(
    pady=(2, 0)
)


# =========================================================
# MAIN CONTENT
# =========================================================

main_frame = tk.Frame(
    root,
    bg=BLACK
)


main_frame.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=15,
    pady=(0, 8)
)


main_frame.grid_rowconfigure(
    0,
    weight=1
)


main_frame.grid_columnconfigure(
    0,
    weight=1
)


# =========================================================
# CHAT CARD
# =========================================================

chat_card = tk.Frame(
    main_frame,
    bg=DARK_BLACK,
    bd=1,
    relief=tk.SOLID
)


chat_card.grid(
    row=0,
    column=0,
    sticky="nsew"
)


chat_card.grid_rowconfigure(
    0,
    weight=1
)


chat_card.grid_columnconfigure(
    0,
    weight=1
)


# =========================================================
# CHAT AREA
# =========================================================

chat_area = scrolledtext.ScrolledText(
    chat_card,
    wrap=tk.WORD,
    font=("Segoe UI", 10),
    bg=DARK_BLACK,
    fg=LIGHT_TEXT,
    insertbackground=WHITE,
    selectbackground=MAROON,
    selectforeground=WHITE,
    bd=0,
    padx=15,
    pady=12
)


chat_area.grid(
    row=0,
    column=0,
    sticky="nsew"
)


# =========================================================
# CHAT TEXT STYLES
# =========================================================

chat_area.tag_config(
    "user_label",
    foreground=LIGHT_MAROON,
    font=("Segoe UI", 9, "bold")
)


chat_area.tag_config(
    "user_message",
    foreground=WHITE,
    font=("Segoe UI", 10)
)


chat_area.tag_config(
    "bot_label",
    foreground="#D66A6A",
    font=("Segoe UI", 9, "bold")
)


chat_area.tag_config(
    "bot_message",
    foreground=LIGHT_TEXT,
    font=("Segoe UI", 10)
)


# =========================================================
# WELCOME MESSAGE
# =========================================================

chat_area.insert(
    tk.END,
    "AI ASSISTANT\n",
    "bot_label"
)


chat_area.insert(
    tk.END,
    "Hello! 👋\n\n"
    "Welcome to the AI FAQ Assistant.\n"
    "Ask me anything about Artificial Intelligence.\n\n",
    "bot_message"
)


chat_area.config(
    state=tk.DISABLED
)


# =========================================================
# BOTTOM PANEL
# =========================================================

bottom_frame = tk.Frame(
    root,
    bg=BLACK
)


bottom_frame.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=15,
    pady=(0, 10)
)


bottom_frame.grid_columnconfigure(
    0,
    weight=1
)


# =========================================================
# QUICK QUESTIONS TITLE
# =========================================================

quick_title = tk.Label(
    bottom_frame,
    text="QUICK QUESTIONS",
    font=("Segoe UI", 8, "bold"),
    bg=BLACK,
    fg=GRAY
)


quick_title.grid(
    row=0,
    column=0,
    sticky="w",
    pady=(0, 3)
)


# =========================================================
# QUICK QUESTIONS CONTAINER
# =========================================================

quick_frame = tk.Frame(
    bottom_frame,
    bg=BLACK
)


quick_frame.grid(
    row=1,
    column=0,
    sticky="ew",
    pady=(0, 7)
)


# Make 5 equal columns

for i in range(5):

    quick_frame.grid_columnconfigure(
        i,
        weight=1
    )


# =========================================================
# 10 QUICK QUESTIONS
# =========================================================

quick_questions = [

    "What is AI?",
    "What is Machine Learning?",
    "What is Python?",
    "What is NLP?",
    "What is Deep Learning?",

    "What is a Chatbot?",
    "What is Supervised Learning?",
    "What is Unsupervised Learning?",
    "What is a Neural Network?",
    "What is Computer Vision?"
]


# =========================================================
# CREATE QUICK BUTTONS
# =========================================================

for index, question in enumerate(
    quick_questions
):

    row = index // 5

    column = index % 5


    button = tk.Button(
        quick_frame,
        text=question,
        font=("Segoe UI", 7, "bold"),
        bg=DARK_MAROON,
        fg=WHITE,
        activebackground=MAROON,
        activeforeground=WHITE,
        relief=tk.FLAT,
        bd=0,
        cursor="hand2",
        padx=4,
        pady=4,
        wraplength=150,
        command=lambda q=question: quick_question(q)
    )


    button.grid(
        row=row,
        column=column,
        sticky="ew",
        padx=2,
        pady=2
    )


# =========================================================
# INPUT FRAME
# =========================================================

input_frame = tk.Frame(
    bottom_frame,
    bg=BLACK
)


input_frame.grid(
    row=2,
    column=0,
    sticky="ew"
)


input_frame.grid_columnconfigure(
    0,
    weight=1
)


# =========================================================
# INPUT BOX
# =========================================================

entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 10),
    bg=INPUT_BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief=tk.SOLID,
    bd=1
)


entry.grid(
    row=0,
    column=0,
    sticky="ew",
    ipady=7,
    padx=(0, 7)
)


# =========================================================
# SEND BUTTON
# =========================================================

send_button = tk.Button(
    input_frame,
    text="SEND",
    font=("Segoe UI", 9, "bold"),
    bg=MAROON,
    fg=WHITE,
    activebackground=DARK_MAROON,
    activeforeground=WHITE,
    relief=tk.FLAT,
    bd=0,
    width=9,
    cursor="hand2",
    command=send_message
)


send_button.grid(
    row=0,
    column=1,
    padx=(0, 5)
)


# =========================================================
# CLEAR BUTTON
# =========================================================

clear_button = tk.Button(
    input_frame,
    text="CLEAR",
    font=("Segoe UI", 9, "bold"),
    bg="#333333",
    fg=WHITE,
    activebackground="#444444",
    activeforeground=WHITE,
    relief=tk.FLAT,
    bd=0,
    width=9,
    cursor="hand2",
    command=clear_chat
)


clear_button.grid(
    row=0,
    column=2
)


# =========================================================
# ENTER KEY
# =========================================================

entry.bind(
    "<Return>",
    send_message
)


# =========================================================
# START APPLICATION
# =========================================================

entry.focus()

root.mainloop()