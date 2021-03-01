from cryptography.fernet import Fernet
import base64


class EncdecError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class EncDec:
    is_debug = False
    cipher_suite = None

    def __init__(self, encryption_key=None, is_debug=False):
        self.is_debug = is_debug
        self.encryption_key = encryption_key
    
    def generate_key(self):
        # Use generate_key() method from Fernet
        # to generate a secure key.
        self.encryption_key = Fernet.generate_key()
        return self.encryption_key
    
    def encrypt(self, content):
        # Uses Fernet and the provided encrption key to encrypt
        # data. Returns None if an error occurs and if is_debug is False
        # otherwise EncdecError exception is raised if an error occured.
        try:
            cipher_suite = Fernet(self.encryption_key)
            encrypted_content = cipher_suite.encrypt(str(content).encode('ascii'))
            encrypted_content = base64.urlsafe_b64encode(encrypted_content).decode('ascii') 
            return encrypted_content
        except Exception as e:
            if self.is_debug:
                raise EncdecError(str(e))
            else:
                return None
    
    def decrypt(self, content):
        # Uses Fernet and the provided encrption key to decrypt
        # data. Returns None if an error occurs and if is_debug is False
        # otherwise EncdecError exception is raised if an error occured.
        try:
            cipher_suite = Fernet(self.encryption_key)
            return cipher_suite.decrypt(base64.urlsafe_b64decode(content)).decode("ascii")
        except Exception as e:
            if self.is_debug:
                raise EncdecError(str(e))
            else:
                return None