"""deepl.py"""

import os
import time
import warnings
from typing import Optional

warnings.filterwarnings("ignore")

from contextlib import redirect_stdout

import pyperclip
from fire import Fire
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

os.environ['WDM_LOG_LEVEL'] = '0'


def main(text: Optional[str] = None):
    options: Options = Options()
    options.add_argument('--lang=ja')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_argument('--disable-extensions')
    options.add_argument('--user-agent=hogehoge')                       
    options.add_argument('--proxy-bypass-list=*')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.page_load_strategy = 'eager'

    if text is None:
        text_ = pyperclip.paste()
        if text_ == "":
            raise ValueError(f"No translatable text found. Make sure to copy the valid text or to pass the text when calling the command.")
        text = text_

    cache_path = os.path.expanduser("~/.cache/eztrans")
    os.makedirs(cache_path, exist_ok=True)

    driver: webdriver.Chrome
    with redirect_stdout(open(os.devnull, "w")):
        driver = webdriver.Chrome(
            ChromeDriverManager(print_first_line=False,
                                path=cache_path).install(),
            options=options
        )

    try:
        driver.get("https://www.deepl.com/ja/translator")
        input_selector = driver.find_element_by_css_selector(".lmt__textarea.lmt__source_textarea.lmt__textarea_base_style")
        input_selector.send_keys(text)

        cnt: int = 0
        output_text: str = ""
        while output_text == "":
            output_selector: str = ".lmt__textarea.lmt__target_textarea.lmt__textarea_base_style"
            output_text = driver.find_element_by_css_selector(output_selector).get_property("value")
            time.sleep(1)
            cnt += 1

    except (NoSuchElementException, TimeoutException):
        raise RuntimeError(f"Oops! Something went wrong...")

    finally:
        driver.close()

    for i, char in enumerate(output_text):
        list(output_text)[i] = char.translate(str.maketrans({
            '\u3000': ' ',
            ' ': ' ',
            '　': ' ',
            '\t': '',
            '\r': '',
            '\x0c': '',
            '\x0b': '',
            '\xa0': '',
        }))

    print("".join(output_text), flush=True)

    pyperclip.copy(output_text)


if __name__ == "__main__":
    Fire(main)
