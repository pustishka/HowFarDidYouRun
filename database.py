import sqlalchemy as db

engine = db.create_engine('sqlite:///stats.db')  # create engine of sqlalchemy based on sqlite with db name 'stats'
connection = engine.connect()  # create connection
metadata = db.MetaData()
stats = db.Table('stats', metadata,
                 db.Column('user_id', db.Integer, primary_key=True),
                 db.Column('username', db.Text),
                 db.Column('distance', db.Integer),
                 db.Column('races', db.Integer),
                 db.Column('rate', db.Float))  # create all columns in data base


# method for getting stats
def get_stats():
    select_first_ten_query = db.select([stats])
    select_first_ten_results = connection.execute(select_first_ten_query)
    return select_first_ten_results


# method for insert data if that a new player or update if player exists in data base
def insert_into_base(username, distance):
    select_all_query = db.select([stats]).filter_by(username=username)  # get data filtered by 'username'
    select_all_result = connection.execute(select_all_query)
    if select_all_result.fetchall() == []:  # checking content of query
        insertion_query = stats.insert().values([
            {'username': username, 'distance': distance, 'races': 1, 'rate': round(distance / 1, 1)}
        ])  # rate equal (distance divide by 1)
        connection.execute(insertion_query)
    else:
        select_all_query = db.select([stats]).filter_by(username=username)
        select_all_result = connection.execute(select_all_query)
        data = select_all_result.fetchall()
        race = data[0][3]
        dist = data[0][2] + distance  # increment our distance
        race += 1  # if player exists we implement column value
        update_query = db.update(stats).where(stats.columns.username == username).values(distance=dist, races=race,
                                                                                         rate=round(dist / race, 1))
        # rate equal if player exists (distance divide by race value)
        connection.execute(update_query)
