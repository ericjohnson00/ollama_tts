from gtts import gTTS
import pygame
import ollama
import time

# Function to generate a response using Ollama
def generate_response(prompt):
    """
    Sends the prompt to Ollama and returns the generated response.
    """
    response = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)
    return response["response"]

# Function to convert text to speech and play it
def text_to_speech(text):
    """
    Converts the given text to speech and plays it.
    """
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Generate and save the audio file
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")
    
    # Load and play the audio
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # Clean up
    pygame.mixer.quit()

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
        print(f"DeepSeek: {response}")

        # Convert response to speech and play it
        text_to_speech(response)

if __name__ == "__main__":
    main()