from setuptools import setup, find_packages

setup(
    name='Duplimage',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'easygui',
        'imagehash',
        'numpy',
        'opencv-python-headless',  # this installs the OpenCV library
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'duplimage=duplimage.main:main'
        ]
    },
    python_requires='>=3.6',  # make sure the minimum required version of Python is supported
)
