from fabric.api import env, require, sudo, task, cd
from fabric.contrib.console import confirm


@task
def ts_estlan():
    env.hosts = ['ts.estlan.eu']
    env.port = 22
    env.tag = 'ts_estlan'
    env.service_name = "gunicorn-EstLan"
    env.code_dir = '/srv/EstLan'


@task
def update_requirements():
    """ Install the required packages from the requirements file using pip """
    require('hosts', provided_by=[ts_estlan])
    require('code_dir', provided_by=[ts_estlan])

    sudo("cd %s ;"
         ". ./venv/bin/activate ; "
         "pip install -r ./requirements/production.txt" % env.code_dir)


@task
def deploy():
    """ Perform a deploy to the target requested. """
    require('hosts', provided_by=[ts_estlan])
    require('code_dir', provided_by=[ts_estlan])

    confirm("simple_deploy")

    stop_server(silent=True)

    git_pull()

    update_requirements()

    management_cmd("compilemessages")
    management_cmd("collectstatic --noinput")
    management_cmd("migrate EstLan")
    management_cmd("migrate accounts")
    start_server(silent=True)


# SERVER COMMANDS


def stop_server(silent=False):
    if not silent:
        confirm("stop_server")

    require('service_name', provided_by=[ts_estlan])
    sudo("service %s stop" % env.service_name)


def start_server(silent=False):
    if not silent:
        confirm("start_server")

    require('service_name', provided_by=[ts_estlan])
    sudo("service %s restart" % env.service_name)


# HELPERS


@task
def management_cmd(cmd):
    """ Preform a management command on the target. """

    require('hosts', provided_by=[ts_estlan])
    require('code_dir', provided_by=[ts_estlan])

    sudo("cd %s ;"
         ". ./venv/bin/activate ; "
         "cd EstLan ; "
         "python manage.py %s" % (env.code_dir, cmd))


def git_pull():
    with cd(env.code_dir):
        sudo("git pull")

