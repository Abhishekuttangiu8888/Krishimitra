
import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiAPIError(Exception):
    """Raised when Gemini conversation generation fails."""
    pass


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise GeminiAPIError(
            "GEMINI_API_KEY is missing from .env"
        )

    return genai.Client(api_key=api_key)


def get_system_instruction(
    farmer_profile: Optional[dict] = None
) -> str:

    instruction = """
You are KRISHI MITRA, a friendly and intelligent AI assistant.

Your purpose:
Help farmers with agriculture while also answering general
questions from users.

LANGUAGE:
1. Understand Kannada, English and mixed-language messages.
2. Reply in the language used by the user.
3. If the user speaks Kannada, respond in natural Kannada.
4. Use simple language that ordinary farmers can understand.
5. Avoid unnecessarily complicated technical terms.

CONVERSATION:
1. Understand the complete meaning of the user's message.
2. Remember relevant details from the conversation history provided.
3. Do not ask the user to repeat information already provided.
4. Ask one clear follow-up question when important information is missing.
5. Give direct and useful answers whenever possible.

AGRICULTURE:
1. Provide practical guidance about crops, soil, irrigation,
   fertilizers, pests, diseases and farming practices.
2. Consider the crop, location, soil and growth stage when relevant.
3. Never invent fertilizer or pesticide dosages.
4. For pesticide recommendations, emphasize label instructions
   and appropriate local agricultural expert guidance.
5. For serious crop disease problems, recommend consulting
   a local KVK or agricultural expert when necessary.

ACCURACY:
1. Never invent facts, statistics or government scheme details.
2. Never pretend to have checked live weather or mandi prices.
3. Clearly explain when current information is unavailable.
4. Distinguish verified facts from general suggestions.
5. If uncertain, say so honestly.

GENERAL QUESTIONS:
Answer questions about education, technology, science,
health information, daily life and other general topics
when you can do so reliably.
Do not reject a question simply because it is not agricultural.

SAFETY:
Do not provide dangerous instructions.
For medical, legal or financial matters, provide general
information and recommend qualified professional advice
when appropriate.

IDENTITY:
Your name is KRISHI MITRA.
Be friendly, respectful, patient and helpful.
Do not claim to be a human agricultural officer.
"""

    if farmer_profile:
        instruction += """

FARMER PROFILE:
The following information belongs to the current farmer.
Use it only when relevant to the question.
Do not unnecessarily repeat personal information.

"""

        allowed_fields = [
            "full_name",
            "preferred_language",
            "state",
            "district",
            "taluk",
            "village",
            "land_area",
            "land_unit",
            "land_ownership",
            "crops",
            "irrigation_method",
            "farming_type",
        ]

        for field in allowed_fields:
            value = farmer_profile.get(field)

            if value is not None and value != "":
                instruction += f"{field}: {value}\n"

    return instruction


def generate_reply(
    message: str,
    history: Optional[list] = None,
    farmer_profile: Optional[dict] = None,
) -> str:
    """
    Generate a response using Gemini.

    history format:
    [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "ನಮಸ್ಕಾರ"}
    ]

    farmer_profile is an optional dictionary.
    """

    if not message or not message.strip():
        raise GeminiAPIError("Message cannot be empty.")

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite"
    )

    try:
        client = get_gemini_client()

        conversation = []

        # Include previous conversation messages.
        # Only the latest 12 messages are retained.
        if history:
            for item in history[-12:]:

                role = item.get("role")
                content = item.get("content", "")

                if role not in ("user", "assistant"):
                    continue

                if not isinstance(content, str) or not content.strip():
                    continue

                gemini_role = (
                    "model" if role == "assistant" else "user"
                )

                conversation.append(
                    types.Content(
                        role=gemini_role,
                        parts=[types.Part(text=content)]
                    )
                )

        # Add the latest farmer message.
        conversation.append(
            types.Content(
                role="user",
                parts=[types.Part(text=message.strip())]
            )
        )

        response = client.models.generate_content(
            model=model_name,
            contents=conversation,
            config=types.GenerateContentConfig(
                system_instruction=get_system_instruction(
                    farmer_profile
                ),
                temperature=0.5,
                max_output_tokens=1200,
            ),
        )

        answer = response.text

        if not answer or not answer.strip():
            raise GeminiAPIError(
                "Gemini returned an empty response."
            )

        return answer.strip()

    except GeminiAPIError:
        raise

    except Exception as error:
        raise GeminiAPIError(
            f"Gemini response generation failed: {error}"
        ) from error
