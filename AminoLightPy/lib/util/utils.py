import os
import json
import platform
import tempfile
from pathlib import Path
from time import time

import warnings

def deprecated(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class CacheManager:
    def __init__(self, app_name="AminoLightPy"):
        """Initialize the cache manager for the specified application.
        
        Args:
            app_name: The name of the application for cache identification
        """
        self.app_name = app_name
        self.cache_dir = self._get_cache_dir()
        self.sids_dir = self.cache_dir / "sids"
        
        self._ensure_dirs_exist()
    
    def _get_cache_dir(self) -> Path:
        """Determine the appropriate cache directory based on the platform.
        
        Returns:
            Path: The path to the cache directory
        """
        system = platform.system()
        
        try:
            if system == "Windows":
                # Windows: %LOCALAPPDATA%\app_name\cache or %APPDATA%\app_name\cache
                local_app_data = os.environ.get("LOCALAPPDATA")
                if local_app_data and os.path.exists(local_app_data):
                    return Path(local_app_data) / self.app_name / "cache"
                
                app_data = os.environ.get("APPDATA")
                if app_data and os.path.exists(app_data):
                    return Path(app_data) / self.app_name / "cache"
            
            elif system == "Darwin":  # macOS
                # macOS: ~/Library/Caches/app_name
                library_path = Path.home() / "Library" / "Caches"
                if library_path.exists():
                    return library_path / self.app_name
            
            elif system == "Linux" or system == "FreeBSD":
                # Linux/BSD: ~/.cache/app_name or $XDG_CACHE_HOME/app_name
                xdg_cache_home = os.environ.get("XDG_CACHE_HOME")
                if xdg_cache_home and Path(xdg_cache_home).exists():
                    return Path(xdg_cache_home) / self.app_name
                
                user_cache = Path.home() / ".cache"
                if user_cache.exists():
                    return user_cache / self.app_name
        
        except (TypeError, ValueError, OSError):
            # Fall through to the default case
            pass
            
        # Fallback to temporary directory if standard locations aren't available
        return Path(tempfile.gettempdir()) / self.app_name
    
    def _ensure_dirs_exist(self):
        """Create the necessary directories if they don't exist."""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.sids_dir.mkdir(exist_ok=True)
        except (OSError, IOError) as e:
            print(f"Warning: Failed to create cache directories: {e}")
    
    def _sanitize_filename(self, filename):
        """Sanitize the filename to ensure it's valid across platforms.
        
        Args:
            filename: The original filename
            
        Returns:
            str: A sanitized filename
        """
        # Replace potentially problematic characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def save_sid(self, login, secret):
        """Save SID for the specified login.
        
        Args:
            login: User login (email/phone)
            secret: SID to store
        """
        try:
            safe_login = self._sanitize_filename(login)
            filepath = self.sids_dir / f"{safe_login}_sid.json"
            
            with open(filepath, "w") as f:
                json.dump({"sid": secret, "time": time()}, f)
        except (OSError, IOError, TypeError) as e:
            print(f"Warning: Failed to save SID: {e}")
    
    def get_sid(self, login):
        """Get SID for the specified login.
        
        Args:
            login: User login (email/phone)
            
        Returns:
            dict: Dictionary with SID and creation time, or None if not found
        """
        try:
            safe_login = self._sanitize_filename(login)
            filepath = self.sids_dir / f"{safe_login}_sid.json"
            
            if not filepath.exists():
                return None
            
            with open(filepath) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, OSError, IOError) as e:
            print(f"Warning: Failed to read SID: {e}")
            return None
    
    def remove_sid(self, login):
        """Remove SID for the specified login.
        
        Args:
            login: User login (email/phone)
            
        Returns:
            bool: True if removal was successful, False otherwise
        """
        try:
            safe_login = self._sanitize_filename(login)
            filepath = self.sids_dir / f"{safe_login}_sid.json"
            
            if filepath.exists():
                os.remove(filepath)
                return True
            return False
        except (OSError, IOError) as e:
            print(f"Warning: Failed to remove SID: {e}")
            return False
    
    def sid_exists(self, login):
        """Check if SID exists for the specified login.
        
        Args:
            login: User login (email/phone)
            
        Returns:
            bool: True if SID exists, False otherwise
        """
        try:
            safe_login = self._sanitize_filename(login)
            filepath = self.sids_dir / f"{safe_login}_sid.json"
            return filepath.exists()
        except (OSError, IOError):
            return False