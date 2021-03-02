class PhoneNumberInvalid(Exception):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def __str__(self):
        return f"The phone number you tried to use is invalid ({self.phone_number})."
