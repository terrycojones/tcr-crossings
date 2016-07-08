#!/usr/bin/env python

"""
This fabfile contains the recipe for automatically testing and deploying the
website.

The file is divided into 3 sections:

  Site definitions
  Helper functions
  Top-level fab commands

Unless you are doing working to fix our deployment process, you will probably
only be interested in the top-level fab commands. You can list these by running

  $ fab --list

and

  $ fab -d command-name  # Show a description of a command.

Helper functions (which all start with underscore) cannot be run directly from
the shell. They are used by the top-level commands.

The top-level commands have names (and comments) that should make it easy to
figure out what they do.

"""

from datetime import datetime
from fabric.api import require, run, local, abort, env, put
from fabric.context_managers import settings
import os


# ------------------------- SITE DEFINITIONS -------------------------

def production():
    """Define the host for borders.transcontinental.cc"""
    RELEASE = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    env.hosts = ['borders@jon.es']
    env.sitename = 'borders.transcontinental.cc'
    env.path = '%s-%s' % (env.sitename, RELEASE)

# ------------------------- HELPER FUNCTIONS -------------------------


def x_make_virtualenv():
    """Create a new virtualenv."""
    require('hosts', provided_by=[production])
    run('cd %(path)s && virtualenv .' % env)


def x_install_dependencies():
    """Use pip to install required packages."""
    # PyPI mirror list is at http://pypi.python.org/mirrors
    require('hosts', provided_by=[production])
    run('./%(path)s/bin/pip install --timeout=60 --log %(path)s-pip.log '
        '--download-cache PIP-DOWNLOAD-CACHE -M '
        '--mirrors b.pypi.python.org '
        '--mirrors c.pypi.python.org '
        '--mirrors d.pypi.python.org '
        '--mirrors e.pypi.python.org '
        '--mirrors f.pypi.python.org '
        '-r %(path)s/requirements.txt 2>%(path)s-pip.errs' % env)


def x_test_deployment():
    """Tests the deployed website passes the tests."""
    require('hosts', provided_by=[production])
    try:
        # Copy over the local_settings.py for unit testing.
        run('cp %(path)s/fluidinfo/local_settings.example '
            '%(path)s/fluidinfo/local_settings.py' % env)
        print('\nRunning the unit tests (this can take some time)...\n')
        # run the tests
        result = run('source %(path)s/bin/activate && '
                     'cd %(path)s/fluidinfo && '
                     'python manage.py test' % env)
        if result.failed:
            # handle failed test run
            abort('Tests failed - fix and re-deploy')
    finally:
        # Put correct local_settings.py in place.
        run('cp %(path)s/resources/django/%(sitename)s-local_settings.py '
            '%(path)s/fluidinfo/local_settings.py' % env)


def _replace_symlink():
    """
    Link the newly uploaded deployment to the right place in the filesystem
    after removing the old link.
    """
    require('hosts', provided_by=[production])
    run('rm -f %(sitename)s' % env)
    run('ln -s %(path)s %(sitename)s' % env)


def _update_init():
    """Install the updated /etc/init config file."""
    require('hosts', provided_by=[production])
    with settings(warn_only=True):
        run('sudo /bin/cp /etc/init/%(sitename)s.conf '
            '/etc/init/%(sitename)s.conf.orig' % env)
    run('sudo /bin/cp %(path)s/resources/init/%(sitename)s.conf /etc/init' %
        env)


def _update_nginx():
    """Install the updated nginx config file."""
    require('hosts', provided_by=[production])
    with settings(warn_only=True):
        run('sudo /bin/cp /etc/nginx/sites-available/%(sitename)s '
            '/etc/nginx/sites-available/%(sitename)s.orig' % env)
    run('sudo /bin/cp %(path)s/resources/nginx/%(sitename)s '
        '/etc/nginx/sites-available' % env)
    run('test -f /etc/nginx/sites-enabled/%(sitename)s || '
        'sudo ln -s /etc/nginx/sites-available/%(sitename)s '
        '/etc/nginx/sites-enabled/%(sitename)s' % env)


def _restart_nginx_if_config_has_changed():
    """Restart nginx if its config file has changed."""
    require('hosts', provided_by=[production])
    run('cmp -s /etc/nginx/sites-available/%(sitename)s '
        '/etc/nginx/sites-available/%(sitename)s.orig || '
        'sudo /etc/init.d/nginx restart'
        % env)


