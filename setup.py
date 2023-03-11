from setuptools import setup

setup(
    name='pAnnot',
    version='1.0',
    description='parse genome annotations',
    author='Tiezheng Yuan',
    author_email='tiezhengyuan@hotmail.com',
    packages=[
        'pAnnot',
        'pAnnot.database',
        'pAnnot.connector',
        'pAnnot.parser',
        'pAnnot.utils',
        'pAnnot.scripts',
    ],
    install_requires=['requests', 'Bio', 'python-dotenv'],
)