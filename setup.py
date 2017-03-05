from setuptools import setup, find_packages

setup(
    name='sample',

    version='0.0.1',

    description='Amber State Machine',
    long_description='Amber State Machine',

    # The project's main homepage.
    url='',

    # Author details
    author='Henri Korpela',
    author_email='',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='dfa nfa state_machine automate',

    packages=find_packages(exclude=['tests']),
)