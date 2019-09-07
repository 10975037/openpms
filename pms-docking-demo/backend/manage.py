from app.models import db
from app.utils.factory import create_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
