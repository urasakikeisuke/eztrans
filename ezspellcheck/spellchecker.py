"""spellchecker.py"""

import argparse
from typing import Optional

import pyperclip # type: ignore
import numpy
from autocorrect import Speller # type: ignore


def softmax(array: numpy.ndarray) -> numpy.ndarray:
    array = (array - array.min()) / (array.max() - array.min())
    x = numpy.exp(array - numpy.max(array))
    sum_x = numpy.sum(x)

    return x / sum_x * 100.


def main_(src: str, quiet: bool) -> str:
    for i, char in enumerate(src):
        list(src)[i] = char.translate(str.maketrans({
            '\u3000': ' ',
            ' ': ' ',
            '　': ' ',
            '\t': '',
            '\r': '',
            '\x0c': '',
            '\x0b': '',
            '\xa0': '',
        }))
    src = "".join(src)
    src = src.split(" ")

    max_length = 0
    for word in src:
        if len(word) > max_length:
            max_length = len(word)

    speller = Speller()

    target = []
    for word in src:
        checked = speller(word)

        if not quiet:
            print(f"{word:{max_length}s} -> ", end="", flush=True)

            if word == checked:
                print(f"\x1b[92;1m{checked}\x1b[0m")
            else:
                candidates = speller.get_candidates(word)
                
                if len(candidates) > 1:
                    probs = []
                    candidates_ = []
                    for prob, candidate in candidates:
                        probs.append(prob)
                        candidates_.append(candidate)
                    
                    candidates = sorted(zip(probs, candidates_), reverse=True)
                    probs, candidates_ = zip(*candidates)

                    probs = softmax(numpy.array(probs, dtype=numpy.float64))

                    for prob, candidate in zip(probs, candidates_):
                        print(f"\x1b[91;1m{candidate} ({prob:.1f}%) \x1b[0m", end="", flush=True)
                    
                    print()
                
                else:
                    print(f"\x1b[91;1m{candidates[0][1]} (100.0%) \x1b[0m", flush=True)

        target.append(speller(word))

    if not quiet:
        print()

    return " ".join(target)


def main(text: str, autocopy: bool, quiet: bool):
    if text is None:
        text_ = pyperclip.paste()
        if text_ == "":
            raise ValueError(f"No translatable text found. Make sure to copy a valid text or to pass the text when calling the command.")
        text = text_

    output_text = main_(text, quiet)

    print(output_text, flush=True)

    if autocopy:
        pyperclip.copy(output_text)

        if pyperclip.paste() != output_text:
            print("\nFailed to copy output text to the clipboard")

def entory_point():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", type=str, default=None, help="Input text to be translated")
    parser.add_argument("-c", "--autocopy", action="store_true", help="Whether to use auto copy to clipboard")
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress verbose message")
    args = parser.parse_args()

    main(args.text, args.autocopy, args.quiet)