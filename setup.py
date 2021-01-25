# coding=utf-8
from distutils.core import setup

from setuptools import find_packages

import zsh_history_to_fish


def get_readme():
    with open('README.md') as readme_file:
        return readme_file.read()


setup(
    name='zsh-history-to-fish',
    version=zsh_history_to_fish.__version__,
    description=zsh_history_to_fish.__description__,
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/rsalmei/zsh-history-to-fish',
    author=zsh_history_to_fish.__author__,
    author_email=zsh_history_to_fish.__email__,
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Natural Language :: English',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='zsh fish shell history script'.split(),
    packages=find_packages(),
    python_requires='>=3.5, <4',
    install_requires=['click'],
    extras_require={},
    entry_points={
        'console_scripts': [
            'zsh-history-to-fish=zsh_history_to_fish.command:exporter',
        ],
    },
)
