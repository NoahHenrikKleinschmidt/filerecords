import setuptools

with open( "README.md", "r" ) as fh:
    long_description = fh.read()

setuptools.setup(
    name="filerecords", 
    version="0.0.1",
    author="Noah H. Kleinschmidt",
    author_email="noah.kleinschmidt@students.unibe.ch",
    description="A command-line toolbox to keep file metadata in an organized and easily accessible way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="NONE YET",
    
    packages=setuptools.find_packages(),

    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [ 
            "filerecords=filerecords.cli:setup",
            "records=filerecords.cli:setup",
        ]
    },
    python_requires='>=3.6',
)