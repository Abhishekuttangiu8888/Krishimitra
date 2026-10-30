

import re
import base64
import hashlib

from difflib import SequenceMatcher



import requests

import streamlit as st
import streamlit.components.v1 as components



from backend.integrations.sarvam import (

    transcribe_audio,

    SarvamAPIError,

)

from backend.integrations.sarvam_tts import (

    speak_text,

    SarvamTTSError,

)





API_URL = "http://127.0.0.1:8000/api"





# ---------------------------------------------------------

# REGISTRATION QUESTIONS

# ---------------------------------------------------------



FIELDS = [

    "name",

    "mobile",

    "district",

    "taluk",

    "village",

    "land_area",

    "land_unit",

    "ownership",

    "crops",

    "irrigation",

    "farming_type",

    "needs",

    "password",

]





QUESTIONS = {

    "name": "ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ತಿಳಿಸಿ.",

    "mobile": "ನಿಮ್ಮ ಹತ್ತು ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ತಿಳಿಸಿ.",

    "district": (

        "ನೀವು ಕರ್ನಾಟಕದ ಯಾವ ಜಿಲ್ಲೆಯಲ್ಲಿ ವಾಸಿಸುತ್ತೀರಿ? "

        "ಉದಾಹರಣೆಗೆ ಬೆಳಗಾವಿ, ಮಂಡ್ಯ ಅಥವಾ ಮೈಸೂರು."

    ),

    "taluk": "ನಿಮ್ಮ ತಾಲೂಕು ಯಾವುದು?",

    "village": "ನಿಮ್ಮ ಗ್ರಾಮದ ಹೆಸರನ್ನು ತಿಳಿಸಿ.",

    "land_area": (

        "ನಿಮ್ಮ ಬಳಿ ಎಷ್ಟು ಕೃಷಿ ಭೂಮಿ ಇದೆ? "

        "ಉದಾಹರಣೆಗೆ ಎರಡು ಅಥವಾ ಎರಡು ಪಾಯಿಂಟ್ ಐದು ಎಂದು ಹೇಳಿ."

    ),

    "land_unit": (

        "ನಿಮ್ಮ ಜಮೀನಿನ ಅಳತೆಯ ಘಟಕ ಯಾವುದು? "

        "ಎಕರೆ, ಗುಂಟೆ ಅಥವಾ ಹೆಕ್ಟೇರ್?"

    ),

    "ownership": (

        "ಜಮೀನು ನಿಮ್ಮ ಸ್ವಂತದ್ದೇ, ಗುತ್ತಿಗೆಗೆ ಪಡೆದಿದ್ದೀರಾ "

        "ಅಥವಾ ಹಂಚಿಕೆಯ ಜಮೀನೇ?"

    ),

    "crops": (

        "ನೀವು ಯಾವ ಬೆಳೆಗಳನ್ನು ಬೆಳೆಯುತ್ತೀರಿ? "

        "ಭತ್ತ, ರಾಗಿ, ಮೆಕ್ಕೆಜೋಳ, ಕಬ್ಬು, ಹತ್ತಿ, "

        "ನೆಲಗಡಲೆ ಅಥವಾ ಅಡಿಕೆ?"

    ),

    "irrigation": (

        "ನಿಮ್ಮ ಜಮೀನಿನಲ್ಲಿ ಯಾವ ನೀರಾವರಿ ವಿಧಾನವಿದೆ? "

        "ಮಳೆ ಆಧಾರಿತ, ಬೋರ್‌ವೆಲ್, ಕಾಲುವೆ, "

        "ಹನಿ ನೀರಾವರಿ ಅಥವಾ ಇತರೆ?"

    ),

    "farming_type": (

        "ನೀವು ಯಾವ ರೀತಿಯ ಕೃಷಿ ಮಾಡುತ್ತೀರಿ? "

        "ಸಾಂಪ್ರದಾಯಿಕ, ಸಾವಯವ, ಮಿಶ್ರ ಅಥವಾ ವಾಣಿಜ್ಯ ಕೃಷಿ?"

    ),

    "needs": (

        "ನಿಮಗೆ ಯಾವ ಸೇವೆಗಳು ಬೇಕು? "

        "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು, ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು, "

        "ಬೆಳೆ ರೋಗಗಳ ಮಾಹಿತಿ, ಹವಾಮಾನ ಅಥವಾ ಬೆಳೆ ಯೋಜನೆ?"

    ),

    "password": (

        "ಈಗ ನಿಮ್ಮ ಖಾತೆಗೆ ಪಾಸ್‌ವರ್ಡ್ ರಚಿಸಿ. "

        "ದಯವಿಟ್ಟು ಕೀಬೋರ್ಡ್ ಬಳಸಿ."

    ),

}





