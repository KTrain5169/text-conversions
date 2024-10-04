import wave
import time
import struct
import os
import subprocess
import sys
import tempfile
import audioread
import soundfile as sf
from art import text2art
from collections import Counter
import random
import qrcode
import barcode
from barcode.writer import ImageWriter
import math
import numpy as np  # Add this import at the top of the file


class TextConverter:
    def __init__(self):
        self.history_folder = "conversion-history"
        self.qr_folder = os.path.join(self.history_folder, "qr_codes")
        self.barcode_folder = os.path.join(self.history_folder, "barcodes")
        os.makedirs(self.qr_folder, exist_ok=True)
        os.makedirs(self.barcode_folder, exist_ok=True)
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
            'braille': 'braille_history.txt',
            'barcode': 'barcode_history.txt',
            'morse_sound': 'morse_audio.mp3',
        }

    def save_result(self, result, mode):
        file_path = os.path.join(self.history_folder, self.history_files[mode])
        with open(file_path, 'a', encoding="utf-8") as f:
            f.write(f'\n{result}')
        return f"Result saved to {file_path}"

    def flipUD(self, text):
        flip_map = str.maketrans(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.,!?/\"'()[]{\}",
            "ɐqɔpǝɟɓɥᴉſʞlɯuodbɹsʇnʌʍxʎz∀ꓭƆꓷƎℲꓨHIſꓘ⅃WNOꓒΌꓤSꓕꓵΛMX⅄Z⇂ᘕԐત૨୧L8მ0·ˋ¡¿\„,)(][}/{"
        )
        return text.translate(flip_map)

    def reverse_text(self, text):
        return text[::-1]

    def text_flip(self, text):
        return self.flipUD(text)

    def enchant_text(self, text):
        enchant_dict = {
            'A': 'ᔑ', 'B': 'ʖ', 'C': 'ᓵ', 'D': '↸', 'E': 'ᒷ', 'F': '⎓',
            'G': '⊣', 'H': '⍑', 'I': '╎', 'J': '⋮', 'K': 'ꖌ', 'L': 'ꖎ',
            'M': 'ᒲ', 'N': 'リ', 'O': '𝙹', 'P': '!¡', 'Q': 'ᑑ', 'R': '∷',
            'S': 'ᓭ', 'T': 'ℸ', 'U': '⚍', 'V': '⍊', 'W': '∴', 'X': ' ̇/',
            'Y': '||', 'Z': 'Λ',
            'a': 'ᔑ', 'b': 'ʖ', 'c': 'ᓵ', 'd': '↸', 'e': 'ᒷ', 'f': '⎓',
            'g': '⊣', 'h': '⍑', 'i': '╎', 'j': '⋮', 'k': 'ꖌ', 'l': 'ꖎ',
            'm': 'ᒲ', 'n': 'リ', 'o': '𝙹', 'p': '!¡', 'q': 'ᑑ', 'r': '∷',
            's': 'ᓭ', 't': 'ℸ', 'u': '⚍', 'v': '⍊', 'w': '∴', 'x': ' ̇/',
            'y': '||', 'z': 'Λ'
        }

        return ''.join(enchant_dict.get(char, char) for char in text)

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
        words = text.split()
        translated_words = []
        vowels = "aeiouAEIOU"
        consonant_clusters = ["bl", "br", "ch", "cl", "cr", "dr", "fl", "fr",
                              "gl", "gr", "pl", "pr", "sc", "sh", "sk", "sl",
                              "sm", "sn", "sp", "st", "sw", "th", "tr", "tw",
                              "wh", "wr", "sch", "scr", "shr", "spl", "spr",
                              "squ", "str", "thr"]

        for word in words:
            if word[0].lower() in vowels:
                translated_words.append(word + "way")
            elif word.lower()[:3] in consonant_clusters:
                translated_words.append(word[3:] + word[:3] + "ay")
            elif word.lower()[:2] in consonant_clusters:
                translated_words.append(word[2:] + word[:2] + "ay")
            else:
                translated_words.append(word[1:] + word[0] + "ay")

        return " ".join(translated_words)

    def caesar_cipher(self, text, shift):
        encrypted = []
        for char in text:
            if char.isalpha():
                shift_amount = 65 if char.isupper() else 97
                encrypted.append(
                    chr((ord(char) - shift_amount + shift) % 26 + shift_amount))
            else:
                encrypted.append(char)
        return ''.join(encrypted)

    def ascii_art(self, text):
        return text2art(text)

    def border_text(self, text):
        return text2art(text, font='block')

    def zalgo_text(self, text):
        zalgo_chars = ['̍', '̎', '̄', '̅', '̿', '̑', '̆', '̐', '͒', '͗', '͑', '̇', '̈', '̊', '͂', '̓', '̈', '͊', '͋', '͌', '̃', '̂', '̌', '͐',
                       '̀', '́', '̋', '̏', '̒', '̓', '̔', '̽', '̉', 'ͣ', 'ͤ', 'ͥ', 'ͦ', 'ͧ', 'ͨ', 'ͩ', 'ͪ', 'ͫ', 'ͬ', 'ͭ', 'ͮ', 'ͯ', '̾', '͛', '͆', '̚']
        return ''.join(random.choice(zalgo_chars) + char for char in text)

    def morse_code(self, text):
        MORSE_CODE_DICT = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..',
            '1': '.----', '2': '..---', '3': '...--', '4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..',
            '9': '----.', '0': '-----',
            ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
            '-': '-....-', '(': '-.--.', ')': '-.--.-'
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

    def generate_code(self, text, code_type, filename=None):
        if code_type == 'qr':
            folder = self.qr_folder
            default_filename = "qr_code"
        elif code_type == 'barcode':
            folder = self.barcode_folder
            default_filename = "barcode"
        else:
            raise ValueError("Invalid code type. Must be 'qr' or 'barcode'.")

        if filename is None:
            filename = default_filename

        file_path = os.path.join(folder, f"{filename}.png")

        if code_type == 'qr':
            qr = qrcode.QRCode(
                version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img.save(file_path)
        elif code_type == 'barcode':
            EAN = barcode.get_barcode_class('code128')
            ean = EAN(text, writer=ImageWriter())
            ean.save(file_path.replace('.png', ''))

        return f"{code_type.upper()} code saved as {file_path}"

    def text_to_emoticons(self, text):
        emoticon_dict = {
            'hello': '👋', 'world': '🌍', 'love': '❤️', 'happy': '😊', 'sad': '😢',
            'laugh': '😂', 'smile': '😃', 'angry': '😠', 'cool': '😎', 'sun': '☀️',
            'moon': '🌙', 'star': '⭐', 'food': '🍔', 'drink': '🍹', 'music': '🎵',
            'book': '📚', 'computer': '💻', 'phone': '📱', 'car': '🚗', 'house': '🏠',
            'tree': '🌳', 'flower': '🌸', 'dog': '🐶', 'cat': '🐱', 'bird': '🐦',
            'fish': '🐠', 'heart': '❤️', 'fire': '🔥', 'water': '💧', 'earth': '🌎',
            'air': '💨', 'time': '⏰', 'money': '💰', 'work': '💼', 'sleep': '😴',
            'party': '🎉', 'gift': '🎁', 'camera': '📷', 'movie': '🎬', 'music': '🎵',
            'sport': '⚽', 'win': '🏆', 'yes': '👍', 'no': '👎', 'ok': '👌',
            'bye': '👋', 'please': '🙏', 'thanks': '🙏', 'sorry': '😔', 'wow': '😮',
            'omg': '😱', 'lol': '😂', 'idea': '💡', 'question': '❓', 'answer': '✅',
            'warning': '⚠️', 'stop': '🛑', 'go': '🚦', 'fast': '⚡', 'slow': '🐌',
            'up': '⬆️', 'down': '⬇️', 'left': '⬅️', 'right': '➡️', 'back': '🔙',
            'soon': '🔜', 'new': '🆕', 'free': '🆓', 'hot': '🔥', 'cold': '❄️',
            'big': '🐘', 'small': '🐜', 'loud': '📢', 'quiet': '🤫', 'good': '👍',
            'bad': '👎', 'sick': '🤒', 'healthy': '💪', 'smart': '🧠', 'crazy': '🤪',
            'king': '👑', 'queen': '👸', 'baby': '👶', 'ghost': '👻', 'alien': '👽',
            'robot': '🤖', 'rainbow': '🌈', 'unicorn': '🦄', 'pizza': '🍕',
            'beer': '🍺', 'wine': '🍷', 'coffee': '☕', 'tea': '🍵',
            'cake': '🎂', 'balloon': '🎈', 'rocket': '🚀', 'airplane': '✈️',
            'train': '🚂', 'boat': '⛵', 'beach': '🏖️', 'mountain': '⛰️',
            'camping': '⛺', 'snow': '❄️', 'rain': '🌧️', 'wind': '💨',
            'cloud': '☁️', 'thunder': '⚡', 'rainbow': '🌈', 'light': '💡',
            'dark': '🌑', 'city': '🏙️', 'village': '🏘️', 'island': '🏝️',
            'bridge': '🌉', 'building': '🏢', 'police': '👮',
            'firefighter': '👩‍🚒', 'doctor': '👩‍⚕️', 'nurse': '👩‍⚕️',
            'teacher': '👩‍🏫', 'student': '👨‍🎓', 'office': '🏢',
            'hospital': '🏥', 'school': '🏫', 'church': '⛪', 'bank': '🏦',
            'factory': '🏭', 'market': '🏪', 'restaurant': '🍽️',
            'coffee_shop': '☕', 'bicycle': '🚲', 'motorcycle': '🏍️',
            'bus': '🚌', 'taxi': '🚕', 'subway': '🚇', 'truck': '🚚',
            'helicopter': '🚁', 'passport': '🛂', 'map': '🗺️', 'moneybag': '💰',
            'shopping_cart': '🛒', 'gift_box': '🎁', 'crown': '👑',
            'diamond': '💎', 'key': '🔑', 'lock': '🔒', 'pen': '🖊️',
            'pencil': '✏️', 'paintbrush': '🖌️', 'globe': '🌐', 'clock': '🕰️',
            'calendar': '📅', 'trophy': '🏆', 'medal': '🥇', 'first_place': '🥇',
            'second_place': '🥈', 'third_place': '🥉', 'money_with_wings': '💸',
            'wallet': '👛', 'credit_card': '💳', 'clothes': '👗', 'shoes': '👠',
            'watch': '⌚', 'ring': '💍', 'glasses': '👓', 'sunglasses': '🕶️',
            'hat': '🎩', 'tshirt': '👕', 'pants': '👖', 'dress': '👗',
            'coat': '🧥', 'handbag': '👜', 'scarf': '🧣', 'gloves': '🧤',
            'sock': '🧦', 'boots': '👢', 'shirt': '👔', 'necktie': '👔',
            'jacket': '🧥', 'sunhat': '👒', 'umbrella': '☂️', 'briefcase': '💼',
            'shopping_bag': '🛍️', 'hammer': '🔨', 'wrench': '🔧',
            'screwdriver': '🪛', 'saw': '🪚', 'axe': '🪓', 'knife': '🔪',
            'syringe': '💉', 'pill': '💊', 'stethoscope': '🩺',
            'test_tube': '🧪', 'microscope': '🔬', 'telescope': '🔭',
            'bulb': '💡', 'battery': '🔋', 'plug': '🔌', 'satellite': '🛰️',
            'antennas': '📡', 'radio': '📻', 'tv': '📺', 'headphones': '🎧',
            'laptop': '💻', 'keyboard': '⌨️', 'mouse': '🖱️', 'printer': '🖨️',
            'camera': '📷', 'phone': '📱', 'tablet': '📱', 'megaphone': '📣',
            'microphone': '🎤', 'speaker': '🔊', 'guitar': '🎸', 'violin': '🎻',
            'drum': '🥁', 'piano': '🎹', 'trumpet': '🎺', 'saxophone': '🎷',
            'speaker': '🔊', 'mute': '🔇', 'light_bulb': '💡',
            'electric_plug': '🔌', 'fireworks': '🎆', 'confetti': '🎊',
            'skull': '💀', 'nail_polish': '💅', 'lipstick': '💄',
            'chocolate': '🍫', 'donut': '🍩', 'ice_cream': '🍦',
            'hamburger': '🍔', 'fries': '🍟', 'spaghetti': '🍝', 'sushi': '🍣',
            'taco': '🌮', 'burrito': '🌯', 'baguette': '🥖', 'bread': '🍞',
            'cheese': '🧀', 'egg': '🥚', 'bacon': '🥓', 'fried_egg': '🍳',
            'pancakes': '🥞', 'butter': '🧈', 'cooking': '🍳', 'chicken': '🍗',
            'meat_on_bone': '🍖', 'salad': '🥗', 'tomato': '🍅',
            'avocado': '🥑', 'broccoli': '🥦', 'mushroom': '🍄', 'carrot': '🥕',
            'potato': '🥔', 'nerd': '🤓', '?': '❓', '!': '❗'
        }

        words = text.split()
        return ' '.join(emoticon_dict.get(word.lower(), word) for word in words)

    def nerd_mode(self, text):
        word_count = len(text.split())
        char_count = len(text)
        char_frequency = Counter(text)
        return {
            "Text": text,
            "Word Count": word_count,
            "Character Count": char_count,
            "Character Frequency": dict(char_frequency),
            "Nerd emoji": "🤓"
        }

    def text_to_braille(self, text):
        braille_dict = {
            'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
            'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
            'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
            's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
            'y': '⠽', 'z': '⠵',
            '0': '⠼⠚', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑',
            '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊',
            ' ': ' ', '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', "'": '⠄',
            '"': '⠐⠂', '-': '⠤', '@': '⠜'
        }
        return ''.join(braille_dict.get(char.lower(), char) for char in text)

    def pigpen_mode(self, text):
        pigpen_trans = str.maketrans(
            'abcdefghijklmnopqrstuvwxyz',
            '⍁⍂⍃⍄⍅⍆⍇⍈⍉⍊⍋⍌⍍⍎⍏⍐⍑⍒⍓⍔⍕⍖⍗⍘⍙⍚'
        )
        return text.translate(pigpen_trans)

    def morse_code_audio(self, text):
        MORSE_CODE_DICT = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.'
        }

        def generate_sine_wave(freq, duration, volume=1.0, sample_rate=44100):
            num_samples = int(sample_rate * duration)
            samples = [int(volume * 32767 * math.sin(2 * math.pi * freq * t / sample_rate))
                       for t in range(num_samples)]
            return samples

        dot_duration = 0.1
        dash_duration = dot_duration * 3
        freq = 800

        dot = generate_sine_wave(freq, dot_duration)
        dash = generate_sine_wave(freq, dash_duration)
        short_gap = [0] * int(44100 * dot_duration)
        medium_gap = [0] * int(44100 * dash_duration)
        long_gap = [0] * int(44100 * dot_duration * 7)

        morse_audio = []
        for char in text.upper():
            if char == ' ':
                morse_audio.extend(long_gap)
            elif char in MORSE_CODE_DICT:
                for symbol in MORSE_CODE_DICT[char]:
                    morse_audio.extend(dot if symbol == '.' else dash)
                    morse_audio.extend(short_gap)
                morse_audio.extend(medium_gap)

        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            temp_wav_path = temp_wav.name
            with wave.open(temp_wav_path, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
                wav_file.writeframes(struct.pack(
                    '<' + 'h' * len(morse_audio), *morse_audio))

        # Convert WAV to MP3
        output_file = os.path.join(
            self.history_folder, self.history_files['morse_sound'])
        with audioread.audio_open(temp_wav_path) as audio_file:
            data = b''.join(audio_file.read_data())
            data_array = np.frombuffer(data, dtype=np.int16)
            data_array = data_array.reshape(-1, 1)  # Reshape to 2D array
            sf.write(output_file, data_array, audio_file.samplerate, format='mp3')

        # Clean up the temporary WAV file
        os.unlink(temp_wav_path)

        # Play the audio using the system's default player
        if sys.platform == 'win32':  # Windows
            os.startfile(output_file)
        elif sys.platform == 'darwin':  # macOS
            subprocess.call(['open', output_file])
        else:  # Linux and other Unix-like
            subprocess.call(['xdg-open', output_file])

        print(f"Playing Morse code audio for: {text}")
        input("Press Enter when you're done listening...")

        return output_file
