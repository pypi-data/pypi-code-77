# Copyright 2020 Rockabox Media Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

setup(
    name='rbx',
    version='2.11.0.dev184',
    license='Apache 2.0',
    description='Scoota Platform utilities',
    long_description='A collection of common tools for Scoota services.',
    url='http://scoota.com/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
    ],
    author='The Scoota Engineering Team',
    author_email='engineering@scoota.com',
    python_requires='>=3.7',
    install_requires=[
        'arrow>=1,<2',
        'Click<8',
        'colorama',
        'google-cloud-firestore>=2.0.2,<2.1',
        'google-cloud-logging>=2.2.0,<2.3',
        'PyYAML>=5.1.2',
        'requests>=1.21.1',
    ],
    extras_require={
        'aws': [
            'boto3==1.17.13',
        ],
        'buildtools': [
            'bumpversion==0.5.3',
            'check-manifest',
            'fabric~=2.5.0',
            'twine',
        ],
        'eds': [
            'google-cloud-bigquery>=2.9.0,<2.10',
            'google-cloud-datastore>=2.1.0,<2.2',
            'PyMySQL',
            'rfc3339',
            'sqlalchemy>=1.3,<1.4',
        ],
        'geo': [
            'googlemaps>=4.4.2,<5',
        ],
        'manifest': [
            'boto3==1.17.13',
            'opencv-python-headless==4.4.0.46'
        ],
        'mdm': [
            # Cap to 2.2.0 until the unsecure channel issue is resolved
            # See https://github.com/googleapis/python-pubsub/issues/290
            'google-cloud-pubsub>=2,<2.3.0',
        ],
        'mysql': [
            'PyMySQL',
            'sqlalchemy>=1.3,<1.4',
        ],
        'queues': [
            'rq==1.4.3',
            'rq-scheduler==0.10.0',
        ],
        'storage': [
            'google-cloud-storage>=1.36,<2',
        ],
        'tasks': [
            'google-cloud-tasks>=2.0,<3',
        ],
        'tests': [
            'Flask==1.1.2',
            'googlemaps>=4.4.2,<5',
        ],
    },
    entry_points={
        'console_scripts': [
            'buildtools = rbx.buildtools.cli:program.run [buildtools]',
            'build_image_from_manifest = rbx.manifest.cli:build_image_from_manifest [manifest]',
            'geocode = rbx.geo.cli:geocode [geo]',
            'reverse_geocode = rbx.geo.cli:reverse_geocode [geo]',
            'unpack = rbx.geo.cli:unpack [geo]',
        ],
    },
    packages=find_packages(),
    zip_safe=True
)
