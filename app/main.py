from pipeline.router import router
from voice.speech_to_text import record_until_silence, speech_to_text
from voice.text_to_speech import humanize_text, text_to_speech_piper

def main():
    query = input("Enter your medical query: ")
    if query.lower() in ["exit", "quit"]:
        print("Exiting the assistant. Goodbye!")
        return
    elif query.lower() == "record query":
        text = record_until_silence()
        query = speech_to_text(file=text)
    response = router(query)
    print("Assistant response:", response)
    humanized_response = humanize_text(response)
    text_to_speech_piper(humanized_response)
    return response
main()