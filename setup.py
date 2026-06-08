from setuptools import setup

setup(
    name='source',
    version='0.0.1',
    packages=[
        '.source'
        '.source.application',
        '.source.model',
        '.source.model.dto',
        '.source.application',
        '.source.application.file_handler',
        '.source.application.file_merger',
        '.source.application.process_handler',
    ]
)
