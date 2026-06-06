from flask import Flask, request, jsonify
from pipeline.router import router
from voice.text_to_speech import humanize_text, text_to_speech_piper
from voice.speech_to_text import record_until_silence, speech_to_text

app = Flask(__name__)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")

    if not query:
        print("No query provided in the request")
        return jsonify({"error": "No query provided"}), 400

    if query.lower() == "record query":
        audio_file = record_until_silence()
        query = speech_to_text(file=audio_file)

    response = router(query)

    humanized_response = humanize_text(response)

    text_to_speech_piper(humanized_response)

    return jsonify({
        "query": query,
        "response": response,
    })

if __name__ == "__main__":
    app.run(debug=True)