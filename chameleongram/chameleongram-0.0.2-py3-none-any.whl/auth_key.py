import os
from hashlib import sha1
from typing import Tuple

from chameleongram.connection import Connection
from chameleongram.crypto import AES, RSA, Prime
from chameleongram.raw.core import types, functions
from chameleongram.raw.primitives import *
from chameleongram.raw.reader import Reader
from chameleongram.utils import asyncrange


class AuthKey:
    """Generates an unique Authentication Key - https://core.telegram.org/mtproto/auth_key"""

    MAX_RETRIES = 5

    async def send(self, tl_object: TL):
        data = tl_object.getvalue()
        await self.connection.send(
            bytes(8)
            + Long.getvalue(MessageID.getvalue())
            + Int.getvalue(len(data))
            + data
        )
        return await self.recv()

    async def recv(self) -> TL:
        data = await self.connection.recv()
        assert (
                len(data) != 4
        ), f"[Auth Key][Transport] len(recv()) is 4 (_all[{int.from_bytes(data, 'little', signed=True)}])"
        tl_object = Reader(data[20:]).getobj()
        return tl_object

    def __init__(self, dc_id: int, test_mode: bool = False, max_retries: int = 5):
        self.dc_id = dc_id
        self.connection = None
        self.test_mode = test_mode
        self.MAX_RETRIES = max_retries

    def __str__(self):
        return f"AuthKey(test_mode={self.test_mode}, dc_id={self.dc_id}, connection={self.connection})"

    async def generate(self) -> Tuple[bytes, bytes]:
        async for retries in asyncrange(self.MAX_RETRIES):
            self.connection = Connection(dc_id=self.dc_id, test_mode=self.test_mode)
            try:
                await self.connection.connect()
                nonce = int.from_bytes(os.urandom(16), "little", signed=True)
                res_pq = await self.send(functions.ReqPqMulti(nonce=nonce))
                assert isinstance(
                    res_pq, types.ResPQ
                ), f"[Auth Key][ResPqMulti] Bad response ({res_pq.__class__.__qualname__})"
                assert (
                        nonce == res_pq.nonce
                ), "[Auth Key] nonce and ResPQ nonce are different."
                for (
                        server_public_key_fingerprint
                ) in res_pq.server_public_key_fingerprints:
                    if server_public_key_fingerprint in RSA.public_key_fingerprints:
                        public_key_fingerprint = server_public_key_fingerprint
                        break
                g = Prime.decompose((pq := int.from_bytes(res_pq.pq, "big")))
                p, q = sorted((g, pq // g))
                server_nonce = res_pq.server_nonce
                new_nonce = int.from_bytes(os.urandom(32), "little", signed=True)
                data = types.PQInnerData(
                    pq=res_pq.pq,
                    p=p.to_bytes(4, "big"),
                    q=q.to_bytes(4, "big"),
                    nonce=nonce,
                    server_nonce=res_pq.server_nonce,
                    new_nonce=new_nonce,
                ).getvalue()
                sha_digest = sha1(data).digest()
                data_with_hash = (
                        sha_digest + data + os.urandom(255 - len(data) - len(sha_digest))
                )
                encrypted_data = RSA.encrypt(data_with_hash, public_key_fingerprint)
                server_dh_params = await self.send(
                    functions.ReqDHParams(
                        nonce=nonce,
                        server_nonce=res_pq.server_nonce,
                        p=p.to_bytes(4, "big"),
                        q=q.to_bytes(4, "big"),
                        public_key_fingerprint=public_key_fingerprint,
                        encrypted_data=encrypted_data,
                    )
                )
                assert isinstance(
                    server_dh_params, types.ServerDHParamsOk
                ), f"[Auth Key][ReqDHParams] Bad response ({server_dh_params.__class__.__qualname__})"
                encrypted_answer = server_dh_params.encrypted_answer
                server_nonce = int.to_bytes(server_nonce, 16, "little", signed=True)
                new_nonce = int.to_bytes(new_nonce, 32, "little", signed=True)
                tmp_aes_key = (
                        sha1(new_nonce + server_nonce).digest()
                        + sha1(server_nonce + new_nonce).digest()[:12]
                )
                tmp_aes_iv = (
                        sha1(server_nonce + new_nonce).digest()[12:]
                        + sha1(new_nonce + new_nonce).digest()
                        + new_nonce[:4]
                )
                server_nonce = int.from_bytes(server_nonce, "little", signed=True)
                answer_with_hash = AES.decrypt_ige(
                    encrypted_answer, tmp_aes_key, tmp_aes_iv
                )
                answer = answer_with_hash[20:]
                server_dh_inner_data = Reader(answer).getobj()
                dh_prime = int.from_bytes(server_dh_inner_data.dh_prime, "big")
                g = server_dh_inner_data.g
                b = int.from_bytes(os.urandom(256), "big")
                g_b = int.to_bytes(pow(g, b, dh_prime), 256, "big")
                retry_id = 0
                data = types.ClientDHInnerData(
                    nonce=nonce, server_nonce=server_nonce, retry_id=retry_id, g_b=g_b
                ).getvalue()
                sha = sha1(data).digest()
                padding = os.urandom(-(len(data) + len(sha)) % 16)
                data_with_hash = sha + data + padding
                encrypted_data = AES.encrypt_ige(
                    data_with_hash, tmp_aes_key, tmp_aes_iv
                )
                set_client_dh_params_answer = await self.send(
                    functions.SetClientDHParams(
                        nonce=nonce,
                        server_nonce=server_nonce,
                        encrypted_data=encrypted_data,
                    )
                )
                g_a = int.from_bytes(server_dh_inner_data.g_a, "big")
                auth_key = int.to_bytes(pow(g_a, b, dh_prime), 256, "big")
                server_nonce = int.to_bytes(server_nonce, 16, "little", signed=True)
                g_b = int.from_bytes(g_b, "big")
                safe_range = 2 ** (2048 - 64)
                assert 1 < g < dh_prime - 1
                assert 1 < g_a < dh_prime - 1
                assert 1 < g_b < dh_prime - 1
                assert safe_range < g_a < dh_prime - safe_range
                assert safe_range < g_b < dh_prime - safe_range
                answer = server_dh_inner_data.getvalue()
                assert answer_with_hash[:20] == sha1(answer).digest()
                assert nonce == res_pq.nonce
                server_nonce = int.from_bytes(server_nonce, "little", signed=True)
                assert nonce == server_dh_params.nonce
                assert server_nonce == server_dh_params.server_nonce
                assert nonce == set_client_dh_params_answer.nonce
                assert server_nonce == set_client_dh_params_answer.server_nonce
                server_nonce = int.to_bytes(server_nonce, 16, "little", signed=True)
                server_salt = (
                        int.from_bytes(new_nonce[:8], "big")
                        ^ int.from_bytes(server_nonce[:8], "big")
                ).to_bytes(8, "big")
            except Exception as ex:
                if retries == self.MAX_RETRIES - 1:
                    raise ex
            else:
                return auth_key, server_salt
            finally:
                await self.connection.close()
