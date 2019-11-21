from setuptools import setup, find_packages

setup(
    name='blender_squirrel',
    version='0.1a0',
    description='Blender Squirrel - A Addon Manager for Blender',
    author="Christopher Winkelmann",
    author_email="winkelchri@gmail.com",
    url='https://github.com/winkelchri/blender_addon_installer',
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(
        exclude=['log', 'tests', 'ui-mockups', '.*']
    ),
    include_package_data=True,
    data_files=None,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'squirrel=cli:cli'
        ]
    }
)
