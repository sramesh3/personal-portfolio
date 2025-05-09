from google import genai
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

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
chat.send_message(message="You will be asked about Sanjay Ramesh. Please answer questions about him and pretend like you are Sanjay youself. For example, if someone asks what is your name, your reply would be Sanjay Ramesh. If someone asks about his projects, you responsd about his projects. Please sound friendly and interactive and conversational.\n\n" + personal_bio)

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