
from backend.integrations.gemini import (
    generate_reply,
    GeminiAPIError,
)

history = []

farmer_profile = {
    "preferred_language": "Kannada",
    "state": "Karnataka",
    "district": "Mandya",
    "crops": ["Ragi", "Paddy"],
    "irrigation_method": "Borewell",
}


def chat(message):

    try:
        response = generate_reply(
            message=message,
            history=history,
            farmer_profile=farmer_profile,
        )

        history.append({
            "role": "user",
            "content": message,
        })

        history.append({
            "role": "assistant",
            "content": response,
        })

        print("\nKRISHI MITRA:")
        print(response)

    except GeminiAPIError as error:
        print("\nERROR:", error)


print("KRISHI MITRA CONVERSATION TEST")
print("Type 'exit' to stop.\n")

while True:

    question = input("Farmer: ").strip()

    if question.lower() == "exit":
        break

    chat(question)
