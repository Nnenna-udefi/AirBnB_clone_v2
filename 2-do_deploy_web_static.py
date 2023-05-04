#!/usr/bin/python3
"""Fabfile that distributes an archive to the web servers"""
from fabric.api import *
import os.path
from datetime import datetime

env.hosts = ['34.203.75.215', '54.175.88.234']
env.user = 'ubuntu'

def do_deploy(archive_path):
    """deploys and distributes archive"""
    if os.path.isfile(archive_path) is False:
        return False
    
    # get the file name without extensions
    filen = archive_path.split('/')[-1]
    name = filen.split('.')[0]

    # upload the archive to the web server
    put(archive_path, '/tmp/{}'.format(filen))

    # uncompress the archive to the folder
    run('mkdir -p /data/web_static/releases/{}'.format(name))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(filen, name))

    # delete the archive from the web server
    run('rm /tmp/{}'.format(filen))

    # delete the symbolic link from the web server
    run('rm -rf /data/web_static/current')

    # create a new symbolic link with the archive file
    run('sudo ln -sf /data/web_static/releases/{} /data/web_static/current'.format(name))

    return True

