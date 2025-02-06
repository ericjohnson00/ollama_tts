import sys
import os
import time
import ollama
import pygame
import speech_recognition as sr
from gtts import gTTS
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel

# Initialize pygame for audio playback
pygame.mixer.init()

class OllamaChatApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up UI
        self.setWindowTitle("Ollama Voice Chat")
        self.setGeometry(100, 100, 500, 400)

        self.label = QLabel("Ask something:", self)
        self.text_input = QTextEdit(self)
        self.submit_button = QPushButton("Submit", self)
        self.voice_button = QPushButton("🎤 Speak", self)
        self.response_box = QTextEdit(self)
        self.response_box.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.voice_button)
        layout.addWidget(self.response_box)
        self.setLayout(layout)

        # Connect buttons to functions
        self.submit_button.clicked.connect(self.handle_text_input)
        self.voice_button.clicked.connect(self.handle_voice_input)

    def handle_text_input(self):
        """Handles text input and generates a response."""
        user_input = self.text_input.toPlainText().strip()
        if user_input:
            self.generate_response(user_input)

    def handle_voice_input(self):
        """Handles voice input, converts it to text, and generates a response."""
        user_input = self.recognize_speech()
        if user_input:
            self.text_input.setPlainText(user_input)  # Show recognized text
            self.generate_response(user_input)

    def generate_response(self, prompt):
        """Sends the prompt to Ollama and handles the response."""
        self.response_box.setText("Generating response...")
        try:
            response = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)["response"]
            self.response_box.setText(response)
            self.text_to_speech(response)  # Convert response to speech
        except Exception as e:
            self.response_box.setText(f"Error: {e}")

    def recognize_speech(self):
        """Captures and transcribes voice input."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.response_box.setText("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            self.response_box.setText("❌ Could not understand audio.")
            return None
        except sr.RequestError:
            self.response_box.setText("⚠️ Check your internet connection.")
            return None

    def text_to_speech(self, text):
        """Converts text to speech and plays it."""
        try:
            tts = gTTS(text=text, lang="en")
            tts.save("output.mp3")
            
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            os.remove("output.mp3")  # Delete the file after playing
        except Exception as e:
            self.response_box.setText(f"TTS Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OllamaChatApp()
    window.show()
    sys.exit(app.exec())
