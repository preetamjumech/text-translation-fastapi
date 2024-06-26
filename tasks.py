from models import TranslationModel
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("t5-small", max_length = 512)
translator = T5ForConditionalGeneration.from_pretrained("t5-small")

#store the translation
def store_translation(t):
    model = TranslationModel(text = t.text, base_lang = t.base_lang, final_lang = t.final_lang)
    model.save()
    return model.id

#run the translation
def run_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)
    prefix = f"translate {model.base_lang} to {model.final_lang}: {model.text}"
    input_ids = tokenizer(prefix, return_tensors = "pt").input_ids
    outputs = translator.generate(input_ids, max_new_tokens = 512)
    translation = tokenizer.decode(outputs[0], skip_special_tokens = True)
    model.translation = translation
    model.save()

#return the translated text
def find_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)
    translation = model.translation

    if translation is None:
        translation = "Processing . Check back later"

    return translation



