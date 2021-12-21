"""google.py"""

from typing import Optional

import pyperclip
from fire import Fire
from googletrans import Translator


def main(text: Optional[str] = None):
    if text is None:
        text_ = pyperclip.paste()
        if text_ == "":
            raise ValueError(f"No translatable text found. Make sure to copy the valid text or to pass the text when calling the command.")
        text = text_

    translator: Translator = Translator()
    input_lang = translator.detect(text).lang

    if input_lang != "ja":
        output_text = translator.translate(text, src=input_lang, dest="ja").text
    else:
        output_text = translator.translate(text, src=input_lang, dest="en").text

    print(output_text, flush=True)

    pyperclip.copy(output_text)

if __name__ == "__main__":
    Fire(main)
