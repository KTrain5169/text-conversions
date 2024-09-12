import random
from art import text2art
import sys
import time
import qrcode
from collections import Counter
import os


class TextConverter:
    def __init__(self):
        self.history_folder = "conversion-history"
        os.makedirs(self.history_folder, exist_ok=True)
        self.history_files = {
            'reverse': 'reverse_history.txt',
            'flip': 'flip_history.txt',
            'enchant': 'enchant_history.txt',
            'case': 'case_history.txt',
            'leetspeak': 'leetspeak_history.txt',
            'scramble': 'scramble_history.txt',
            'piglatin': 'piglatin_history.txt',
            'caesar': 'caesar_history.txt',
            'ascii': 'ascii_history.txt',
            'border': 'border_history.txt',
            'zalgo': 'zalgo_history.txt',
            'morse': 'morse_history.txt',
            'binary': 'binary_history.txt',
            'shadow': 'shadow_history.txt',
            'emoticons': 'emoticons_history.txt',
        }

    def save_result(self, result, mode):
        file_path = os.path.join(self.history_folder, self.history_files[mode])
        with open(file_path, 'a', encoding="utf-8") as f:
            f.write(f'\n{result}')
        return f"Result saved to {file_path}"

    def flipUD(self, text):
        flip_map = str.maketrans(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.,!?\"'()[]{}",
            "ɐqɔpǝɟɓɥᴉſʞlɯuodbɹsʇnʌʍxʎz∀ꓭƆꓷƎℲꓨHIſꓘ⅃WNOꓒΌꓤSꓕꓵΛM⅄Z⇂ᘕԐત૨୧L8მ0·ˋ¡¿\\„,)(][}{"
        )
        return text.translate(flip_map)[::-1]

    def reverse_text(self, text):
        return text[::-1]

    def text_flip(self, text):
        return self.flipUD(text)

    def enchant_text(self, text):
        enchanted_text = str.maketrans(
            "abcdefghijklmnoqrstuvwzABCDEFGHIJKLMNOQRSTUVWZ1234567890.,!?\"'()[]{}",
            "ᔑʖᓵ↸ᒷ⎓⊣⍑╎⋮ꖌꖎᒲリ𝙹ᑑ∷ᓭℸ⚍⍊∴Λᔑʖᓵ↸ᒷ⎓⊣⍑╎⋮ꖌꖎᒲリ𝙹ᑑ∷ᓭℸ⚍⍊∴Λ1234567890.,!?\"'()[]{}"
        )
        enchanted_text = text.translate(enchanted_text)
        return str(enchanted_text).replace('p', '!¡').replace('P', '!¡').replace('y', '||').replace('Y', '||').replace('x', ' ̇/').replace('X', ' ̇/')

    def case_switch(self, text, case='upper'):
        if case.lower() == 'upper':
            return text.upper()
        elif case.lower() == 'lower':
            return text.lower()
        else:
            raise ValueError("Case must be 'upper' or 'lower'")

    def leetspeak(self, text):
        leet_dict = {'a': '4', 'e': '3', 'l': '1', 'o': '0', 't': '7'}
        return ''.join(leet_dict.get(char, char) for char in text.lower())

    def scramble_text(self, text):
        return ''.join(random.sample(text, len(text)))

    def piglatin(self, text):
        vowels = "aeiouAEIOU"
        if text[0] in vowels:
            return text + "way"
        else:
            return text[1:] + text[0] + "ay"

    def caesar_cipher(self, text, shift):
        encrypted = []
        for char in text:
            if char.isalpha():
                shift_amount = 65 if char.isupper() else 97
                encrypted.append(chr((ord(char) - shift_amount + shift) % 26 + shift_amount))
            else:
                encrypted.append(char)
        return ''.join(encrypted)

    def ascii_art(self, text):
        return text2art(text)

    def border_text(self, text):
        return text2art(text, font='block')

    def zalgo_text(self, text):
        zalgo_chars = ['̍', '̎', '̄', '̅', '̿', '̑', '̆', '̐', '͒', '͗', '͑', '̇', '̈', '̊', '͂', '̓', '̈', '͊', '͋', '͌', '̃', '̂', '̌', '͐', '̀', '́', '̋', '̏', '̒', '̓', '̔', '̽', '̉', 'ͣ', 'ͤ', 'ͥ', 'ͦ', 'ͧ', 'ͨ', 'ͩ', 'ͪ', 'ͫ', 'ͬ', 'ͭ', 'ͮ', 'ͯ', '̾', '͛', '͆', '̚']
        return ''.join(random.choice(zalgo_chars) + char for char in text)

    def morse_code(self, text):
        MORSE_CODE_DICT = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
            '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
            ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
        }
        return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

    def binary_text(self, text):
        return ' '.join(format(ord(char), '08b') for char in text)

    def text_shadow(self, text, offset=1):
        shadow = '\n'.join(' ' * offset + line for line in text.split('\n'))
        return f"{text}\n{shadow}"

    def scroll_text(self, text, delay=0.1):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def qr_code(self, text, filename):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        file_path = os.path.join(self.history_folder, f"{filename}.png")
        img.save(file_path)
        return f"QR code saved as {file_path}"

    def text_to_emoticons(self, text):
        emoticon_dict = {'hello': '👋', 'world': '🌍'}
        words = text.split()
        return ' '.join(emoticon_dict.get(word.lower(), word) for word in words)

    def nerd_mode(self, text):
        word_count = len(text.split())
        char_count = len(text)
        char_frequency = Counter(text)
        return {
            "Word Count": word_count,
            "Character Count": char_count,
            "Character Frequency": dict(char_frequency)
        }
