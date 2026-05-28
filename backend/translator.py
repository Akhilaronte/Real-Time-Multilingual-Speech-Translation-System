# backend/translator.py
from transformers import MarianMTModel, MarianTokenizer

class Translator:
    def __init__(self):
        self.models = {}  # cache loaded models

    def _get_model(self, src_lang: str, tgt_lang: str):
        key = f"{src_lang}-{tgt_lang}"
        if key not in self.models:
            model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            self.models[key] = (tokenizer, model)
        return self.models[key]

    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        if src_lang == tgt_lang:
            return text
        tokenizer, model = self._get_model(src_lang, tgt_lang)
        inputs = tokenizer([text], return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)