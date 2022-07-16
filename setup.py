from setuptools import find_packages, setup

setup(
    name='baby_blockchain',
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.*",
    version='0.0.1',
    description='Implementation of baby blockchain in educational purposes',
    author='InterNosTC',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)