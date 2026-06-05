from setuptools import setup

setup(
    name='file_merger',
    version='0.0.1',
    packages=[
        '.source'
        '.source.application',
        '.source.file_merger.model',
        '.source.file_merger.application',
    ]
)
