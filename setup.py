from setuptools import setup, find_packages

setup(
    name='sdgpy',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'tkinter',
    ],
    entry_points={
        'console_scripts': [
            'sdgpy = src.main:main',
        ],
    },
)
