import sqlalchemy as db
from sqlalchemy import select

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
    race = select_all_result.fetchall()[0][3]
    print(race)
    if select_all_result is False:
        insertion_query = stats.insert().values([
            {'username': username, 'distance': distance, 'races': 1, 'rate': distance / race}
        ])
        connection.execute(insertion_query)
    else:
        select_all_query = db.select([stats]).filter_by(username=username)
        select_all_result = connection.execute(select_all_query)
        dist = select_all_result.fetchall()[0][2] + distance
        race += 1
        update_query = db.update(stats).where(stats.columns.username == username).values(distance=dist, races=race,
                                                                                            rate=dist / race)
        connection.execute(update_query)


# select_all_query = db.select([stats]).filter_by(username='eduardus1')
# select_all_result = connection.execute(select_all_query)
#
# print(select_all_result.fetchall()[0][2])
