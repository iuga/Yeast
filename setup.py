from setuptools import setup, find_packages

setup(
    name='yeast',
    description='Yeast: A Python data processing engine for modeling or visualization',
    version='0.1.0',
    author='@iuga',
    url='https://github.com/iuga/Yeast',
    packages=find_packages(exclude=['tests', 'tools']),
    license='MIT License',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().split()
)
