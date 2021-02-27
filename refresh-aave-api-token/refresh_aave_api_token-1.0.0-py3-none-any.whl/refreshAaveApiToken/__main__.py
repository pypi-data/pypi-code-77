import sys
import boto3
import argparse
import os


# from .classmodule import MyClass
# from .funcmodule import my_function

user_pool_id = "us-east-2_UA5tqZASv"
client_id = "5b6893vo53h5jo7jk8prhphei4"
client = boto3.client('cognito-idp')

refresh_token = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.rKd7DP1a4GwpnIg2pbIWvwVAspE6WDKKgr6L5xFHRaHZp2sJ-KE0ABa_XIm15F7Bij5je7Eq9tEdPMA2oiVLVj6JCUII3wS3tQIq3ABPJVAdDVFcejlTZOD-ymPc8zyUE9TFpM81lEvzXX4-VHomlHRoO_Lmhpmcr-ZHHMWbFlNAC6Agzj0j0SiQ8qDek6dRnDFWfA-AHMfQLc7XSNi9nbAJZ3eiRI_gj2domFhft4VpQxEchAFpqAvV_DtpPP-D3WCkIgWz29WUhoj3kP_CYgtyvn2odtJd53FMXtV2sEMXK4iaE6fW3Vit1Rtrz6hdU2Xg530kf7kfZhcZw6RBQg.ZQWK4bi-fcZRYt2L.mou_grdknBdVeD-2x88SvNq1c6zZjAc1X-uwc8HHVjxKjnBEgiSgmq0Pt5tU2XSj7JZrvVXt7DoEqpr-1k6Yj7zs646BFFyrcK51ioADN9fNivUVcJXAcWJdBJBDwVRrya99REU7YwUZRkv3MmShh3zRB4kJyliz5XikDmGBmMM_kjNIvry9rb48CVPEae9UXYmPtI5Zoft5JVZIrICSqunVsmaLjf3BhKzBYis1Qi7iR5COhWJgLGdbxYFU__ppa6MBCjoVarNoI2QBoaHKHAWLx7QBgmKDU7-gYqKjwaauxVrZST_ZWLlKybJZ-90pIv_dA3X0rIPjKkaNMH_KVu_oUxm3-8PcPN8-0cWR6DopqREqmn6d2t89K2RwfQhV9xqL96Vr2EkyYMSZk9jKkMBBgLXm0PKfsAQYKWsBwqUgsJ_B-NE6zfvU_gvHKLbYi9G5xZ6ign-FWbcWAk1_qXKGPsQ2lrIVwPAEqkrwwSU0KKODp4odl9kvzWPGveQ3CiXJnf074OpBXwcq9RRg8Jx-C90SGnXk-JgkXy362tILo3U4c3MRO1dKQ4I2wkWTKh4a8SbdDvm3VyhkUTZ_kz5iaFND70CG9mr-MPRuQsBjbnCzZlx48zx8FmX2wDv3dsAaxjVJQTsl8DYCUZKFMAwzDFXwPealPex4MH-k_XsVJ561dGm7pkvgdq-t0J_ZidyRlW5Oze7yuiC2j-lRX7SwLSXcTcuUCU485iA99Af-alhjvFaJg7kSLKTdQF1Wz_0edIM8x2EX8o0a4GnmUTpxj4IRN33af3EKPnegjG1hVlhLLAo8DlCV5N-Gd85pRPnwZj-yMhqXrGXRoZx3GEz8uhgBoLCWHOBhU7luMLyeDoAj6hWY0aYpAVSQTGTFRzkm1WNFvN8j3JtHvmTtHzp6uv-nO3PrMdW2SDg7F1nOV6slScp-MzkYe958-tAirvNlY8F-znsgCQlqftFIbpux4tdf07FiL7KcTdJh58ynRymqO2J3Wr33gUlJKIuPqMDGzbiHvq-w85FANOcLY7amHNKAKgbWId2XM4an7osI7hMyrJ_h2gBV5icJ9aOOsDqpWAPVgDkeqU4xQhrc5n9SUYFbIql1g_OE92OJoXyISmoiWnB7rraN48lYGV2BGkLEo2vQtNUbPDNwyeI3P9eLr0P_JawyN7BY7-YLl0rUVX5zuoNMwSdHy6np132ANYRMrc0BdRrnkq7db_qu4h-_g4F6bGKnmCvqR-hvcwm3E0YWURKUR0Dy2Kzu2zVRQ6yfkgPCeRGjlpFz3NyGhp6EVA6LLYKnEsoH4E9KrNxqNeyh2KLoapsiOUKP5OGhDlAoFXVbS4PZn16y324pDTu9pe8FQbQt5BJfr_8BJ5E6yyil9RUiLPKnhwvCbD-rkskNAbzF28Xj1AdMnNYPsZI0Dw0w6CGvCCfX33_NYJnkBWixB6y-oMEDUtXO1DhN5DGpelF0aG90tlp8XjLz-ZB5gvRSGbmwQKtjlPutesrusd5e7tUdXA06r2SCpjtioU6rQR7-Jz8mcaWLR_1g__yvdvDq4dPmuu_DupnBzDKCQgy9iQaG2355aJNSi-SnuhOA382Uthnr3pB7se_UlpB6HQiXPIiWROVebuFDina53AxJMrngUoA3K6X8L3PxZOiS1kFkJUswPKgqr2xZ6lzIa7i7KN4-qlYJzSESQgpR5_ECc0dV_-V07MU0E8I3JpS6fGpRDqyQJH2A54ir.gBgmAMMN230EY2AmqgF55A"


def refresh_access_token(refresh_token):

    dict_to_return = {
        "isError": True,
        "error": "CryptoTalk API Error!"
    }

    try:
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token
            },
        )
        dict_to_return["isError"] = False
        dict_to_return["data"] = response
        return dict_to_return
        
    except:
        dict_to_return["data"] = sys.exc_info()[0]
        return dict_to_return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh_token', type=str,
                        help="Enter your refresh token. This refresh token will be used to generate a new access token for you.")

    os.system('cls' if os.name == 'nt' else 'clear')

    args = parser.parse_args()

    sys.stdout.write("*" * 50 + "\n")
    sys.stdout.write(
        "This application will take your refresh token and generate a new access token for you. \n")

    response = refresh_access_token(args.refresh_token)

    if response["isError"] == True:
        sys.stdout.write("*" * 50 + "\n")
        sys.stdout.write("An Error has occured. \n")
        sys.stdout.write(str(response["data"]) + "\n")

    else:
        sys.stdout.write("*" * 50 + "\n")
        sys.stdout.write("Below is your new access token\n")
        sys.stdout.write(
            "\n" + str(response["data"]["AuthenticationResult"]["AccessToken"]) + "\n" + "\n")
        


if __name__ == '__main__':
    main()
