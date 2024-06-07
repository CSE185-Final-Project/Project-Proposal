from setuptools import setup, find_packages

setup(
    name='RNAseq_Easy',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['docs/Manual.txt', 'scripts/data_vis.R'],
    },
    install_requires=[
        'pandas', 
        'scipy >= 1.13',
        "memory_profiler"
    ],
    entry_points={
        'console_scripts': [
            'RNAseq_Easy=scripts.scRNAseq_Easy:main',
        ],
    },
)
