"""
Utility functions for filerecords.
"""

import logging
import yaml
from yaml.loader import SafeLoader
import os
import sys
import pandas as pd

import filerecords.api.settings as settings

def log( name : str = "filerecords", level : int = logging.INFO, outfile : str = None ):
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
    logger = logging.getLogger( name )
    logger.setLevel( level )

    if not logger.hasHandlers():

        if outfile is None:
            logger.addHandler( logging.StreamHandler( sys.stdout ) )
        else:
            logger.addHandler( logging.FileHandler( outfile ) )

    return logger

logger = log()

def make_new_registry( directory : str ):
    """
    Make a new registry in a directory.

    Parameters
    ----------
    directory : str
        The directory to create the registry in.
    """

    registry_dir = os.path.join( directory, settings.registry_dir )
    if not os.path.exists( registry_dir ):
        os.mkdir( registry_dir )

    # add an INDEXFILE to the registry.
    indexfile = os.path.join( registry_dir, settings.indexfile )
    os.system( f"echo '{settings.indexfile_header}' > {indexfile}" )

    # add a METADATA file to the registry.
    _init_metafile( registry_dir )

    logger.info( f"New registry created at {directory}" )


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
    paths = os.path.abspath( directory )
    while True:

        registry_dir = os.path.join( paths, settings.registry_dir )
        if os.path.exists( registry_dir ):
            logger.info( f"Found registry at {registry_dir}" )
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
    
