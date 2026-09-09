import os
import json
import sys

# Ensure UTF-8 output on Windows PowerShell / CMD
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class MultilingualEngine:
    """
    Dedicated Multilingual Engine for SIH26003.
    Provides localizations for English, Hindi, Assamese, Mizo, and Khasi.
    """
    SUPPORTED_LANGUAGES = ["english", "hindi", "assamese", "mizo", "khasi"]

    def __init__(self, dict_path=None):
        if dict_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            dict_path = os.path.join(base_dir, "json_language_packs", "master_multilingual_dictionary.json")
        
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                self.dictionary = json.load(f)
        else:
            self.dictionary = {}

    def get_encouragement(self, difficulty: str, language: str = "english") -> str:
        lang_key = language.lower()
        diff_key = difficulty.lower()
        prompts = self.dictionary.get("encouragement_prompts", {}).get(diff_key, {})
        return prompts.get(lang_key) or prompts.get("english", "Great job!")

    def get_voice_confirmation(self, language: str = "english") -> str:
        lang_key = language.lower()
        confirms = self.dictionary.get("voice_guidance_confirmations", {})
        return confirms.get(lang_key) or confirms.get("english", "Voice guidance active.")

if __name__ == "__main__":
    engine = MultilingualEngine()
    print("=========================================================")
    print(" SIH26003 Dedicated Multilingual Engine (5 Languages)")
    print("=========================================================")
    for lang in MultilingualEngine.SUPPORTED_LANGUAGES:
        prompt = engine.get_encouragement("medium", lang)
        confirm = engine.get_voice_confirmation(lang)
        print(f"\n🌐 [{lang.upper()}]")
        print(f"  * Encouragement : {prompt}")
        print(f"  * Voice Guidance: {confirm}")
