class NeededSignUp(Exception):
    def __init__(self, phone_number: str, phone_code_hash: str):
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash

    def __str__(self):
        return f"The account doesn't exist, so you need to sign up."
