from frontend.i18n import (
    load_language_file,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
)

kannada = load_language_file("kn")
english = load_language_file("en")

assert DEFAULT_LANGUAGE == "kn"
assert "welcome" in kannada
assert "welcome" in english
assert "home" in kannada
assert "home" in english

print("Kannada translations: OK")
print("English translations: OK")
print("Supported languages:", SUPPORTED_LANGUAGES)
print("Language foundation test passed!")