def _upload():
    """Archive the repo, upload it to the server, and unarchive."""
    require('hosts', provided_by=[production])
    local('git archive --prefix=%(path)s/ -v --format tar HEAD | '
          'bzip2 > %(path)s.tar.bz2' % env)
    put('%(path)s.tar.bz2' % env, '.')
    run('tar xfj %(path)s.tar.bz2' % env)
    local('rm %(path)s.tar.bz2' % env)


def _install_local_settings():
    """Install the server's local_settings.py file."""
    require('hosts', provided_by=[production])
    # Install the local settings from the resources directory.
    run('cp %(path)s/resources/django/%(sitename)s-local_settings.py '
        '%(path)s/www/server/local_settings.py' % env)


def _upload_static_files():
    """Tell Django to (locally) collect all needed static files and upload
    and unpack them."""
    require('hosts', provided_by=[production])
    local("rm -fr www/collected-static")
    local("mkdir www/collected-static")
    local("cd www && python manage.py collectstatic --noinput -v0")
    # local("cd www && python manage.py compress --force")
    local('tar cfvj %(path)s-static.tar.bz2 www/collected-static' % env)
    put('%(path)s-static.tar.bz2' % env, '.')
    run('cd %(path)s && tar xfj ../%(path)s-static.tar.bz2' % env)
    local("rm -fr www/collected-static %(path)s-static.tar.bz2" % env)


def x_idiot_check():
    print('You want me to update the live website without running tests..?')
    print('Only use this for trivial changes!')
    idiotCheck = raw_input("Are you sure? (Type 'yes') ").strip()
    if idiotCheck == 'yes':
        print('OK... on your head be it...')
    else:
        abort('Idiot test failed.')


def _deploy(test=True):
    """Deploy the website and run the tests if C{test} is C{True}."""
    _upload()
    _upload_static_files()
    # _make_virtualenv()
    # _install_dependencies()
    _install_local_settings()
    _update_init()
    _update_nginx()
    # with settings(warn_only=True):
        # The site may not be running, ignore any error.
        # stop_django()
    _replace_symlink()
    # start_django()
    _restart_nginx_if_config_has_changed()


# ------------------------- TOP-LEVEL COMMANDS -------------------------


def test():
    """
    Run the test suite locally. Ideally you'll be in a virtualenv.
    """
    env.shell = '/bin/bash -l -c'
    local_settings = os.path.exists('fluidinfo/local_settings.py')
    if local_settings:
        print('Backing up local_settings.py')
        # make a backup of localsettings so we can restore it after the tests
        local('cp fluidinfo/local_settings.py fluidinfo/local_settings.py.old')
    # cp the example localsettings since they provide a working test setup
    local('cp fluidinfo/local_settings.example fluidinfo/local_settings.py')
    try:
        local('python fluidinfo/manage.py test', capture=False)
    finally:
        if local_settings:
            print('Restoring local_settings.py')
            # restore the localsettings back to their original form
            local('mv fluidinfo/local_settings.py.old '
                  'fluidinfo/local_settings.py')


def start_django():
    """Start the web service."""
    require('hosts', provided_by=[production])
    run('echo "Started Django via fab at `date`." >> django.log')
    run('sudo start %(sitename)s' % env)


def stop_django():
    """Stop the web service."""
    require('hosts', provided_by=[production])
    run('sudo stop %(sitename)s' % env)
    run('echo "Stopped Django via fab at `date`." >> django.log')


def restart_django():
    """Restart the web service."""
    require('hosts', provided_by=[production])
    run('sudo restart %(sitename)s' % env)


def start_nginx():
    """Start nginx."""
    run('sudo /etc/init.d/nginx start')


def stop_nginx():
    """Stop nginx."""
    run('sudo /etc/init.d/nginx stop')


def restart_nginx():
    """Restart nginx."""
    run('sudo /etc/init.d/nginx restart')


def deploy_without_testing():
    """
    Deploy the website on the live server without running the
    tests.
    """
    _deploy(test=False)


def deploy():
    """
    Wraps all the steps up to deploy to the live server.
    """
    _deploy()
