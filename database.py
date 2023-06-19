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


def insert_into_base(username, distance):
    select_all_query = db.select([stats]).filter_by(username=username)
    select_all_result = connection.execute(select_all_query)
    if select_all_result.fetchall() == []:
        insertion_query = stats.insert().values([
            {'username': username, 'distance': distance, 'races': 1, 'rate': distance / 1}
        ])
        connection.execute(insertion_query)
    else:
        select_all_query = db.select([stats]).filter_by(username=username)
        select_all_result = connection.execute(select_all_query)
        data = select_all_result.fetchall()
        race = data[0][3]
        dist = data[0][2] + distance
        race += 1
        update_query = db.update(stats).where(stats.columns.username == username).values(distance=dist, races=race,
                                                                                         rate=dist / race)
        connection.execute(update_query)
