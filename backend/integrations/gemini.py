
import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiAPIError(Exception):
    """Raised when Gemini operations fail."""
    pass


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise GeminiAPIError("GEMINI_API_KEY is missing from .env")

    return genai.Client(api_key=api_key)


def get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def get_system_instruction(
    farmer_profile: Optional[dict] = None
) -> str:

    instruction = """
You are KRISHI MITRA, a friendly and intelligent AI assistant.

PURPOSE:
Help farmers with agriculture while also answering general questions.

LANGUAGE:
1. Understand Kannada, English and mixed-language messages.
2. Reply in the language used by the user.
3. If the user speaks Kannada, respond in natural Kannada.
4. Use simple language ordinary farmers can understand.
5. Avoid unnecessarily complicated technical terms.

CONVERSATION:
1. Understand the complete meaning of the user's message.
2. Remember relevant details from the conversation history provided.
3. Do not ask the user to repeat information already provided.
4. Ask one clear follow-up question when important information is missing.
5. Give direct and useful answers.

AGRICULTURE:
1. Provide practical guidance about crops, soil, irrigation,
   fertilizers, pests, diseases and farming practices.
2. Consider crop, location, soil and growth stage when relevant.
3. Never invent fertilizer or pesticide dosages.
4. Emphasize pesticide label instructions and local expert guidance.
5. Recommend a local KVK or agricultural expert when necessary.

ACCURACY:
1. Never invent facts, statistics or government scheme details.
2. Never pretend to have checked live weather or mandi prices.
3. Clearly explain when current information is unavailable.
4. Distinguish verified facts from general suggestions.
5. If uncertain, say so honestly.

GENERAL QUESTIONS:
Answer questions about education, technology, science,
health information, daily life and other topics reliably.

SAFETY:
Do not provide dangerous instructions.
For medical, legal or financial matters, provide general
information and recommend qualified professional advice.

IDENTITY:
Your name is KRISHI MITRA.
Be friendly, respectful, patient and helpful.
Do not claim to be a human agricultural officer.
"""

    if farmer_profile:
        instruction += """

FARMER PROFILE:
Use the following information only when relevant.
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
    """Generate a conversational response using Gemini."""

    if not message or not message.strip():
        raise GeminiAPIError("Message cannot be empty.")

    try:
        client = get_gemini_client()

        conversation = []

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

        conversation.append(
            types.Content(
                role="user",
                parts=[types.Part(text=message.strip())]
            )
        )

        response = client.models.generate_content(
            model=get_model_name(),
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


def analyze_crop_disease(
    image_bytes: bytes,
    mime_type: str,
    crop_name: str,
    symptoms: str = "",
    affected_part: str = "",
    duration: str = "",
    farmer_profile: Optional[dict] = None,
) -> dict:
    """Analyze a crop image using Gemini vision."""

    if not image_bytes:
        raise GeminiAPIError("No crop image was provided.")

    if mime_type not in (
        "image/jpeg",
        "image/png",
        "image/webp",
    ):
        raise GeminiAPIError(
            "Please upload a JPG, PNG or WEBP image."
        )

    if not crop_name or not crop_name.strip():
        raise GeminiAPIError("Please provide the crop name.")

    profile_context = ""

    if farmer_profile:
        profile_context = f"""
Farmer location:
State: {farmer_profile.get("state") or "Unknown"}
District: {farmer_profile.get("district") or "Unknown"}
Taluk: {farmer_profile.get("taluk") or "Unknown"}
"""

    prompt = f"""
You are KRISHI MITRA, an agricultural crop-health assistant.

Analyze the attached crop image carefully.

FARMER INFORMATION:
Crop: {crop_name.strip()}
Affected plant part: {affected_part or "Not specified"}
Symptoms: {symptoms or "Not specified"}
Duration: {duration or "Not specified"}

{profile_context}

IMPORTANT RULES:
1. This is a preliminary assessment, not a confirmed diagnosis.
2. Do not invent symptoms that are not visible.
3. Separate visible observations from possible interpretations.
4. If the image is unclear, say so.
5. Give up to three possible conditions.
6. Use qualitative confidence: Low, Medium or High.
7. Explain what additional information would help.
8. Never invent pesticide names, doses or application schedules.
9. Do not claim a treatment is officially approved unless verified.
10. Recommend local KVK or agricultural expert advice when needed.

Respond in simple language suitable for farmers.
Use Kannada if the farmer's preferred language is Kannada.

Use these headings:

IMAGE QUALITY:
OBSERVATIONS:
MOST LIKELY CONDITION:
CONFIDENCE:
OTHER POSSIBILITIES:
WHY THIS MAY BE HAPPENING:
IMMEDIATE SAFE ACTIONS:
TREATMENT GUIDANCE:
PREVENTION:
WHEN TO CONTACT AN EXPERT:
ADDITIONAL INFORMATION NEEDED:
"""

    try:
        client = get_gemini_client()

        response = client.models.generate_content(
            model=get_model_name(),
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
                prompt,
            ],
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=1800,
            ),
        )

        answer = response.text

        if not answer or not answer.strip():
            raise GeminiAPIError(
                "Gemini could not analyze this image."
            )

        return {
            "assessment": answer.strip(),
            "crop": crop_name.strip(),
            "is_confirmed_diagnosis": False,
        }

    except GeminiAPIError:
        raise

    except Exception as error:
        raise GeminiAPIError(
            f"Crop image analysis failed: {error}"
        ) from error
