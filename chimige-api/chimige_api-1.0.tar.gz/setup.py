from setuptools import setup


long_description = """
# chimige_api

Из-за некорректного отображения документации в PyPI, она была полностью перемещена на гитхаб - https://github.com/Ma-Mush/chimige_api/
"""


setup(
    name="chimige_api",
    version="1.0",
    description="Api для соцсети Chimige (Чимиге)",
    packages=["chimige_api"],
    author_email="ma_mush@mail.ru",
    zip_safe=False,
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires= "requests==2.25.1"
)
