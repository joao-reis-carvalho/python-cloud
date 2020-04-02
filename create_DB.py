import sqlite3

conn = sqlite3.connect('project.db')

c = conn.cursor()

c.execute('''CREATE TABLE apirelease (
                [buildtime] date,
                [version] varchar(30) primary key,
                [links] varchar2 (30),
                [methods] varchar2 (30))''')

c.execute('''INSERT INTO apirelease values ('2017-01-01 10:00:00',
            "v1", "/api/v1/users", "get, post, put, delete")''')

c.execute('''CREATE TABLE users (
                [username] varchar2 (20),
                [email] varchar2 (30),
                [password] varchar2 (30),
                [full_name] varchar (30),
                [id] integer primary key)''');

c.execute('''INSERT INTO users values ('manish_kut',
            "manishest@gmail.com", "manish123", "Manish Kutrapali", 1)''')

c.execute('''INSERT INTO users values ('sheldon_smart',
            "sheldon@gmail.com", "bazinga", "Sheldon Whatever", 2)''')

c.execute('''CREATE TABLE tweets (
                [id] integer primary key autoincrement,
                [username] varchar2 (30),
                [body] varchar2 (30),
                [tweet_time] date)''');

conn.commit()
