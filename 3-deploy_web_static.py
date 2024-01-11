#!/usr/bin/python3
from fabric.api import put, run, local, env
from time import strftime
from os import path

env.hosts = ["100.25.220.119", "100.25.147.34"]

def do_pack():
    """A script that generates and archives the contents of the web_static folder"""
    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/".format(filename))
        return "versions/web_static_{}.tgz".format(filename)
    except Exception as e:
        return None

def do_deploy(archive_path):
    """Fabric script that distributes an archive to your web servers"""
    if not path.exists(archive_path):
        return False
    try:
        tgzfile = archive_path.split("/")[-1]
        filename = tgzfile.split(".")[0]
        pathname = "/data/web_static/releases/" + filename
        put(archive_path, '/tmp/')
        run("mkdir -p {}".format(pathname))
        run("tar -xzf /tmp/{} -C {}".format(tgzfile, pathname))
        run("rm /tmp/{}".format(tgzfile))
        run("mv {}/web_static/* {}".format(pathname, pathname))
        run("rm -rf {}/web_static".format(pathname))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(pathname))
        return True
    except Exception as e:
        return False

def deploy():
    """Run the do_pack and do_deploy functions"""
    path = do_pack()
    if not path:
        return False
    return do_deploy(path)
