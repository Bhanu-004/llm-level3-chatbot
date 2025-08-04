from deep_translator import GoogleTranslator

def translate_to_german(text):
    try:
        translated = GoogleTranslator(source='auto', target='de').translate(text)
        return f"🇩🇪 German Translation: {translated}"
    except Exception as e:
        return f"[Translation Error] {e}"