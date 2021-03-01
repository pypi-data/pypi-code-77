# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastabf',
 'fastabf.DAL',
 'fastabf.HACpackage',
 'fastabf.Helpers',
 'fastabf.csvstores',
 'fastabf.pipelines']

package_data = \
{'': ['*'], 'fastabf': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['pandas>=1.2,<2.0']

setup_kwargs = {
    'name': 'fastabf',
    'version': '0.8.10',
    'description': 'A robust computation package for activity based funding calculations',
    'long_description': 'fastABF is a fast and robust computation module for activity based funding (ABF). It helps to \nstreamline the computation of ABF activities as per the National Efficient Price (NEP) 20-21 framework guidelines.  It covers the following major ABF activity types\n\n- admitted acute\n- admitted sub/non-acute\n- non-admitted\n- emergency department or emergency service\n\n**Documentation**: [fastABF doc](https://greenlakemedical.github.io/fastABF/)\n\n---\n## Features\n\n- **Fast to setup** - go from start to computing an example ABF episode within 5 minutes. Save *close to a month* of development and testing time!\n- **Robust** - with python type hints, strong version control (via Poetry) and strong test coverage the code base is ready for use in backend systems.\n- **Easy to understand and extend** - numerous comments and well structured organisation, ensure that health IT developers can easily use and extend these modules. \n- **Pain free** - The code aims to distill the numerous computations detailed in the IHPA NEP 20-21 computation documentation and guidelines. These span over **60 pages**. This is in addition to the HAC computation guidelines which span **over 40 pages**. The effort we have put into this is time that you can spend on making other innovative contributions (or taking several long walks :) ).\n- **Lower bug count** - By leveraging a well tested and open source code base - developers can reduce the chance of introducing bugs into their ABF calculations by over 25-30%* \n- **Incorporates METeOR conventions** - The METeOR identifiers have been mapped to user friendly Python `Enum` names. Now instead of remembering the METeOR numerical identifiers you can use these human readable class names  - reducing the possibility of bugs and errors creeping in. \n- **HAC adjustment computations** - The detailed steps of the HAC adjustments are included as well. \n- **Remoteness calculations** - This code also contains the steps to obtain the remoteness values (from postcode and SA2 address). Hence it enables automatic extraction of the RA16 remoteness class)\n\n<small>* based on the experience of the internal dev-team and bugs caught and resolved via type checking and testing during development.\n\n**Glossary**\n- [HAC]: hosptial acquired complications\n- [IHPA]: Independent hospital pricing authority\n- [METeOR]:  Metadata online registry \n- [ABF]: Activity based funding\n- [NEP]: National efficient price\n\nIt is assumed that you are familiar with \n- python \n- the terminology and concepts of ABF.\n',
    'author': 'Sri Sridharan',
    'author_email': 'sri@greenlakemedical.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GreenlakeMedical/fastABF',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
