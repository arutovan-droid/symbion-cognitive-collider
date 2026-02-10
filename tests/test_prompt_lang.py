from symbion_cognitive_collider.detect_language import detect_prompt_language

def test_detect_ru():
    assert detect_prompt_language("Привет, как дела?") == "ru"

def test_detect_en():
    assert detect_prompt_language("Hello world, how are you?") == "en"
