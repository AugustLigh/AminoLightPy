from time import time
from json import dumps
from hashlib import sha1
from typing import BinaryIO
from collections import OrderedDict
from requests import Session
from mimetypes import guess_type
from requests.adapters import HTTPAdapter

from .lib import signature, gen_deviceId
from .lib import CheckException

# add by August Light

api = "http://service.aminoapps.com/api/v1"
device_id = gen_deviceId()
cache = OrderedDict()
cache_len = 32

class AminoSession(Session):
    def __init__(self) -> None:
        super().__init__()
        
        self.headers.update({
            "NDCDEVICEID": device_id,
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Apple iPhone13,1 iOS v16.5 Main/3.19.0",
        }) 

        self.timeout = 5
        self.mount("http://", HTTPAdapter(max_retries=3))

    def request(self, method, url, *args, **kwargs):
        headers = kwargs.get("headers", {})
        data = kwargs.get("data", None)

        if method.lower() == "post":
            if "json" in kwargs and data is None:
                data = kwargs.get("json") or {}
                data["timestamp"] = int(time() * 1000)

                if not "login" in url:
                    data["uid"] = self.headers["AUID"]

                data = dumps(data)

                headers["Content-Type"] = "application/json"
                headers["NDC-MSG-SIG"] = signature(data)

            elif data is None:
                headers["Content-Type"] = "application/x-www-form-urlencoded"

        kwargs["headers"] = headers
        if data is not None:
            kwargs["data"] = data

        if not url.startswith(api):
            url = f"{api}{url}"

        kwargs.setdefault("timeout", self.timeout)
        
        response = super().request(method, url, *args, **kwargs)
           
        
        if not "api:statuscode" in response.text:
            CheckException('{"api:statuscode": 103}')

        if not response.ok:
            CheckException(response.text)

        return response


def upload_media(self, file: BinaryIO) -> str:
    """
    Upload file to the amino servers.

    **Parameters**
        - **file** : File to be uploaded.

    **Returns**
        - **Success** : Url of the file uploaded to the server.

        - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
    """
    if "http" in file:
        return file

    data = file.read()

    file_hash  = sha1(data).hexdigest()
    if file_hash in cache:
        return cache[file_hash]
        
    fileType = guess_type(file.name)[0]
        
    custom_headers = self.session.headers
    custom_headers["Content-Type"] = fileType

    response = self.session.post(
        url="/g/s/media/upload",
        data=data,
        headers=custom_headers,
        stream=True
    )

    cache[file_hash] = response.json()["mediaValue"]
    if len(cache) >= cache_len:
        cache.popitem(last=False)

    return cache[file_hash]
    
def upload_stiker(self, file: BinaryIO) -> str:
    data = file.read()

    fileType = guess_type(file.name)[0]
        
    custom_headers = self.session.headers
    custom_headers["Content-Type"] = fileType

    response = self.session.post(
        url="/g/s/media/upload/target/sticker",
        data=data,
        headers=custom_headers,
        stream=True
    )

    return response.json()["mediaValue"]

def upload_flag_image(self, comId: int, file: BinaryIO) -> str:
    """
    Upload image related to a report and return its link.
    
    **Parameters**
        - **com_id** : Community identifier.
        - **file** : Image file to upload.
        
    **Returns**
        - **Success** : Url of the uploaded image.
        
        - **Fail** : :meth:`Exceptions <AminoLightPy.lib.util.exceptions>`
    """
    data = file.read()
    
    fileType = guess_type(file.name)[0]
    
    custom_headers = self.session.headers
    custom_headers["Content-Type"] = fileType
    
    response = self.session.post(
        url=f"/x{comId}/s/media/upload/target/flag-image",
        data=data,
        headers=custom_headers,
        stream=True
    )
    
    return response.json()["mediaValue"]