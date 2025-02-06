from gtts import gTTS
import pygame
import ollama
import time
import os
import speech_recognition as sr

# Initialize pygame mixer
pygame.mixer.init()

# Function to generate a response using Ollama
def generate_response(prompt):
    """
    Sends the prompt to Ollama and returns the generated response.
    """
    try:
        response = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)
        return response["response"]
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Function to convert text to speech and play it
def text_to_speech(text):
    """
    Converts the given text to speech and plays it.
    """
    try:
        # Generate and save the audio file
        tts = gTTS(text=text, lang="en")
        tts.save("output.mp3")
        
        # Load and play the audio
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        # Stop the mixer and unload the file before deleting
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()  # Unloads the file so it's not in use anymore
        
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
    finally:
        # Clean up the audio file
        if os.path.exists("output.mp3"):
            try:
                os.remove("output.mp3")
            except Exception as e:
                print(f"Error deleting file: {e}")


# Function to capture speech input from the microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)  # Listen for speech

    try:
        text = recognizer.recognize_google(audio)  # Use Google's speech recognition
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("🤷 Couldn't understand the audio, please try again.")
        return None
    except sr.RequestError:
        print("🚫 Couldn't request results, check your internet connection.")
        return None

# Main function
def main():
    print("Welcome to DeepSeek + Ollama + TTS + Speech Recognition!")
    while True:
        # Choose between voice input or text input
        choice = input("Press [T] to type or [V] to use voice (or type 'exit' to quit): ").strip().lower()

        if choice == "exit":
            print("Goodbye!")
            break
        elif choice == "v":
            user_input = recognize_speech()
            if not user_input:
                continue  # Retry if speech wasn't understood
        elif choice == "t":
            user_input = input("You: ")
        else:
            print("Invalid option. Please try again.")
            continue

        # Generate response using Ollama
        print("Generating response...")
        response = generate_response(user_input)
        if response:
            print(f"DeepSeek: {response}")

            # Convert response to speech and play it
            text_to_speech(response)
        else:
            print("Failed to generate a response. Please try again.")

if __name__ == "__main__":
    main()
