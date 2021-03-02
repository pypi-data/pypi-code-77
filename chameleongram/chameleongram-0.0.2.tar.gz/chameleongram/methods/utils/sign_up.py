from chameleongram.exceptions import RpcException
from chameleongram.raw import functions
from ..base import Base


class SignUp(Base):
    async def sign_up(self, phone_number: str, phone_code_hash: str):
        """Sign up with your account."""

        while True:
            print("\nSignup:")
            while not (
                    first_name := input("  - Insert your first name: ").strip()[:64]
            ):
                continue
            last_name = input(
                "  - Insert your last name (leave empty for no one): "
            ).strip()[:64]
            try:
                # TODO: 2FA on login and something I forgot
                result = await self(
                    functions.auth.SignUp(
                        phone_number=phone_number,
                        phone_code_hash=phone_code_hash,
                        first_name=first_name,
                        last_name=last_name,
                    )
                )
                break
            except RpcException as e:
                if e.description == "PHONE_CODE_INVALID":
                    print("  - The code is invalid.\n")
                    continue
        return self
