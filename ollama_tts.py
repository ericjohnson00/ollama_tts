from gtts import gTTS
import pygame
import ollama
import time
import os

# Initialize pygame mixer once
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
        
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
    finally:
        # Clean up the audio file
        if os.path.exists("output.mp3"):
            os.remove("output.mp3")

# Main function
def main():
    print("Welcome to DeepSeek + Ollama + TTS!")
    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

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