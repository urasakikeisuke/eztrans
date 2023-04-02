"""deepl.py"""

import argparse
import os

import pyperclip  # type: ignore
from deepl.translator import Translator
from deepl.exceptions import DeepLException
from googletrans import LANGUAGES, Translator as gTranslator
from rich.console import Console
from rich.columns import Columns
from rich.progress_bar import ProgressBar


TOKEN = os.getenv("DEEPL_API_TOKEN")
if TOKEN is None:
    raise RuntimeError("The environment variable \"DEEPL_API_TOKEN\" is not set")


def main(text: str, autocopy: bool, verbose: bool, c: Console):
    try:
        d_translator = Translator(TOKEN)
    except DeepLException:
        c.print_exception()

    usage = d_translator.get_usage()
    if usage.any_limit_reached:
        raise DeepLException("The translation usage of this API has already reached its limit. Aborting...")

    if text is None:
        text_ = pyperclip.paste()
        if text_ == "":
            raise ValueError(
                f"No translatable text found. Make sure to copy a valid text or to pass the text when calling the command.")
        text = text_

    if verbose:
        c.print()
        c.print(text, justify="full")
        c.print()

    g_translator = gTranslator()
    source_lang = g_translator.detect(text)
    if source_lang.lang == "ja":
        target_lang = "en"
    else:
        target_lang = "ja"

    if verbose:
        c.rule(f"Translating {LANGUAGES[source_lang.lang]} → {LANGUAGES[target_lang]}")

    if target_lang == "en":
        target_lang = "EN-US"

    try:
        output_text = d_translator.translate_text(
            text, source_lang=source_lang.lang.upper(), target_lang=target_lang.upper())
    except DeepLException:
        c.print_exception(width=c.width)

    if verbose:
        c.print()
    c.print(output_text, justify="full")
    if verbose:
        c.print()

    if autocopy:
        pyperclip.copy(output_text)
        if pyperclip.paste() != output_text:
            c.print("\nFailed to copy output text to the clipboard")

    if verbose:
        usage = d_translator.get_usage()
        limit = usage.character.limit
        count = usage.character.count
        style = "bar.complete" if (count / limit) > 0.8 else "bright_green"
        columns = Columns([
            "[bright_black]API usage",
            ProgressBar(total=limit, completed=count, width=c.width // 3, complete_style=style),
            f"[bright_magenta]{count:,} [bright_black]of [magenta]{limit:,}",
            f"{count / limit * 100.:.1f}[bright_black]%"
        ], padding=(0, 3), align="left")
        c.print(columns, no_wrap=True)


def entory_point():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", type=str, default=None, help="Input text to be translated")
    parser.add_argument("-c", "--autocopy", action="store_true", help="Whether to use auto copy to clipboard")
    parser.add_argument("-v", "--verbose", action="store_true", help="Whether to print verbose output")
    args = parser.parse_args()

    c = Console()

    try:
        main(args.text, args.autocopy, args.verbose, c)
    except:
        c.print_exception()
