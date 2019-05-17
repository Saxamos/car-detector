from setuptools import setup, find_packages

setup(
    name='car-detector',
    version='1.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    license='MIT license',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'detect = app.__main__:main',
        ]
    },
    include_package_data=True,
    # package_data={
    #     'profil_generation_template': [
    #         'simulator/profil_generation_template/*',
    #         'simulator/profil_generation_template/grounds/*',
    #         'simulator/profil_generation_template/photos/*'
    #         'simulator/povray.pov'
    #     ],
    # },
    install_requires=[
        'numpy==1.16.2',
        'Pillow==5.2.0',
        'keras==2.2.4',
        'tensorflow==1.13.1',
        'freezegun==0.3.11',
    ],
    extras_require={
        'dev': [
            'pytest',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console'
    ],
)