DISTRICTS = [

    "Bagalkote",

    "Ballari",

    "Belagavi",

    "Bengaluru Rural",

    "Bengaluru Urban",

    "Bidar",

    "Chamarajanagar",

    "Chikkaballapur",

    "Chikkamagaluru",

    "Chitradurga",

    "Dakshina Kannada",

    "Davanagere",

    "Dharwad",

    "Gadag",

    "Hassan",

    "Haveri",

    "Kalaburagi",

    "Kodagu",

    "Kolar",

    "Koppal",

    "Mandya",

    "Mysuru",

    "Raichur",

    "Ramanagara",

    "Shivamogga",

    "Tumakuru",

    "Udupi",

    "Uttara Kannada",

    "Vijayanagara",

    "Vijayapura",

    "Yadgir",

]





DISTRICT_KANNADA = {

    "ಬಾಗಲಕೋಟೆ": "Bagalkote",

    "ಬಳ್ಳಾರಿ": "Ballari",

    "ಬೆಳಗಾವಿ": "Belagavi",

    "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ": "Bengaluru Rural",

    "ಬೆಂಗಳೂರು ನಗರ": "Bengaluru Urban",

    "ಬೆಂಗಳೂರು": "Bengaluru Urban",

    "ಬೀದರ್": "Bidar",

    "ಚಾಮರಾಜನಗರ": "Chamarajanagar",

    "ಚಿಕ್ಕಬಳ್ಳಾಪುರ": "Chikkaballapur",

    "ಚಿಕ್ಕಮಗಳೂರು": "Chikkamagaluru",

    "ಚಿತ್ರದುರ್ಗ": "Chitradurga",

    "ದಕ್ಷಿಣ ಕನ್ನಡ": "Dakshina Kannada",

    "ದಾವಣಗೆರೆ": "Davanagere",

    "ಧಾರವಾಡ": "Dharwad",

    "ಗದಗ": "Gadag",

    "ಹಾಸನ": "Hassan",

    "ಹಾವೇರಿ": "Haveri",

    "ಕಲಬುರಗಿ": "Kalaburagi",

    "ಕೊಡಗು": "Kodagu",

    "ಕೋಲಾರ": "Kolar",

    "ಕೊಪ್ಪಳ": "Koppal",

    "ಮಂಡ್ಯ": "Mandya",

    "ಮೈಸೂರು": "Mysuru",

    "ರಾಯಚೂರು": "Raichur",

    "ರಾಮನಗರ": "Ramanagara",

    "ಶಿವಮೊಗ್ಗ": "Shivamogga",

    "ತುಮಕೂರು": "Tumakuru",

    "ಉಡುಪಿ": "Udupi",

    "ಉತ್ತರ ಕನ್ನಡ": "Uttara Kannada",

    "ವಿಜಯನಗರ": "Vijayanagara",

    "ವಿಜಯಪುರ": "Vijayapura",

    "ಯಾದಗಿರಿ": "Yadgir",

}





# ---------------------------------------------------------

# CHOICE ALIASES

# Each option can have several Kannada/English spellings.

# The matcher compares the farmer's answer with these.

# ---------------------------------------------------------



LAND_UNIT_CHOICES = {

    "Acre": [

        "acre", "acres", "ac",

        "ಎಕರೆ", "ಏಕರೆ", "ಎಕರ್", "ಏಕರ್",

        "ಎಕರೆಗಳು", "ಎಕ್ರೆ",

    ],

    "Gunta": [

        "gunta", "guntas",

        "ಗುಂಟೆ", "ಗುಂಟ", "ಗುಂಟಿ", "ಗಂಟೆ",

        "ಗುಂಟೆಗಳು",

    ],

    "Hectare": [

        "hectare", "hectares", "hector", "hectors",

        "hektare",

        "ಹೆಕ್ಟೇರ್", "ಹೆಕ್ಟರ್", "ಹೆಕ್ಟೇರು",

        "ಹೆಕ್ಟೇರುಗಳು",

    ],

}





OWNERSHIP_CHOICES = {

    "Owned": [

        "owned", "own", "my own", "my land",

        "ಸ್ವಂತ", "ಸ್ವಂತದ್ದು", "ನನ್ನದು",

        "ನನ್ನ ಸ್ವಂತ", "ನನ್ನ ಜಮೀನು",

    ],

    "Leased": [

        "leased", "lease", "rented", "rent",

        "ಗುತ್ತಿಗೆ", "ಗುತ್ತಿಗೆಗೆ", "ಬಾಡಿಗೆ",

        "ಬಾಡಿಗೆಗೆ", "ಲೀಸ್",

    ],

    "Shared": [

        "shared", "sharing", "joint ownership",

        "ಹಂಚಿಕೆ", "ಹಂಚಿಕೆಯ", "ಹಂಚಿಕೆಯ ಜಮೀನು",

        "ಜಂಟಿ", "ಜಂಟಿ ಜಮೀನು",

    ],

}





