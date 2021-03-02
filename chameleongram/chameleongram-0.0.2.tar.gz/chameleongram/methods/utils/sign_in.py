from chameleongram.exceptions import RpcException, NeededSignUp, PhoneNumberInvalid
from chameleongram.raw import functions, types
from ..base import Base


class SignIn(Base):
    async def sign_in(self, phone_number: str = None):
        """Sign in with your account/bot."""

        if self.token:
            await self(
                functions.auth.ImportBotAuthorization(
                    api_id=self.api_id,
                    api_hash=self.api_hash,
                    bot_auth_token=self.token,
                )
            )
            return self
        else:
            while True:
                login_phone_number = (
                    (
                            phone_number
                            or self.phone_number
                            or input("Enter your phone number or bot token: ")
                    )
                        .strip()
                        .replace(" ", "")
                        .lstrip("+")
                )
                if login_phone_number:
                    try:
                        if ":" in login_phone_number:
                            await self(
                                functions.auth.ImportBotAuthorization(
                                    api_id=self.api_id,
                                    api_hash=self.api_hash,
                                    bot_auth_token=login_phone_number,
                                )
                            )
                            return self
                        else:
                            sent_code = await self(
                                functions.auth.SendCode(
                                    phone_number=login_phone_number,
                                    api_id=self.api_id,
                                    api_hash=self.api_hash,
                                    settings=types.CodeSettings(),
                                )
                            )
                    except RpcException as e:
                        if e.description == "PHONE_NUMBER_INVALID":
                            print("  - The phone number is invalid.\n")
                            if phone_number:
                                raise PhoneNumberInvalid(phone_number=phone_number)
                            continue
                        elif e.description == "ACCESS_TOKEN_EXPIRED":
                            print("  - Bot Token expired.\n")
                            continue
                        elif e.description == "PHONE_MIGRATE":
                            await self.stop()
                            await self.connect(dc_id=e.x)
                            return await self.sign_in(phone_number=login_phone_number)
                    break
            while True:
                phone_code = "".join(
                    x
                    for x in input("Enter the code you received: ").strip()
                    if x.isdecimal()
                )
                if phone_code:
                    try:
                        result = await self(
                            functions.auth.SignIn(
                                phone_number=login_phone_number,
                                phone_code_hash=sent_code.body.result.phone_code_hash,
                                phone_code=phone_code,
                            )
                        )
                        if isinstance(result.body.result, types.auth.Authorization):
                            self.show_message()
                            return self
                        else:
                            raise NeededSignUp(
                                phone_number=login_phone_number,
                                phone_code_hash=sent_code.body.result.phone_code_hash,
                            )
                    except RpcException as e:
                        if e.description == "PHONE_CODE_INVALID":
                            print("  - The code is invalid.\n")
                            continue
        return self
