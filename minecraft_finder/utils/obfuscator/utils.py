import base64
from typing import Optional

from loguru import logger


class ObfuscatorUtils:
    def __init__(self, key: str) -> None:
        self.key: str = key

    @logger.catch
    def obfuscate(self, text: str) -> str:
        """
        Obfuscate the given text using XOR with the key and encode it to base64.
        :param text: Text to obfuscate
        :return: Obfuscated text
        """
        try:
            obfuscated: str = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, self.key * len(text)))
            return base64.urlsafe_b64encode(obfuscated.encode()).decode()

        except Exception as e:
            logger.warning(f'Error obfuscating text: {e}')
            return text

    @logger.catch
    def deobfuscate(self, obfuscated_text: str) -> Optional[str]:
        """
        Deobfuscate the given obfuscated text using XOR with the key and decode it from base64.
        :param obfuscated_text: Obfuscated texst to deobfuscate
        :return: Deobfuscated text
        """
        try:
            decoded: bytes = base64.urlsafe_b64decode(obfuscated_text.encode()).decode()
            return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(decoded, self.key * len(decoded)))

        except Exception as e:
            logger.warning(f'Error deobfuscating text: {e}')
            return None
