'''
Created on Aug 19, 2014

@author: Kristian
'''
from fabric.api import *
from fabric.colors import green, red

def celery():
    print(green("Starting Celery worker..."))
    local("celery -A xavee worker -l info")

def redis():
    print(green("Starting Redis server..."))
    local("redis-server /usr/local/etc/redis.conf")

def runserver():
    print(green("Starting local server..."))
    local("python manage.py runserver")
    
def migrate():
    with settings(warn_only=True):
        print(green("Migrating local DB..."))
        local("python manage.py schemamigration --auto application")
        local("python manage.py schemamigration --auto blog")
        local("python manage.py schemamigration --auto referrer")
        local("python manage.py migrate")

def test():
    print("Beginning unit tests...")
    local("python manage.py test")
    print("Beginning functional tests...")
    local("python functional_tests.py")

def deploy():
    print(green("Starting local deployment process..."))
    test()
    
    