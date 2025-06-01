import hashlib
import zlib
from Crypto.Hash import MD2, MD4

def calculate_hash(text: str, algorithm: str) -> str:
    if not text:
        return ""

    text_bytes = text.encode('utf-8')

    if algorithm == 'md2':
        return MD2.new(text_bytes).hexdigest()
    elif algorithm == 'md4':
        return MD4.new(text_bytes).hexdigest()
    elif algorithm == 'md5':
        return hashlib.md5(text_bytes).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(text_bytes).hexdigest()
    elif algorithm == 'sha224':
        return hashlib.sha224(text_bytes).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(text_bytes).hexdigest()
    elif algorithm == 'sha384':
        return hashlib.sha384(text_bytes).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(text_bytes).hexdigest()
    elif algorithm == 'shake128':
        return hashlib.shake_128(text_bytes).digest(32).hex()
    elif algorithm == 'shake256':
        return hashlib.shake_256(text_bytes).digest(64).hex()
    elif algorithm == 'blake2b':
        return hashlib.blake2b(text_bytes).hexdigest()
    elif algorithm == 'blake2s':
        return hashlib.blake2s(text_bytes).hexdigest()
    elif algorithm == 'crc32':
        return format(zlib.crc32(text_bytes) & 0xFFFFFFFF, '08x')
    else:
        return "Desteklenmeyen hash algoritması"