from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='bioplotz',
    version='0.1.0.dev2',
    packages=['bioplotz'],
    url='https://github.com/sc-zhang/bioplotz',
    license='',
    author='Shengcheng Zhang',
    author_email='zsc-zhang@foxmail.com',
    description='A python package for drawing some bioinformatic pictures.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy',
                      'matplotlib',
                      'pandas']
)