CROP_CHOICES = {

    "Paddy": [

        "paddy", "rice",

        "ಭತ್ತ", "ಅಕ್ಕಿ",

    ],

    "Ragi": [

        "ragi", "finger millet",

        "ರಾಗಿ",

    ],

    "Maize": [

        "maize", "corn",

        "ಮೆಕ್ಕೆಜೋಳ", "ಮೆಕ್ಕೆ",

    ],

    "Sugarcane": [

        "sugarcane", "sugar cane",

        "ಕಬ್ಬು",

    ],

    "Cotton": [

        "cotton",

        "ಹತ್ತಿ",

    ],

    "Groundnut": [

        "groundnut", "peanut",

        "ನೆಲಗಡಲೆ", "ಶೇಂಗಾ",

    ],

    "Arecanut": [

        "arecanut", "areca nut", "supari",

        "ಅಡಿಕೆ",

    ],

    "Other": [

        "other", "others",

        "ಇತರೆ", "ಬೇರೆ",

    ],

}





IRRIGATION_CHOICES = {

    "Rainfed": [

        "rainfed", "rain fed", "rain",

        "ಮಳೆ ಆಧಾರಿತ", "ಮಳೆ", "ಮಳೆ ನೀರು",

    ],

    "Borewell": [

        "borewell", "bore well", "bore",

        "ಬೋರ್ವೆಲ್", "ಬೋರ್‌ವೆಲ್", "ಬೋರ್", "ಬೋರ್ ವೆಲ್",

    ],

    "Canal": [

        "canal", "canal water",

        "ಕಾಲುವೆ", "ಕಾಲುವೆ ನೀರು",

    ],

    "Drip": [

        "drip", "drip irrigation",

        "ಹನಿ", "ಹನಿ ನೀರಾವರಿ",

    ],

    "Other": [

        "other", "others",

        "ಇತರೆ", "ಬೇರೆ",

    ],

}





FARMING_TYPE_CHOICES = {

    "Traditional": [

        "traditional", "normal farming",

        "ಸಾಂಪ್ರದಾಯಿಕ", "ಸಾಂಪ್ರದಾಯಿಕ ಕೃಷಿ",

    ],

    "Organic": [

        "organic", "organic farming",

        "ಸಾವಯವ", "ಸಾವಯವ ಕೃಷಿ",

    ],

    "Mixed": [

        "mixed", "mixed farming",

        "ಮಿಶ್ರ", "ಮಿಶ್ರ ಕೃಷಿ",

    ],

    "Commercial": [

        "commercial", "commercial farming",

        "ವಾಣಿಜ್ಯ", "ವಾಣಿಜ್ಯ ಕೃಷಿ",

    ],

}





NEEDS_CHOICES = {

    "Government schemes": [

        "government schemes", "government scheme",

        "scheme", "schemes",

        "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು", "ಸರ್ಕಾರಿ ಯೋಜನೆ",

        "ಯೋಜನೆಗಳು", "ಯೋಜನೆ",

    ],

    "Mandi prices": [

        "mandi prices", "mandi price",

        "market prices", "market price",

        "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು", "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",

        "ಮಾರುಕಟ್ಟೆ", "ಮಂಡಿ", "ಬೆಲೆ",

    ],

    "Crop disease help": [

        "crop disease", "crop diseases",

        "disease help", "disease",

        "ಬೆಳೆ ರೋಗ", "ಬೆಳೆ ರೋಗಗಳು", "ರೋಗ",

    ],

    "Weather": [

        "weather", "climate",

        "ಹವಾಮಾನ",

    ],

    "Crop planning": [

        "crop planning", "crop plan",

        "ಬೆಳೆ ಯೋಜನೆ", "ಬೆಳೆ ಯೋಜನೆಗಳು",

    ],

}





# ---------------------------------------------------------

# NUMBER EXTRACTION

# ---------------------------------------------------------



KANNADA_DIGITS = {

    "೦": "0",

    "೧": "1",

    "೨": "2",

    "೩": "3",

    "೪": "4",

    "೫": "5",

    "೬": "6",

    "೭": "7",

    "೮": "8",

    "೯": "9",

}





