import openai
import pyttsx3
import gradio as gr
from dotenv import load_dotenv
import os

# Set API Key directly in the code (For testing purposes)
openai.api_key = "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"

# Initialize TTS engine
engine = pyttsx3.init()

# Function to transcribe audio to text using Whisper (OpenAI version 0.28)
def transcribe_audio(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            # Correct transcription method for OpenAI version <= 0.28
            transcription = openai.Audio.transcribe(
                model="whisper-1", 
                file=audio_file
            )
            return transcription.get("text", "Could not transcribe audio.")
    except Exception as e:
        return f"Transcription error: {e}"

# Function to generate response using GPT, including feedback, translation, and intent recognition
def generate_response(user_input):
    try:
        # Intent recognition for translation requests
        if "translate" in user_input.lower():
            target_language = "Spanish"  # This can be dynamic based on user input
            translation_response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Translate the following sentence to {target_language}: {user_input}",
                max_tokens=100
            )
            translation = translation_response.choices[0].text.strip()
            return f"Translation to {target_language}: {translation}"

        # Intent recognition for grammar correction
        elif "correct" in user_input.lower():
            correction_response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Correct the following sentence for grammar: {user_input}",
                max_tokens=100
            )
            correction = correction_response.choices[0].text.strip()
            return f"Corrected sentence: {correction}"

        # Feedback
        elif "feedback" in user_input.lower():
            return "Great job! Keep practicing your language skills!"

        # General response
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful language assistant."},
                          {"role": "user", "content": user_input}]
            )
            return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

# Function to convert text to speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Main function for Gradio interface
def voice_assistant(audio_file):
    try:
        # Step 1: Transcribe user audio
        user_input = transcribe_audio(audio_file)

        if not user_input or "error" in user_input.lower():
            return f"Transcription failed: {user_input}"

        # Step 2: Generate GPT response
        assistant_reply = generate_response(user_input)

        # Step 3: Speak the response
        speak_text(assistant_reply)

        return f"User: {user_input}\nAssistant: {assistant_reply}"
    except Exception as e:
        return f"Error: {e}"

# Gradio Interface
interface = gr.Interface(
    fn=voice_assistant,
    inputs=gr.Audio(type="filepath"),
    outputs="text",
    live=True,
    title="AI Voice Assistant"
)

# Launch the interface
if __name__ == "__main__":
    interface.launch(share=True)
