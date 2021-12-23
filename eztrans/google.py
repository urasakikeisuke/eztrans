"""google.py"""

import argparse
from typing import Optional

import pyperclip # type: ignore
from googletrans import Translator # type: ignore


def main(text: str, autocopy: bool):
    if text is None:
        text_ = pyperclip.paste()
        if text_ == "":
            raise ValueError(f"No translatable text found. Make sure to copy a valid text or to pass the text when calling the command.")
        text = text_

    translator: Translator = Translator()
    input_lang = translator.detect(text).lang

    if input_lang != "ja":
        output_text = translator.translate(text, src=input_lang, dest="ja").text
    else:
        output_text = translator.translate(text, src=input_lang, dest="en").text

    print(output_text, flush=True)

    if autocopy:
        pyperclip.copy(output_text)

        if pyperclip.paste() != output_text:
            print("\nFailed to copy output text to the clipboard")

def entory_point():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", type=str, default=None, help="Input text to be translated")
    parser.add_argument("-c", "--autocopy", action="store_true", help="Whether to use auto copy to clipboard")
    args = parser.parse_args()

    main(args.text, args.autocopy)