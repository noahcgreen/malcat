from setuptools import setup, find_packages

setup(
    name='malcat',
    packages=find_packages(),
    install_requires=[
        'flask',
        'gunicorn',
        'lxml',
        'requests',
        'redis',
        'requests-cache',
        'flask-caching'
    ]
)
