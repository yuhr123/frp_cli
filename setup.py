from setuptools import setup

setup(
    name='frp_cli',
    version='0.1',
    py_modules=['frp_cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        frp_cli=frp_cli:cli
    ''',
)
