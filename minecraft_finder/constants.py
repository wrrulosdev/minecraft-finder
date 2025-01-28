import os 
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


class ObfuscatorConstants:
    KEY: Optional[str] = os.getenv('OBFUSCATOR_KEY')
    