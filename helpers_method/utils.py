import os

def get_project_directory():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def clean_text(text):
    """
    Cleans the input text by removing specific unwanted substrings.

    This function replaces various specific substrings in the input text 
    with empty strings to clean up the text.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    text = text.replace("&amp;", "").replace("8)", "").replace("@\n¢","").replace("@\n¢8",""
    ).replace("(w","").replace("@\n 8 8)", "").replace("()", "").replace("/ -", "").replace(
    "\,", "").replace("8）", "").replace("@\n 8  ","").replace("8(", "")
    
    return text


def initialize_ocr():
    project_dir = get_project_directory()

    fonts = {
        "ar": os.path.join(project_dir, "fonts/arial.ttf"),           # Arabic
        "af": os.path.join(project_dir, "fonts/africans.ttf"),        # Afrikaans
        "az": os.path.join(project_dir, "fonts/azerbaigan.ttf"),      # Azerbaijani
        "bg": os.path.join(project_dir, "fonts/ballgarian.ttf"),      # Bulgarian
        "cs": os.path.join(project_dir, "fonts/cbesh.ttf"),           # Czech
        "de": os.path.join(project_dir, "fonts/german.ttf"),          # German
        "en": os.path.join(project_dir, "fonts/simfang.ttf"),         # English
        "es": os.path.join(project_dir, "fonts/spanish.ttf"),         # Spanish
        "fr": os.path.join(project_dir, "fonts/french.ttf"),          # French
        "hu": os.path.join(project_dir, "fonts/hungrian.ttf"),        # Hungarian
        "hi": os.path.join(project_dir, "fonts/hindi.ttf"),           # Hindi
        "it": os.path.join(project_dir, "fonts/italian.ttf"),         # Italian
        "ja": os.path.join(project_dir, "fonts/japan.ttc"),           # Japanese
        "ko": os.path.join(project_dir, "fonts/korean.ttf"),          # Korean
        "lv": os.path.join(project_dir, "fonts/latinva.ttf"),         # Latvian
        "mr": os.path.join(project_dir, "fonts/marathi.ttf"),         # Marathi
        "no": os.path.join(project_dir, "fonts/norway.ttf"),          # Norwegian
        "ne": os.path.join(project_dir, "fonts/nepali.ttf"),          # Nepali
        "nl": os.path.join(project_dir, "fonts/dutch.ttf"),           # Dutch
        "pt": os.path.join(project_dir, "fonts/portuguese.ttf"),      # Portuguese
        "pl": os.path.join(project_dir, "fonts/polish.ttf"),          # Polish
        "ru": os.path.join(project_dir, "fonts/cyrillic.ttf"),        # Russian
        "ro": os.path.join(project_dir, "fonts/romania.ttf"),         # Romanian
        "sa": os.path.join(project_dir, "fonts/arial.ttf"),           # Sanskrit
        "sv": os.path.join(project_dir, "fonts/swedish.ttf"),         # Swedish
        "sq": os.path.join(project_dir, "fonts/albanian.ttf"),        # Albanian
        "sl": os.path.join(project_dir, "fonts/slovenian.ttf"),       # Slovenian
        "sk": os.path.join(project_dir, "fonts/slovak.ttf"),          # Slovak
        "tr": os.path.join(project_dir, "fonts/turkish.ttf"),         # Turkish
        "tl": os.path.join(project_dir, "fonts/tagalog.ttf"),         # Tagalog
        "ta": os.path.join(project_dir, "fonts/tamil.ttf"),           # Tamil
        "te": os.path.join(project_dir, "fonts/telugu.ttf"),          # Telugu
        "ur": os.path.join(project_dir, "fonts/arial.ttf"),           # Urdu
        "uk": os.path.join(project_dir, "fonts/ukrainian.ttf"),       # Ukrainian
        "uz": os.path.join(project_dir, "fonts/uzbek.ttf"),           # Uzbek
        "zh": os.path.join(project_dir, "fonts/chinese_cht.ttf"),     # Chinese
    }

    ocr_configs = {
        "ar": {"use_angle_cls": True, "lang": "ar"},  # Arabic
        "af": {"use_angle_cls": True, "lang": "af"},  # Afrikaans
        "az": {"use_angle_cls": True, "lang": "az"},  # Azerbaijani
        "bg": {"use_angle_cls": True, "lang": "bg"},  # Bulgarian
        "cs": {"use_angle_cls": True, "lang": "cs"},  # Czech
        "de": {"use_angle_cls": True, "lang": "de"},  # German
        "en": {"use_angle_cls": True, "lang": "en"},  # English
        "es": {"use_angle_cls": True, "lang": "es"},  # Spanish
        "fr": {"use_angle_cls": True, "lang": "fr"},  # French
        "hu": {"use_angle_cls": True, "lang": "hu"},  # Hungarian
        "hi": {"use_angle_cls": True, "lang": "hi"},  # Hindi
        "it": {"use_angle_cls": True, "lang": "it"},  # Italian
        "ja": {"use_angle_cls": True, "lang": "ja"},  # Japanese
        "ko": {"use_angle_cls": True, "lang": "ko"},  # Korean
        "lv": {"use_angle_cls": True, "lang": "lv"},  # Latvian
        "mr": {"use_angle_cls": True, "lang": "mr"},  # Marathi
        "no": {"use_angle_cls": True, "lang": "no"},  # Norwegian
        "ne": {"use_angle_cls": True, "lang": "ne"},  # Nepali
        "nl": {"use_angle_cls": True, "lang": "nl"},  # Dutch
        "pt": {"use_angle_cls": True, "lang": "pt"},  # Portuguese
        "pl": {"use_angle_cls": True, "lang": "pl"},  # Polish
        "ru": {"use_angle_cls": True, "lang": "ru"},  # Russian
        "ro": {"use_angle_cls": True, "lang": "ro"},  # Romanian
        "sa": {"use_angle_cls": True, "lang": "sa"},  # Sanskrit
        "sv": {"use_angle_cls": True, "lang": "sv"},  # Swedish
        "sq": {"use_angle_cls": True, "lang": "sq"},  # Albanian
        "sl": {"use_angle_cls": True, "lang": "sl"},  # Slovenian
        "sk": {"use_angle_cls": True, "lang": "sk"},  # Slovak
        "tr": {"use_angle_cls": True, "lang": "tr"},  # Turkish
        "tl": {"use_angle_cls": True, "lang": "tl"},  # Tagalog
        "ta": {"use_angle_cls": True, "lang": "ta"},  # Tamil
        "te": {"use_angle_cls": True, "lang": "te"},  # Telugu
        "ur": {"use_angle_cls": True, "lang": "ur"},  # Urdu
        "uk": {"use_angle_cls": True, "lang": "uk"},  # Ukrainian
        "uz": {"use_angle_cls": True, "lang": "uz"},  # Uzbek
        "zh": {"use_angle_cls": True, "lang": "zh"},  # Chinese
    }

    return ocr_configs, fonts


def get_translate_headers():
    """
    Returns the HTTP headers required for making a request to Yandex Translate.

    This function constructs and returns a dictionary of HTTP headers typically 
    used for making requests to the Yandex Translate service.

    Returns:
        dict: A dictionary containing the necessary HTTP headers.
    """
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://translate.yandex.com",
        "Referer": "https://translate.yandex.com/",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
    }
