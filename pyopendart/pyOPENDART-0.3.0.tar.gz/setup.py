# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyopendart',
 'pyopendart.api',
 'pyopendart.api.dataframe',
 'pyopendart.api.dict',
 'pyopendart.api.http']

package_data = \
{'': ['*']}

install_requires = \
['furl>=2.1.0,<3.0.0',
 'pandas>=1.2.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.25.1,<3.0.0']

extras_require = \
{'httpx': ['httpx>=0.16.1,<0.17.0']}

setup_kwargs = {
    'name': 'pyopendart',
    'version': '0.3.0',
    'description': '전자공시시스템 DART 파이썬 API (for Humans)',
    'long_description': '# pyOPENDART - OPEN DART Python API (for Humans)\n\n전자공시시스템 API 를 편리하게 사용하기 위해 저수준 HTTP API부터 데이터프레임을 리턴하는 고수준 API 등 각종 편리한 API와 유틸리티들을 제공합니다.\n\n### Disclaimer\n> 본 소프트웨어는 금융감독원의 전자공시시스템 OPEN API 를 추가적으로 가공하고 부가기능을 제공하는 소프트웨어로써 MIT 라이선스에 따라 저자 또는 저작권자는 소프트웨어와 소프트웨어와 연관되어 발생하는 문제에 대해 책임을 지지 않습니다.\n> \n> OPEN DART API에 관한 정보는 opendart.fss.or.kr 를 참조하시기 바랍니다.\n\n## Installation\n\n```shell\npip install pyopendart\n```\n\n## What is DART?\n\n> 전자공시시스템(DART ; Data Analysis, Retrieval and Transfer System)은 상장법인 등이 공시서류를 인터넷으로 제출 하고, 투자자 등 이용자는 제출 즉시 인터넷을 통해 조회할 수 있도록 하는 종합적 기업공시 시스템입니다.\n>\n> by [dart.fss.or.kr - DART소개](http://dart.fss.or.kr/introduction/content1.do)\n\n## What is OPEN DART?\n\n> DART에 공시되고있는 공시보고서 원문 등을 오픈API를 통해 활용할 수 있습니다. 활용을 원하시는 누구든지(개인, 기업, 기관 등) 이용하실 수 있습니다.\n>\n> by [opendart.fss.or.kr - 오픈API 소개](https://opendart.fss.or.kr/intro/main.do)\n\n## Features\n\n* OPEN API 데이터프레임, 딕셔너리 클라이언트\n    * dart의 축약된 필드명을 자세한 한글, 영어 필드명으로 변환\n    * 날짜, 숫자등에 대해 데이터 타입 변환\n* 공시원문, 재무재표 등 원본파일 다운로드 클라이언트\n* 로우레벨 OPEN API HTTP 클라이언트\n    * 커넥션 풀, 타임아웃등 네트워크 옵션 조정 기능 제공\n    * xml, json, zip 리소스 접근 메서드 제공\n* 편리하고 타입 정의된 클라이언트 인터페이스들\n    * 요청 인자 중 공시유형등의 필드에 대한 Enum 제공\n    * 예외 클래스 제공\n* 개발가이드에 나와있는 출력설명란의 출력과 설명의 매핑 제공 (비고 등)\n\n## Usage\n\n[https://pyopendart.seonghyeon.dev/](https://pyopendart.seonghyeon.dev/) 에서 자세한 문서를 확인할 수 있습니다.\n\n## License\nThis project is licensed under the terms of the MIT license.',
    'author': 'Seonghyeon Kim',
    'author_email': 'self@seonghyeon.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NovemberOscar/pyOPENDART',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
