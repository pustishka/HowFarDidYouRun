import sqlalchemy as db

engine = db.create_engine('sqlite:///stats.db')
connection = engine.connect()
metadata = db.MetaData()
stats = db.Table('stats', metadata,
                 db.Column('user_id', db.Integer, primary_key=True),
                 db.Column('username', db.Text),
                 db.Column('distance', db.Integer),
                 db.Column('races', db.Integer),
                 db.Column('rate', db.Float))
metadata.create_all(engine)