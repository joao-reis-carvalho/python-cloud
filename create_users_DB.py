import sqlite3

conn = sqlite3.connect('Users.db')

c = conn.cursor()

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

conn.commit()
