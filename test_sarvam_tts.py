
from backend.integrations.sarvam_tts import speak_text

text = "ನಮಸ್ಕಾರ ರೈತರೇ! ನಾನು ಕೃಷಿ ಮಿತ್ರ. ನಿಮ್ಮ ಕೃಷಿ ಸಮಸ್ಯೆಗಳಿಗೆ ಸಹಾಯ ಮಾಡಲು ನಾನು ಇಲ್ಲಿದ್ದೇನೆ."

try:
    audio = speak_text(text)

    with open("female_kannada_test.wav", "wb") as file:
        file.write(audio)

    print("Female Kannada voice generated successfully!")
    print("Audio saved as female_kannada_test.wav")

except Exception as error:
    print("Error:", error)
