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

def update_ranking():
    print(green("Dumping WorldRanking table..."))
    local("pg_dump -Fc --no-acl --no-owner -h localhost -U Kristian -t application_worldranking xavee_db > worldranking.dump")
    print(green("Uploading dump to Amazon S3..."))
    local("aws s3 cp --acl public-read worldranking.dump s3://xavee/")
    print(green("Restoring WorldRanking table into remote Heroku DB..."))
    local("heroku pgbackups:restore DATABASE 'https://s3-ap-northeast-1.amazonaws.com/xavee/worldranking.dump' --confirm xavee")
    print(green("Finally, deleting the dump from Amazon S3."))
    local("aws s3 rm s3://xavee/worldranking.dump")
    

def test():
    print("Beginning unit tests...")
    local("python manage.py test")
    print("Beginning functional tests...")
    local("python functional_tests.py")

def deploy():
    print(green("Starting local deployment process..."))
    test()
    
    