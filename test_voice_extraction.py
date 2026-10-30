
from backend.integrations.voice_extraction import (
    extract_name,
    extract_mobile_number
)


print("----- NAME TESTS -----")

name_tests = [
    "Ramesh",
    "My name is Ramesh",
    "My name is Ramesh and I live in Mandya",
    "ನನ್ನ ಹೆಸರು ರಾಮೇಶ್",
    "ನನ್ನ ಹೆಸರು ರಾಮೇಶ್ ನಾನು ಮಂಡ್ಯದಿಂದ ಬಂದಿದ್ದೇನೆ"
]

for text in name_tests:
    print("Input:", text)
    print("Extracted:", extract_name(text))
    print()


print("----- MOBILE TESTS -----")

mobile_tests = [
    "9876543210",
    "nine eight seven six five four three two one zero",
    "ಒಂಬತ್ತು ಎಂಟು ಏಳು ಆರು ಐದು ನಾಲ್ಕು ಮೂರು ಎರಡು ಒಂದು ಸೊನ್ನೆ",
    "ನನ್ನ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ nine eight seven six five four three two one zero"
]

for text in mobile_tests:
    result = extract_mobile_number(text)
    print("Input:", text)
    print("Result:", result)
    print()
