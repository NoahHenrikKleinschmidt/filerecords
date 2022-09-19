import setuptools

with open( "README.md", "r" ) as fh:
    long_description = fh.read()

setuptools.setup(
    name="filerecords", 
    version="0.0.1",
    author="Noah H. Kleinschmidt",
    author_email="noah.kleinschmidt@students.unibe.ch",
    description="A command-line toolbox to keep file metadata in an organized and easily accessible way through comments and flags.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoahHenrikKleinschmidt/filerecords",
    
    # the nuitka stuff is put on ice for the time being...
    # command_options={
    #   'nuitka': {
    #      # boolean option, e.g. if you cared for C compilation commands
    #      '--show-scons': True,
    #      # options without value, e.g. enforce using Clang
    #      '--clang': None,
    #      # options with single values, e.g. enable a plugin of Nuitka
    #      '--enable-plugin': "pyside2",
    #      # options with several values, e.g. avoiding including modules
    #      '--nofollow-import-to' : ["*.tests", "*.distutils", #],
    #      #'--noinclude-custom-mode' : [
    #                                     "matplotlib", 
    #                                     "IPython", 
    #                                     "bokeh", 
    #                                     "sphinx",
    #                                     "pytest",
    #                                     "tkinter",
    #                                     "sqlalchemy",
    #                                     "jupyter",
    #                                     "ipywidgets",
    #                                     "PIL",
    #                                     "PyQt5",
    #                                 ]
    #   }
    # },
    
    packages=setuptools.find_packages(),

    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        "pandas",
        "PyYAML",
        ],

    entry_points={
        "console_scripts": [ 
            "filerecords=filerecords.cli:setup",
            "records=filerecords.cli:setup",
        ]
    },
    
    python_requires='>=3.6',
)