'''
Created on Aug 19, 2014

@author: Kristian
'''
from fabric.api import *
from fabric.colors import green, red
from fabric.contrib import django

django.project('xavee')
from application import tasks


def celery():
    print(green("Starting Celery worker..."))
    local("celery -A xavee worker -l info")

def redis():
    print(green("Starting Redis server..."))
    local("redis-server /usr/local/etc/redis.conf")

def runserver():
    print(green("Starting local server..."))
    local("python manage.py runserver")
    
def makemessages():
    print(green("Generating translation files..."))
    local("django-admin.py makemessages -l ja --ignore=venv/*")
    
def compilemessages():
    print(green("Compiling translation files..."))
    local("django-admin.py compilemessages")
    
def collectstatic():
    print(green("Compressing JS/CSS and uploading statics to S3..."))
    django.settings_module('xavee.settings.deploy')
    local("python manage.py compress")
    local("python manage.py collectstatic")

def get_wr():
    print(green("Getting top 200 world ranking for all categories from iTunes..."))
    tasks.collect_all_ios_rankings(200)

def migrate():
    with settings(warn_only=True):
        print(green("Migrating local DB..."))
        local("python manage.py schemamigration --auto application")
        local("python manage.py schemamigration --auto blog")
        local("python manage.py schemamigration --auto referrer")
        local("python manage.py migrate")

def update_remote_wr():
    print(green("Dumping WorldRanking table..."))
    local("pg_dump -Fc --no-acl --no-owner -h localhost -U Kristian -t application_worldranking xavee_db > worldranking.dump")
    print(green("Uploading dump to Amazon S3..."))
    local("aws s3 cp --acl public-read worldranking.dump s3://xavee/")
    print(green("Restoring WorldRanking table into remote Heroku DB..."))
    local("heroku pgbackups:restore DATABASE 'https://s3-ap-northeast-1.amazonaws.com/xavee/worldranking.dump' --confirm xavee")
    print(green("Finally, deleting the dump from Amazon S3 and locally."))
    local("aws s3 rm s3://xavee/worldranking.dump")
    local("rm worldranking.dump")
    
# def update_category():
#     print(green("Dumping Category table..."))
#     local("pg_dump -Fc --no-acl --no-owner -h localhost -U Kristian -t application_category xavee_db > category.dump")
#     print(green("Uploading dump to Amazon S3..."))
#     local("aws s3 cp --acl public-read category.dump s3://xavee/")
#     print(green("Restoring Category table into remote Heroku DB..."))
#     local("heroku pgbackups:restore DATABASE 'https://s3-ap-northeast-1.amazonaws.com/xavee/category.dump' --confirm xavee")
#     print(green("Finally, deleting the dump from Amazon S3 and locally."))
#     local("aws s3 rm s3://xavee/category.dump")
#     local("rm category.dump")

def backup_db():
    with settings(warn_only=True):
        print(green("Backing up the DB..."))
        local("dropdb backup_xavee_db")
        local("createdb -O Kristian -T xavee_db backup_xavee_db")

def test():
    print("Beginning unit tests...")
    local("python manage.py test")
    print("Beginning functional tests...")
    local("python functional_tests.py")

def deploy():
    print(green("Starting full deployment process..."))
    test()
    
    