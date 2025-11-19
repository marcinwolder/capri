from transformers import MarianMTModel, MarianTokenizer, pipeline


def detect_language(text):
	"""Detect language of the text."""
	model_ckpt = 'papluca/xlm-roberta-base-language-detection'
	pipe = pipeline('text-classification', model=model_ckpt)
	return pipe(text, top_k=1, truncation=True)


def translate(text, src_lang, dst_lang='en'):
	"""Translate text from source language to destination language."""
	model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{dst_lang}'
	tokenizer = MarianTokenizer.from_pretrained(model_name)
	model = MarianMTModel.from_pretrained(model_name)

	tokenized_text = tokenizer(
		text, return_tensors='pt', padding=True, truncation=True, max_length=512
	)
	translated = model.generate(**tokenized_text)

	return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]


def _test(text):
	src_text = text
	lang = detect_language(src_text)
	translated_text = translate(src_text, src_lang=lang[0]['label'], dst_lang='en')
	print('Translated text:', translated_text)


# _test("Hola, ¿cómo estás?")
