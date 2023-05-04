#!/usr/bin/python3
"""
    Fabric script that generates a .tgz archive from the
    contents of the web_static folder
"""
from fabric.api import *
from datetime import datetime


def do_pack():
    """generates a .tgz from html folder"""
    # creates the versions directory
    run('mkdir -p versions')

    dnow = datetime.now()
    archive_name = 'web_static_{}{}{}{}{}{}.tgz'.format(dnow.year, dnow.month,
                                                       dnow.day, dnow.hour,
                                                       dnow.minute,
                                                       dnow.second)
    
    # create archive and store it in the version directory
    arch_storage = local("tar cvzf version/{} /web_static".format(archive_name))

    if arch_storage.succeeded:
        return 'versions/{}'.format(archive_name)
    else:
        return None
