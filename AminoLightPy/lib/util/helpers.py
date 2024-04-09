from hmac import new
from json import loads
from os import urandom
from typing import Union
from hashlib import sha1
from base64 import b64decode, b64encode

PREFIX = b'\x19'
SIG_KEY = b'\xdf\xa5\xed\x19-\xdan\x88\xa1/\xe1!0\xdcb\x06\xb1%\x1eD'
DEVICE_KEY = b"\xe70\x9e\xcc\tS\xc6\xfa`\x00['e\xf9\x9d\xbb\xc9e\xc8\xe9"

def gen_deviceId(data: bytes = None) -> str:
    if isinstance(data, str): data = bytes(data, 'utf-8')
    identifier = PREFIX + (data or urandom(20))
    mac = new(DEVICE_KEY, identifier, sha1)
    return f"{identifier.hex()}{mac.hexdigest()}".upper()

def signature(data: Union[str, bytes]) -> str:
    data = data if isinstance(data, bytes) else data.encode("utf-8")
    return b64encode(PREFIX + new(SIG_KEY, data, sha1).digest()).decode("utf-8")

def update_deviceId(device: str) -> str:
    return gen_deviceId(bytes.fromhex(device[2:42]))

def self_deviceId(email: str) -> str:
    hash = sha1(email.encode()).digest()
    return gen_deviceId(hash)

def decode_sid(sid: str) -> dict:
    sid = sid.replace("-", "+").replace("_", "/")
    sid += "=" * (-len(sid) % 4)
    decoded_bytes = b64decode(sid.encode())
    return loads(decoded_bytes[1:-20].decode())

def sid_to_uid(SID: str) -> str: return decode_sid(SID)["2"]

def sid_to_ip_address(SID: str) -> str: return decode_sid(SID)["4"]