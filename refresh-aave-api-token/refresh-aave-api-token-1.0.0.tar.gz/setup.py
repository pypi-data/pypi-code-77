from setuptools import  setup,Extension
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'refresh-aave-api-token',
    version = '1.0.0',
    author='Avyact Jain',
    description = "A package to refresh access tokens for CryptoTalk Aave Rest APIs.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='avyactjain@gmail.com', 
    install_requires=['boto3','argparse'],
    packages = ['refreshAaveApiToken'],
    entry_points = {
        'console_scripts': [
            'refreshAaveApiToken = refreshAaveApiToken.__main__:main'
        ]
    },
    project_urls={  # Optional
        'SignUp': 'https://aaveonmobile-home.auth.us-east-2.amazoncognito.com/signup?client_id=5b6893vo53h5jo7jk8prhphei4&response_type=code&scope=/aave/address%20/aave/allowance%20/aave/borrow%20/aave/configuration%20/aave/deposit%20/aave/rates%20/aave/repay%20/aave/setUserUseReserveAsCollateral%20/aave/swapBorrowRateMode%20/aave/user-health%20/aave/withdraw%20aws.cognito.signin.user.admin%20email%20openid%20phone%20profile&redirect_uri=https://access-token-fiz3rywh2a-an.a.run.app/token',
        'Twitter': 'https://twitter.com/CryptoTalk_',
    },
    )
