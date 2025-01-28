import sys
import os
import json
import base64
from typing import Optional

import requests
from requests.exceptions import HTTPError
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

OBFUSCATOR_KEY: Optional[str] = os.getenv('OBFUSCATOR_KEY')


class ObfuscatorUtils:
    def __init__(self, key: str) -> None:
        self.key: str = key

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


class Client:
    def __init__(self) -> None:
        self.endpoint: str = 'http://127.0.0.1:8000/finder/username'
        self.obfuscator: ObfuscatorUtils = ObfuscatorUtils(key=OBFUSCATOR_KEY)
        
    def get(self, username: str) -> Optional[str]:
        """
        Sends a GET request to the API to retrieve data for the given username.
        If successful, deobfuscates the result and returns it.
        
        :param username: The username to search for.
        :return: Deobfuscated text if successful, otherwise `None`.
        """
        try:
            r: requests.Response = requests.get(f'{self.endpoint}/{username}')
            
            if r.status_code != 200:
                print(f'Status code is not 200 - {r.status_code} - {r.text}')
                raise HTTPError('Status code')
            
        except Exception as e:
            print(f'Error in requests: {e}')
            return None
        
        response: dict = json.loads(r.text)
        print(self.obfuscator.deobfuscate(response['result']))


if __name__ == '__main__':
    if OBFUSCATOR_KEY is None:
        print('Invalid OBFUSCATOR_KEY value in .env!')
        sys.exit(1)
        
    client: Client = Client()
    
    if len(sys.argv) <= 1:
        print('Usage: python client.py <username>')
        sys.exit(1)
        
    client.get(username=sys.argv[1])