ENGLISH_NUMBERS = {

    "zero": 0,

    "one": 1,

    "two": 2,

    "three": 3,

    "four": 4,

    "five": 5,

    "six": 6,

    "seven": 7,

    "eight": 8,

    "nine": 9,

    "ten": 10,

    "eleven": 11,

    "twelve": 12,

    "thirteen": 13,

    "fourteen": 14,

    "fifteen": 15,

    "sixteen": 16,

    "seventeen": 17,

    "eighteen": 18,

    "nineteen": 19,

    "twenty": 20,

}





KANNADA_NUMBERS = {

    "ಸೊನ್ನೆ": 0,

    "ಶೂನ್ಯ": 0,

    "ಒಂದು": 1,

    "ಒಂದ": 1,

    "ಎರಡು": 2,

    "ಮೂರು": 3,

    "ನಾಲ್ಕು": 4,

    "ಐದು": 5,

    "ಆರು": 6,

    "ಏಳು": 7,

    "ಎಂಟು": 8,

    "ಒಂಬತ್ತು": 9,

    "ಹತ್ತು": 10,

    "ಹನ್ನೊಂದು": 11,

    "ಹನ್ನೆರಡು": 12,

    "ಹದಿಮೂರು": 13,

    "ಹದಿನಾಲ್ಕು": 14,

    "ಹದಿನೈದು": 15,

    "ಹದಿನಾರು": 16,

    "ಹದಿನೇಳು": 17,

    "ಹದಿನೆಂಟು": 18,

    "ಹತ್ತೊಂಬತ್ತು": 19,

    "ಇಪ್ಪತ್ತು": 20,

}





def normalize_digits(text):

    for kannada, english in KANNADA_DIGITS.items():

        text = text.replace(kannada, english)



    return text





def extract_number(text):

    if not text:

        return None



    text = normalize_digits(text.lower().strip())



    match = re.search(r"\d+(?:\.\d+)?", text)



    if match:

        return float(match.group())



    half_values = {

        "ಅರ್ಧ": 0.5,

        "ಒಂದೂವರೆ": 1.5,

        "ಎರಡೂವರೆ": 2.5,

        "ಮೂರೂವರೆ": 3.5,

        "ನಾಲ್ಕೂವರೆ": 4.5,

        "ಐದೂವರೆ": 5.5,

        "one and a half": 1.5,

        "two and a half": 2.5,

        "three and a half": 3.5,

        "half": 0.5,

    }



    for word, value in half_values.items():

        if word in text:

            return float(value)



    match = re.search(

        r"\b(one|two|three|four|five|six|seven|eight|nine|ten)"

        r"\s+point\s+"

        r"(zero|one|two|three|four|five|six|seven|eight|nine)\b",

        text,

    )



    if match:

        first = ENGLISH_NUMBERS[match.group(1)]

        second = ENGLISH_NUMBERS[match.group(2)]

        return float(f"{first}.{second}")



    match = re.search(

        r"(ಒಂದು|ಎರಡು|ಮೂರು|ನಾಲ್ಕು|ಐದು|ಆರು|ಏಳು|ಎಂಟು|ಒಂಬತ್ತು|ಹತ್ತು)"

        r"\s+ಪಾಯಿಂಟ್\s+"

        r"(ಸೊನ್ನೆ|ಶೂನ್ಯ|ಒಂದು|ಎರಡು|ಮೂರು|ನಾಲ್ಕು|ಐದು|ಆರು|ಏಳು|ಎಂಟು|ಒಂಬತ್ತು)",

        text,

    )



    if match:

        first = KANNADA_NUMBERS[match.group(1)]

        second = KANNADA_NUMBERS[match.group(2)]

        return float(f"{first}.{second}")



    for word, value in ENGLISH_NUMBERS.items():

        if re.search(r"\b" + re.escape(word) + r"\b", text):

            return float(value)



    for word, value in KANNADA_NUMBERS.items():

        if word in text:

            return float(value)



    return None





# ---------------------------------------------------------

# MOBILE NUMBER EXTRACTION

# ---------------------------------------------------------



