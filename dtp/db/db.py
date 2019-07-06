from pony.orm import Database

provider ='postgres'
user='postgres'
password='123456'
host='127.0.0.1'
database='dtp'


db = Database(provider=provider,
              user=user, password=password,
              host=host, database=database)
