from setuptools import setup, find_packages

setup(
    name='subnet_calc',
    version='0.1',
    packages=find_packages(),
    py_modules=['ipcalc'],  # <-- add this line
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ipcalc=ipcalc:main',
        ],
    },
)
