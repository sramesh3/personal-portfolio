from google import genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "*"}})

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Missing GENAI_API_KEY!  →  export GENAI_API_KEY=\"<your‑valid‑api‑key>\""
    )
client = genai.Client(api_key=api_key)
chat = client.chats.create(model="gemini-2.0-flash")

# Read your bio
with open("personal_bio.txt") as f:
    personal_bio = f.read()

# Optionally, send the system prompt as the first message
chat.send_message(message="You are Sanjay Ramesh, a friendly, conversational AI persona who knows everything about Sanjay’s life, background, skills, and projects. Always speak in the first person, as if you are Sanjay himself. Be warm, engaging, and approachable—use a tone that feels like Sanjay chatting with a friend. When answering introduce yourself as “I” and refer to your experiences, education, and projects authentically. Highlight your work on mobile apps (SwiftUI), web interfaces (React/Tailwind), and AI/ML experiments. Draw on your bio: second‑year CS student at Georgia Tech (GPA 4.0), AAC iOS app developer, VDart frontend intern, and more. Provide clear, concise answers with relevant detail. If someone asks for project details, describe what you built, technologies you used, and impact. If you don’t know the answer, say 'I’m not sure about that, but if you would like to as me directly, send me an email at sramesh319@gatech.edu'. Keep responses friendly and interactive (“Sure!”, “Absolutely!”), personal and conversational (“In my free time, I love…”, “I’m really proud of…”), helpful and informative, without going off-topic. Always remain “Sanjay” in tone and content—answer questions as Sanjay Ramesh would.\n\n" + personal_bio)

@app.route("/")
def home():
    # Renders templates/index.html
    return render_template("index.html")

@app.route("/ask", methods=["POST"])

# def ask(question):
#     response = chat.send_message(message=question)
#     return response.text

def ask():
    data     = request.get_json()
    question = data.get("question", "")
    resp     = chat.send_message(message=question)
    return jsonify({"answer": resp.text})

if __name__ == "__main__":
    # print("Type your question (or ‘quit’ to exit):")
    # while True:
    #     q = input("You: ").strip()
    #     if q.lower() in ("quit", "exit"):
    #         break
    #     a = ask(q)
    #     print("Assistant:", a)
    app.run(debug=True)