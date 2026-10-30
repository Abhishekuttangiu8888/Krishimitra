
import re
import unicodedata


# English spoken digits
ENGLISH_DIGITS = {
    "zero": "0",
    "oh": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

# Kannada spoken digits
KANNADA_DIGITS = {
    "ಸೊನ್ನೆ": "0",
    "ಶೂನ್ಯ": "0",
    "ಒಂದು": "1",
    "ಎರಡು": "2",
    "ಮೂರು": "3",
    "ನಾಲ್ಕು": "4",
    "ಐದು": "5",
    "ಆರು": "6",
    "ಏಳು": "7",
    "ಎಂಟು": "8",
    "ಒಂಬತ್ತು": "9",
}


def normalize_mobile_number(text: str) -> str:
    """
    Extract mobile digits from English, Kannada,
    or mixed-language spoken text.
    """

    if not text:
        return ""

    text = unicodedata.normalize("NFC", text.lower())

    # First, convert spoken English and Kannada digits.
    tokens = re.findall(r"[a-z]+|[\u0C80-\u0CFF]+|\d+", text)

    digits = []

    for token in tokens:

        if token.isdigit():
            digits.append(token)

        elif token in ENGLISH_DIGITS:
            digits.append(ENGLISH_DIGITS[token])

        elif token in KANNADA_DIGITS:
            digits.append(KANNADA_DIGITS[token])

    return "".join(digits)


def validate_mobile_number(number: str) -> bool:
    """
    Validate an Indian 10-digit mobile number.
    """

    return bool(re.fullmatch(r"[6-9]\d{9}", number))


def extract_mobile_number(text: str) -> dict:
    """
    Extract and validate a mobile number.
    """

    number = normalize_mobile_number(text)

    if len(number) != 10:
        return {
            "success": False,
            "number": number,
            "message": "Please provide exactly 10 digits."
        }

    if not validate_mobile_number(number):
        return {
            "success": False,
            "number": number,
            "message": "Please provide a valid Indian mobile number."
        }

    return {
        "success": True,
        "number": number,
        "message": "Mobile number recognized."
    }


def extract_name(text: str) -> str:
    """
    Extract a name from common English or Kannada
    introductory sentences.

    If the answer is already a short name, preserve it.
    If a long sentence cannot be safely understood,
    return an empty value instead of saving the sentence.
    """

    if not text:
        return ""

    text = text.strip()

    patterns = [
        r"(?i)my name is\s+(.+)",
        r"(?i)i am\s+(.+)",
        r"(?i)i'm\s+(.+)",
        r"ನನ್ನ ಹೆಸರು\s+(.+)",
        r"ನಾನು\s+(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            candidate = match.group(1).strip()

            # Remove common trailing information.
            candidate = re.split(
                r"[,.;]|\s+(?:and|but|from|living|ನಾನು|ಮತ್ತು)\s+",
                candidate,
                maxsplit=1,
                flags=re.IGNORECASE
            )[0].strip()

            return candidate

    # A short answer may simply be the name.
    if len(text.split()) <= 3 and len(text) <= 50:
        return text

    # Never save an entire unclear sentence as a name.
    return ""
