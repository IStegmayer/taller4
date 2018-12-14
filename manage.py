#! /usr/bin/env python

from rcity import app, db, migrate
from flask_script import Manager, prompt_bool
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    db.create_all()
    print('Initialized the database.')

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop the current DB?"):
        db.drop_all()
        print('DB dropped.')
    else:
        print('Drop aborted.')

if __name__ == '__main__':
    manager.run()
