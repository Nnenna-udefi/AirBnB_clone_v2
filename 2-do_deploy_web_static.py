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

    put(archive_path, '/tmp/')

    # Extract the archive to the new folder on the server
    filename = archive_path.split('/')[-1]
    foldername = '/data/web_static/releases/' + filename.split('.')[0]
    run('mkdir -p {}'.format(foldername))
    run('tar -xzf /tmp/{} -C {} --strip-components=1'.format(filename, foldername))

    # Remove the archive from the server
    run('rm /tmp/{}'.format(filename))

    # Move the contents of the web_static folder to the new folder
    run('mv {}/web_static/* {}/'.format(foldername, foldername))
    run('rm -rf {}/web_static'.format(foldername))

    # Delete the symbolic link to the current version and create a new one
    run('rm -f /data/web_static/current')
    run('ln -s {} /data/web_static/current'.format(foldername))

    return True
