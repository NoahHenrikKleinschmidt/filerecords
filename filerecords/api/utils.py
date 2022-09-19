"""
Utility functions for filerecords.
"""

import logging
import subprocess
import yaml
from yaml.loader import SafeLoader
import os
import sys
import pandas as pd

import filerecords.api.settings as settings

def log( name : str = "filerecords", level : int = None, outfile : str = None ):
    """
    A logger that can be used to log records.

    Parameters
    ----------
    name : str
        The name of the logger.
    level : int
        The level of the logger.
    outfile : str
        The file to log to. If None, logs to stdout.
    """
    level = level if level else settings.log_level
    logger = logging.getLogger( name )
    logger.setLevel( level )

    if not logger.hasHandlers():

        if outfile is None:
            logger.addHandler( logging.StreamHandler( sys.stdout ) )
        else:
            logger.addHandler( logging.FileHandler( outfile ) )

    return logger

logger = log()

def make_new_registry( directory : str, perms : (int or str) = None ):
    """
    Make a new registry in a directory.

    Parameters
    ----------
    directory : str
        The directory to create the registry in.
    perms : int or str
        The permissions to set on the registry directory. This can be either the 
        numeric permissions (e.g. 755) or a string (e.g. "rwxr-xr-x").
        By default the permissions are inherited by the parent directory.
    """

    registry_dir = os.path.join( directory, settings.registry_dir )
    if os.path.exists( registry_dir ):
        raise FileExistsError( f"Registry already exists in {directory}" )
    
    os.makedirs( registry_dir )

    # add an INDEXFILE to the registry.
    indexfile = os.path.join( registry_dir, settings.indexfile )
    os.system( f"echo '{settings.indexfile_header}' > {indexfile}" )

    # add a METADATA file to the registry.
    _init_metafile( registry_dir )

    # set the permissions 
    if perms is None:
        perms = get_directory_perms(directory)
    os.system( f"chmod -R {perms} {registry_dir}" )

    logger.info( f"New registry created at {directory}" )

def get_directory_perms(directory):
    """
    Get the permissions of the parent directory.
    
    Parameters
    ----------
    directory : str
        The directory to get the permissions of the parent directory of.

    Returns
    -------
    int
        The permissions of the parent directory as numeric value.
    """
    perms = os.stat( directory ).st_mode
    perms = oct( perms )[-3:]
    perms = int( perms )
    return perms


def find_registry( directory :str ):
    """
    Find a registry associated with a source directory. 
    This will repeatedly search the upper level directories
    until a registry is found.

    Parameters
    ----------
    directory : str

    Returns
    -------
    str or None
        The path to the registry directory or None if no registry was found.
    """
    # paths = os.path.abspath( directory )
    paths = subprocess.check_output( f"cd {directory} ; pwd", shell = True ).decode().strip()
    while True:

        registry_dir = os.path.join( paths, settings.registry_dir )
        if os.path.exists( registry_dir ):
            logger.debug( f"Found registry in { os.path.dirname(registry_dir) }" )
            return registry_dir

        paths = os.path.dirname( paths )

        if paths == "/":
            return None

def get_indexfile( registry_dir : str ):
    """
    Get the indexfile of a registry.

    Parameters
    ----------
    registry_dir : str
        The path to the registry directory.
    
    Returns
    -------
    str
        The path to the registry's indexfile.
    """
    indexfile = os.path.join( registry_dir, settings.indexfile )

    if not os.path.exists( indexfile ):
        logger.critical( f"No indexfile found in {registry_dir}, broken registry?!" )
        return None

    return indexfile

def get_metafile( registry_dir : str ):
    """
    Get the metafile of a registry.

    Parameters
    ----------
    registry_dir : str
        The path to the registry directory.
    
    Returns
    -------
    str
        The path to the registry's metafile.
    """
    metafile = os.path.join( registry_dir, settings.registry_metafile )

    if not os.path.exists( metafile ):
        logger.critical( f"No metafile found in {registry_dir}, broken registry?!" )
        return None

    return metafile


def load_indexfile( filename : str ):
    """
    Load a registry indexfile.

    Parameters
    ----------
    filename : str
        The path to the registry indexfile.
    
    Returns
    -------
    pandas.DataFrame
        The contents of the registry indexfile.
    """
    df = pd.read_csv( filename, sep = "\t" )
    df.index = df["id"].values
    return df 

def load_yamlfile( filename : str ):
    """
    Load a yaml metadata file.

    Parameters
    ----------
    filename : str
        The path to the yaml file.
    
    Returns
    -------
    dict
        The contents of the yaml file.
    """
    with open( filename, "r" ) as f:
        contents = yaml.load( f, Loader = SafeLoader )

    return contents

def save_yamlfile( filename : str, contents : dict ):
    """
    Save a yaml metadata file.

    Parameters
    ----------
    filename : str
        The path to the yaml file.
    contents : dict
        The contents of the yaml file.
    """
    with open( filename, "w" ) as f:
        yaml.dump( contents, f )

def add_registry_to_gitignore():
    """
    Add the registry directory to a .gitignore file in the current directory.
    """
    gitignore = os.path.join( os.getcwd(), ".gitignore" )
    with open( gitignore, "a" ) as f:
        f.write( f"\n{settings.registry_dir}" )

def _init_metafile( registry_dir : str ):
    """
    Initialize a registry metadata file. 

    Parameters
    ----------
    registry_dir : str
        The registry directory.
    """
    contents = {
        "directory" : registry_dir,
        "comments" : {},
        "flags" : [],
        "groups" : {}
    }
    metafile = os.path.join( registry_dir, settings.registry_metafile )
    with open( metafile, "w" ) as f:
        yaml.dump( contents, f )

def _init_entryfile( registry_dir : str, id : str ):
    """
    Initialize a registry entry file. 

    Parameters
    ----------
    registry_dir : str
        The registry directory.
    id : str
        The id of the entry.
    """
    entryfile = os.path.join( registry_dir, id )
    with open( entryfile, "w" ) as f:
        yaml.dump( settings.entryfile_template, f )
    
    perms = get_directory_perms(registry_dir)
    os.system( f"chmod -R {perms} {entryfile}" )