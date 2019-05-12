from tea_site import create_app, db
from tea_site.models import *


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()