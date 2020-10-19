"""Setup file for Lapdog."""
from setuptools import setup, find_packages
import os

path_to_lapdog = "/Users/isaacsheikh/Document/GitHub/lapdog"

setup(name="lapdog",
      version="1.0.0",
      description="A slack bot that reads, sends, and deletes SQS issues",
      author="Rachel Sheikh",
      author_email='sheikhrachel97@gmail.com',
      platforms=['osx'],
      license=['MIT'],
      url="http://github.com/sheikrachel/lapdog",
      packages=[pkg for subdir in os.listdir(path_to_lapdog)
                if os.path.isdir(os.path.join(path_to_lapdog, subdir))
                for pkg in find_packages(os.path.join(path_to_lapdog, subdir))],
      install_requires=['requests',
                        'pytest',
                        'pre-commit',
                        'black',
                        'flask',
                        'boto3',
                        'moto'
                        ]
      )
