#!/usr/bin/python3
"""script that creates and distributes the function deploy to the web servers
"""
from fabric.api import *
import os.path
from datetime import datetime

env.hosts = ['34.203.75.215', '54.175.88.234']
env.user = 'ubuntu'


def do_pack():
    """generates a .tgz from html folder"""
    # creates the versions directory
    local('mkdir -p versions')

    dnow = datetime.now()
    archive_name = 'web_static_{}{}{}{}{}{}.tgz'.format(dnow.year, dnow.month,
                                                        dnow.day, dnow.hour,
                                                        dnow.minute,
                                                        dnow.second)
    # create archive and store it in the version directory
    arch_store = local("tar -cvzf versions/{} web_static".format(archive_name))

    if arch_store.succeeded:
        return 'versions/{}'.format(archive_name)
    else:
        return None

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

def deploy():
    """call do_pack and do_deploy functions"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

def do_clean():
    """Fabric that deletes out-of-date archives, using the functiondo_clean"""
    number = int(number)

    if number < 2:
        number = 1
    else:
        number += 1

    archives_to_delete = sorted(
        run("ls -1 /data/web_static/releases").split("\n"))

    for archive in archives_to_delete[:-number]:
        if archive != "":
            with settings(warn_only=True):
                run("rm -rf /data/web_static/releases/{}".format(archive))

    versions_to_delete = sorted(
        local("ls -1 versions", capture=True).split("\n"))

    for version in versions_to_delete[:-number]:
        if version != "":
            with settings(warn_only=True):
                local("rm versions/{}".format(version))
