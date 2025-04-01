from time import time, sleep
from json import dumps, loads
from hashlib import sha1
from typing import BinaryIO, Optional, Dict, Any, Union
from collections import OrderedDict
from requests import Session, Response
from mimetypes import guess_type
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from functools import lru_cache
from threading import RLock
import logging

from .lib import signature, gen_deviceId
from .lib import CheckException

from requests.exceptions import (
    ReadTimeout,
    ConnectTimeout, 
    ConnectionError,
)

# add by August Light

api = "http://service.aminoapps.com/api/v1"
device_id = gen_deviceId()
cache = OrderedDict()
cache_len = 32
_cache_lock = RLock()


class TTLCache:
    def __init__(self, max_size=100, ttl=60):
        self._cache = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl
        self._lock = RLock()
    
    def get(self, key):
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time() - timestamp <= self._ttl:
                    # Updating the position in OrderedDict (LRU)
                    self._cache.move_to_end(key)
                    return value
                else:
                    del self._cache[key]
        return None
    
    def set(self, key, value):
        with self._lock:
            self._cache[key] = (value, time())
            self._cache.move_to_end(key)
            # Clearing the cache if the size is exceeded
            if len(self._cache) > self._max_size:
                self._cache.popitem(last=False)


_request_cache = TTLCache(max_size=100, ttl=30)  # 30 second TTL

class AminoSession(Session):
    def __init__(self) -> None:
        super().__init__()
        
        self.headers.update({
            "NDCDEVICEID": device_id,
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Apple iPhone13,1 iOS v16.5 Main/3.19.0",
        }) 


        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
            backoff_factor=0.5,
            respect_retry_after_header=True
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy, 
            pool_connections=10,
            pool_maxsize=20
        )
        
        self.mount("http://", adapter)
        
        self.timeout = 5
        
        self._common_headers = {
            "Content-Type": "application/json",
        }
        
        self.use_cache = True
    
    def _prepare_data(self, data, url):
        """Streamlined data preparation for query"""
        if isinstance(data, dict):

            if "timestamp" not in data:
                data["timestamp"] = int(time() * 1000)
            
            if not "login" in url and "AUID" in self.headers:
                data["uid"] = self.headers["AUID"]
        
        return data
    
    def _get_cache_key(self, method, url, params=None):
        """Generates a unique cache key for the request"""
        if method.upper() != "GET" or not self.use_cache:
            return None
        
        return f"{method}:{url}:{str(params) if params else ''}"
    
    def request(self, method, url, *args, **kwargs):
        headers = {**kwargs.get("headers", {})}
        data = kwargs.get("data", None)
        json_data = kwargs.get("json", None)
        
        cache_key = self._get_cache_key(method, url, kwargs.get("params"))
        if cache_key:
            cached_response = _request_cache.get(cache_key)
            if cached_response:
                return cached_response
        
        if method.lower() == "post":
            if json_data is not None and data is None:
                prepared_data = self._prepare_data(json_data, url)
                data = dumps(prepared_data)
                
                headers["Content-Type"] = "application/json"
                headers["NDC-MSG-SIG"] = signature(data)
                
                del kwargs["json"]
                
            elif data is None:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        kwargs["headers"] = headers
        if data is not None:
            kwargs["data"] = data
        
        if not url.startswith(api):
            url = f"{api}{url}"
        
        kwargs.setdefault("timeout", self.timeout)
        

        response = None
        max_retries = 2
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                response = super().request(method, url, *args, **kwargs)
                break
            except (ReadTimeout, ConnectTimeout, ConnectionError):
                retry_count += 1
                if retry_count > max_retries:
                    raise
                
                sleep_time = 0.3 * (2 ** retry_count)
                sleep(sleep_time)
        
        # Проверяем код ответа
        if not response.ok:
            CheckException(response.text)
        

        if cache_key:
            _request_cache.set(cache_key, response)
        
        return response
    

def upload_media(self, file: BinaryIO) -> str:
    """
    Upload file to the amino servers.

    **Parameters**
        - **file** : File to be uploaded.

    **Returns**
        - **Success** : Url of the file uploaded to the server.

        - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
    """
    data = file.read()
    file_hash = sha1(data).hexdigest()
    
    with _cache_lock:
        if file_hash in cache:
            return cache[file_hash]
    
    fileType = guess_type(file.name)[0] or "application/octet-stream"
    
    custom_headers = self.session.headers.copy()
    custom_headers["Content-Type"] = fileType
    
    response = self.session.post(
        url="/g/s/media/upload",
        data=data,
        headers=custom_headers,
        stream=True
    )
    
    media_value = response.json()["mediaValue"]
    
    # Потокобезопасно обновляем кэш
    with _cache_lock:
        cache[file_hash] = media_value
        if len(cache) >= cache_len:
            cache.popitem(last=False)
    
    return media_value

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
        
        - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
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