MOBILE_WORDS = {

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





def extract_mobile(text):

    if not text:

        return ""



    text = normalize_digits(text.lower())



    for word, digit in sorted(

        MOBILE_WORDS.items(),

        key=lambda item: len(item[0]),

        reverse=True,

    ):

        text = text.replace(word, digit)



    digits = re.sub(r"\D", "", text)



    if len(digits) == 12 and digits.startswith("91"):

        digits = digits[2:]



    if len(digits) == 10 and digits[0] in "6789":

        return digits



    return ""





# ---------------------------------------------------------

# TEXT CLEANING

# ---------------------------------------------------------



def clean_answer(text):

    if not text:

        return ""



    text = text.strip()



    prefixes = [

        r"^my name is\s+",

        r"^i am\s+",

        r"^i'm\s+",

        r"^ನನ್ನ ಹೆಸರು\s+",

        r"^ನಾನು\s+",

    ]



    for pattern in prefixes:

        text = re.sub(

            pattern,

            "",

            text,

            flags=re.IGNORECASE,

        )



    return text.strip(" .,!?:;")





def normalize_match_text(text):

    text = text.lower().strip()

    return re.sub(r"[\W\_]+", "", text, flags=re.UNICODE)





def match_district(text):

    lower = text.lower()



    for kannada, english in DISTRICT_KANNADA.items():

        if kannada in text:

            return english



    for district in DISTRICTS:

        if district.lower() in lower:

            return district



    return ""





# ---------------------------------------------------------

# GENERAL FUZZY CHOICE MATCHER

# Used by all predefined-choice questions.

# ---------------------------------------------------------



def get_text_parts(text):

    """

    Break an answer into words and short word groups.



    This allows the matcher to recognize a choice inside

    a complete sentence instead of comparing only the

    entire sentence.

    """

    words = re.findall(r"[\w]+", text.lower(), flags=re.UNICODE)



    parts = [text.lower().strip()]

    parts.extend(words)



    for size in range(2, min(4, len(words)) + 1):

        for index in range(len(words) - size + 1):

            parts.append(" ".join(words[index:index + size]))



    return list(set(parts))





def get_alias_score(answer, alias):

    normalized_answer = normalize_match_text(answer)

    normalized_alias = normalize_match_text(alias)



    if not normalized_answer or not normalized_alias:

        return 0.0



    # Exact match.

    if normalized_answer == normalized_alias:

        return 1.0



    # Alias is present inside the complete answer.

    if (

        len(normalized_alias) >= 3

        and normalized_alias in normalized_answer

    ):

        return 1.0



    best_score = 0.0



    for part in get_text_parts(answer):

        normalized_part = normalize_match_text(part)



        if not normalized_part:

            continue



        score = SequenceMatcher(

            None,

            normalized_part,

            normalized_alias,

        ).ratio()



        best_score = max(best_score, score)



    return best_score





def get_choice_scores(answer, choices):

    """

    Calculate the best similarity score for every option.

    """

    scores = {}



    for option, aliases in choices.items():

        best_score = 0.0



        for alias in aliases:

            score = get_alias_score(answer, alias)

            best_score = max(best_score, score)



        scores[option] = best_score



    return scores





def match_single_choice(answer, choices, threshold=0.72):

    """

    Match one option.



    Returns an option only when:

    - It passes the confidence threshold.

    - It is sufficiently closer than the second-best option.

    """

    if not answer:

        return ""



    scores = get_choice_scores(answer, choices)



    ranked = sorted(

        scores.items(),

        key=lambda item: item[1],

        reverse=True,

    )



    if not ranked:

        return ""



    best_option, best_score = ranked[0]

    second_score = ranked[1][1] if len(ranked) > 1 else 0.0



    if best_score < threshold:

        return ""



    if best_score - second_score < 0.05:

        return ""



    return best_option





def match_multiple_choices(answer, choices, threshold=0.76):

    """

    Match multiple options from one spoken answer.



    Example:

    'I grow paddy and ragi'

    returns ['Paddy', 'Ragi'].



    Each option is evaluated separately.

    """

    if not answer:

        return []



    scores = get_choice_scores(answer, choices)



    found = [

        option

        for option, score in scores.items()

        if score >= threshold

    ]



    return found





# ---------------------------------------------------------

# FIELD EXTRACTION

# ---------------------------------------------------------



def get_field_value(step, transcript):

    text = transcript.strip()

    lower = text.lower()



    if step == "name":

        return clean_answer(text)



    if step == "mobile":

        return extract_mobile(text)



    if step == "district":

        return match_district(text)



    if step in ["taluk", "village"]:

        return clean_answer(text)



    if step == "land_area":

        return extract_number(text)



    # Single-choice question: closest reliable match.

    if step == "land_unit":

        return match_single_choice(

            text,

            LAND_UNIT_CHOICES,

            threshold=0.72,

        )



    # Single-choice question: closest reliable match.

    if step == "ownership":

        return match_single_choice(

            text,

            OWNERSHIP_CHOICES,

            threshold=0.72,

        )



    # Multiple-choice question: collect recognized crops.

    if step == "crops":

        return match_multiple_choices(

            text,

            CROP_CHOICES,

            threshold=0.76,

        )



    # Single-choice question.

    if step == "irrigation":

        return match_single_choice(

            text,

            IRRIGATION_CHOICES,

            threshold=0.72,

        )



    # Single-choice question.

    if step == "farming_type":

        return match_single_choice(

            text,

            FARMING_TYPE_CHOICES,

            threshold=0.72,

        )



    # Multiple-choice question: collect recognized services.

    if step == "needs":

        return match_multiple_choices(

            text,

            NEEDS_CHOICES,

            threshold=0.76,

        )



    return ""





# ---------------------------------------------------------

# SESSION STATE

# ---------------------------------------------------------



def initialize_state():

    defaults = {

        "voice_registration_step": "name",

        "voice_registration_data": {},

        "voice_registration_started": False,

        "voice_registration_pending_tts": False,
        "voice_registration_last_audio_hash": None,

    }



    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value





def next_step():

    current = st.session_state.voice_registration_step

    index = FIELDS.index(current)



    if index < len(FIELDS) - 1:

        st.session_state.voice_registration_step = FIELDS[index + 1]

    else:

        st.session_state.voice_registration_step = "review"





# ---------------------------------------------------------

# KANNADA TEXT TO SPEECH

# ---------------------------------------------------------



def play_kannada_voice(text):
    """Play generated Kannada speech without showing the black audio player."""
    try:
        with st.spinner("ಕನ್ನಡ ಧ್ವನಿ ಸಿದ್ಧವಾಗುತ್ತಿದೆ..."):
            audio_bytes = speak_text(text)

        if not audio_bytes:
            st.warning("ಧ್ವನಿ ಸೃಷ್ಟಿಯಾಗಿಲ್ಲ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")
            return

        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        components.html(
            f"""
            <audio autoplay>
                <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
            </audio>
            """,
            height=0,
        )
    except SarvamTTSError as error:
        st.error(f"ಕನ್ನಡ ಧ್ವನಿ ದೋಷ: {error}")
    except Exception as error:
        st.error(f"ಧ್ವನಿ ದೋಷ: {error}")


# ---------------------------------------------------------
# PROCESS MICROPHONE RECORDING

# ---------------------------------------------------------



def process_audio():

    audio = st.session_state.get(

        "voice_registration_audio_input"

    )



    if audio is None:

        st.warning("ದಯವಿಟ್ಟು ಮೊದಲು ಮೈಕ್ರೋಫೋನ್ ಬಳಸಿ ಮಾತನಾಡಿ.")

        return



    current = st.session_state.voice_registration_step



    try:

        with st.spinner("ನಿಮ್ಮ ಮಾತನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಾಗುತ್ತಿದೆ..."):

            transcript = transcribe_audio(

                audio_bytes=audio.getvalue(),

                filename="recording.wav",

            )["text"]



        st.caption(f"ಗುರುತಿಸಿದ ಮಾತು: {transcript}")



        value = get_field_value(current, transcript)



        if value is None or value == "" or value == []:

            st.warning(

                "ನಿಮ್ಮ ಉತ್ತರವನ್ನು ಸರಿಯಾಗಿ ಗುರುತಿಸಲಾಗಲಿಲ್ಲ. "

                "ದಯವಿಟ್ಟು ಅದೇ ಪ್ರಶ್ನೆಗೆ ಮತ್ತೆ ಉತ್ತರಿಸಿ."

            )

            return



        if current == "mobile" and not value:

            st.warning("ಸರಿಯಾದ 10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ಹೇಳಿ.")

            return



        if current == "land_area" and value <= 0:

            st.warning("ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ ಶೂನ್ಯಕ್ಕಿಂತ ಹೆಚ್ಚಿರಬೇಕು.")

            return



        st.session_state.voice_registration_data[current] = value



        # Move forward only after a valid answer.

        next_step()



        st.session_state.voice_registration_pending_tts = True



        st.session_state.pop("voice_registration_audio_input", None)



        st.rerun()



    except SarvamAPIError as error:

        st.error(f"ಧ್ವನಿಯನ್ನು ಗುರುತಿಸುವಲ್ಲಿ ತೊಂದರೆ: {error}")



    except Exception as error:

        st.error(f"ದೋಷ: {error}")





# ---------------------------------------------------------

# PASSWORD

# ---------------------------------------------------------



def render_password_field():

    st.subheader("ಖಾತೆಯ ಪಾಸ್‌ವರ್ಡ್")



    st.info(

        "ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್ ಅನ್ನು ಧ್ವನಿಯಲ್ಲಿ ಹೇಳಬೇಡಿ. "

        "ಕೀಬೋರ್ಡ್ ಬಳಸಿ ನಮೂದಿಸಿ."

    )



    password = st.text_input(

        "ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ",

        type="password",

        key="voice_registration_password",

    )



    confirm = st.text_input(

        "ಪಾಸ್‌ವರ್ಡ್ ಮತ್ತೆ ನಮೂದಿಸಿ",

        type="password",

        key="voice_registration_confirm_password",

    )



    if st.button(

        "ಮುಂದೆ",

        type="primary",

        use_container_width=True,

    ):

        if len(password) < 8:

            st.error("ಪಾಸ್‌ವರ್ಡ್ ಕನಿಷ್ಠ 8 ಅಕ್ಷರಗಳಿರಬೇಕು.")



        elif password != confirm:

            st.error("ಎರಡೂ ಪಾಸ್‌ವರ್ಡ್‌ಗಳು ಒಂದೇ ಆಗಿರಬೇಕು.")



        else:

            st.session_state.voice_registration_data["password"] = password

            next_step()

            st.rerun()





# ---------------------------------------------------------

# FINAL REVIEW

# ---------------------------------------------------------



def render_review():

    data = st.session_state.voice_registration_data



    st.subheader("ನಿಮ್ಮ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ")



    st.info(

        "ಖಾತೆ ರಚಿಸುವ ಮೊದಲು ನಿಮ್ಮ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ. "

        "ತಪ್ಪಿದ್ದರೆ ನೋಂದಣಿಯನ್ನು ಮತ್ತೆ ಪ್ರಾರಂಭಿಸಬಹುದು."

    )



    review_fields = [

        ("name", "ಹೆಸರು"),

        ("mobile", "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ"),

        ("district", "ಜಿಲ್ಲೆ"),

        ("taluk", "ತಾಲೂಕು"),

        ("village", "ಗ್ರಾಮ"),

        ("land_area", "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ"),

        ("land_unit", "ಅಳತೆಯ ಘಟಕ"),

        ("ownership", "ಮಾಲೀಕತ್ವ"),

        ("crops", "ಬೆಳೆಗಳು"),

        ("irrigation", "ನೀರಾವರಿ ವಿಧಾನ"),

        ("farming_type", "ಕೃಷಿ ವಿಧಾನ"),

        ("needs", "ಬೇಕಾದ ಸೇವೆಗಳು"),

    ]



    for key, label in review_fields:

        value = data.get(key, "")



        if isinstance(value, list):

            value = ", ".join(value)



        st.write(f"**{label}:** {value}")



    if st.button(

        "ಖಾತೆ ರಚಿಸಿ",

        type="primary",

        use_container_width=True,

    ):

        create_account()



    if st.button(

        "ನೋಂದಣಿ ಮತ್ತೆ ಪ್ರಾರಂಭಿಸಿ",

        use_container_width=True,

    ):

        reset_registration()

        st.rerun()





# ---------------------------------------------------------

# CREATE ACCOUNT USING EXISTING FASTAPI API

# ---------------------------------------------------------



def create_account():

    data = st.session_state.voice_registration_data



    try:

        profile = {

            "full_name": data["name"],

            "preferred_language": "kn",

            "state": "Karnataka",

            "district": data["district"],

            "taluk": data["taluk"],

            "village": data["village"],

            "land_area": str(data["land_area"]),

            "land_unit": data["land_unit"],

            "land_ownership": data["ownership"],

            "crops": data["crops"],

            "irrigation_method": data["irrigation"],

            "farming_type": data["farming_type"],

            "needs": data["needs"],

        }



        payload = {

            "mobile": data["mobile"],

            "password": data["password"],

            "profile": profile,

        }



        with st.spinner("ನಿಮ್ಮ ಖಾತೆಯನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ..."):

            response = requests.post(

                f"{API_URL}/auth/signup",

                json=payload,

                timeout=30,

            )



        if response.status_code in [200, 201]:

            result = response.json()

            token = result.get("access_token")



            if not token:

                st.error("ಸರ್ವರ್‌ನಿಂದ ಲಾಗಿನ್ ಟೋಕನ್ ದೊರೆಯಲಿಲ್ಲ.")

                return



            st.session_state.km_token = token

            st.session_state.km_mobile = data["mobile"]

            st.session_state.km_logged_in = True



            reset_registration()



            st.success("ನಿಮ್ಮ ಖಾತೆ ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ!")

            st.rerun()



        else:

            try:

                detail = response.json().get(

                    "detail",

                    response.text,

                )

            except ValueError:

                detail = response.text



            st.error(f"ನೋಂದಣಿ ವಿಫಲವಾಗಿದೆ: {detail}")



    except requests.RequestException as error:

        st.error(f"ಸರ್ವರ್ ಸಂಪರ್ಕ ದೋಷ: {error}")



    except Exception as error:

        st.error(f"ಖಾತೆ ರಚಿಸುವಲ್ಲಿ ದೋಷ: {error}")





# ---------------------------------------------------------

# RESET REGISTRATION

# ---------------------------------------------------------



def reset_registration():

    st.session_state.voice_registration_step = "name"

    st.session_state.voice_registration_data = {}

    st.session_state.voice_registration_started = False

    st.session_state.voice_registration_pending_tts = False



    keys_to_remove = [

        "voice_registration_password",

        "voice_registration_confirm_password",

        "voice_registration_audio_input",
        "voice_registration_last_audio_hash",

    ]



    for key in keys_to_remove:

        st.session_state.pop(key, None)





# ---------------------------------------------------------

# MAIN VOICE REGISTRATION SCREEN

# ---------------------------------------------------------



def render_voice_registration():
    initialize_state()

    st.markdown(
        """
        <style>
        .stApp { background: #f7faf7; }
        .km-voice-orb {
            width: 112px; height: 112px; border-radius: 50%;
            margin: 22px auto 16px; display: flex;
            align-items: center; justify-content: center;
            color: white; font-size: 42px;
            background: radial-gradient(circle at 35% 30%, #76d99b, #23834a 72%);
            box-shadow: 0 0 0 11px #e5f4e9, 0 8px 30px rgba(35,131,74,.18);
        }
        .km-question {
            background: white; border: 1px solid #dcebdd;
            border-radius: 16px; padding: 20px 18px;
            color: #203b2b; font-size: 19px; text-align: center;
            margin: 16px 0;
        }
        .km-voice-caption {
            text-align: center; color: #23834a;
            font-weight: 600; margin: 8px 0 16px;
        }
        div.stButton > button[kind="primary"] {
            background: #23834a; border: 0; border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



    st.title("🌱 ಕೃಷಿ ಮಿತ್ರ")

    st.subheader("ಧ್ವನಿ ಮೂಲಕ ರೈತರ ನೋಂದಣಿ")



    st.write(

        "ನಿಮ್ಮ ಮಾಹಿತಿಯನ್ನು ಕನ್ನಡ, ಇಂಗ್ಲಿಷ್ ಅಥವಾ ಎರಡೂ ಭಾಷೆಗಳಲ್ಲಿ "

        "ಮಾತನಾಡಬಹುದು. ನಾನು ಒಂದೊಂದೇ ಪ್ರಶ್ನೆ ಕೇಳುತ್ತೇನೆ."

    )



    step = st.session_state.voice_registration_step



    if step == "review":

        render_review()

        return



    if step == "password":

        render_password_field()

        return



    current_index = FIELDS.index(step) + 1



    st.progress(current_index / len(FIELDS))



    st.caption(

        f"ಪ್ರಶ್ನೆ {current_index} / {len(FIELDS)}"

    )



    if not st.session_state.voice_registration_started:

        if st.button(

            "🎙️ ಧ್ವನಿ ಸಹಾಯಕ ಪ್ರಾರಂಭಿಸಿ",

            type="primary",

            use_container_width=True,

        ):

            st.session_state.voice_registration_started = True

            st.session_state.voice_registration_pending_tts = True

            st.rerun()



        return



    if st.session_state.voice_registration_pending_tts:
        st.session_state.voice_registration_pending_tts = False
        play_kannada_voice(QUESTIONS[step])

    st.markdown('<div class="km-voice-orb">♫</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="km-question">{QUESTIONS[step]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="km-voice-caption">🎙️ ನಿಮ್ಮ ಉತ್ತರವನ್ನು ಮಾತನಾಡಿ</div>',
        unsafe_allow_html=True,
    )

    audio = st.audio_input(
        "ಮೈಕ್ರೋಫೋನ್ ಒತ್ತಿ ಮಾತನಾಡಿ",
        key="voice_registration_audio_input",
    )

    # Streamlit reruns after recording; process each recording only once.
    if audio is not None:
        audio_hash = hashlib.sha256(audio.getvalue()).hexdigest()
        if audio_hash != st.session_state.get("voice_registration_last_audio_hash"):
            st.session_state["voice_registration_last_audio_hash"] = audio_hash
            process_audio()

    if st.button(

        "ಪ್ರಶ್ನೆಯನ್ನು ಮತ್ತೆ ಕೇಳಿ",

        use_container_width=True,

    ):

        st.session_state.voice_registration_pending_tts = True

        st.rerun()



    if st.button(

        "ನೋಂದಣಿ ರದ್ದುಮಾಡಿ",

        use_container_width=True,

    ):

        reset_registration()

        st.rerun()
