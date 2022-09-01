"""
Auxiliary functions for the CLI.
"""

def _prep_groups( groups ):
    """
    Prepare the given flag groups for registry adding.
    This will make sure the given groupnames and associated flags are in a proper dictionary form.
    
    Parameters
    ----------
    groups : list of lists
        The groups to prepare.
    
    Returns
    -------
    dict
        The prepared groups. As { name : [flag1, flag2,...], another : [flag3,...], ... }
    """
    # first join all together ( and remove any whitespaces around the : )
    groups = [ " ".join(i).replace(" :", ":").replace(": ", ":" ) for i in groups ]
    # then separate the group name by the : 
    groups = [ i.split(":") for i in groups ]
    # now split the flags into lists and assemble all again
    groups = { i[0] : i[1].split(" ") for i in groups }
    return groups

def _register_groups( registry, groups ):
    """
    Register the given groups in the registry.

    Parameters
    ----------
    registry : Registry
        The registry to register the groups in.
    groups : dict
        The groups to register. As { name : [flag1, flag2,...], another : [flag3,...], ... }
    """
    groups = _prep_groups( groups )
    for name, flags in groups.items():
        registry.add_group( name, flags )
    registry.save()