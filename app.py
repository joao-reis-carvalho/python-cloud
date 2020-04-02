from flask import Flask
from flask import jsonify, request
from flask import abort, make_response
import json
import sqlite3
from time import gmtime, strftime

app = Flask (__name__)

def list_users():
    conn=sqlite3.connect('project.db')
    print("Opened database successfully");
    api_list=[]
    cursor = conn.execute ("SELECT username, full_name, email, password FROM users")
    for row in cursor:
        a_dict={}
        a_dict['username'] = row[0]
        a_dict['full_name'] = row[1]
        a_dict['email'] = row[2]
        a_dict['password'] = row[3]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'user_list': api_list})

def user_filter():
        query_parameters = request.args

        id = query_parameters.get('id')

        query = "SELECT username, password FROM users WHERE"
        to_filter = []

        if id:
            query += ' id=?'
            to_filter.append(id)
        if not (id):
            return page_not_found(404)

        query = query + ';'

        conn = sqlite3.connect('project.db')
        cur = conn.cursor()

        results = cur.execute(query, to_filter).fetchall()

        return jsonify(results)

def add_user(new_user):
    conn = sqlite3.connect('project.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users where username=? or email=?",(new_user['username'],new_user['email']))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        cursor.execute('''INSERT INTO users (username, email, password, full_name, id) values(?,?,?,?,?)''',(new_user['username'],new_user['email'],new_user['password'], new_user['full_name'], new_user['id']))
        conn.commit()
        return "Success"
    conn.close()
    return jsonify(a_dict)

def del_user(del_user):
    conn = sqlite3.connect('project.db')
    print ("Opened database successfully");
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? ", (del_user,))
    data = cursor.fetchall()
    print ("Data" ,data)
    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("DELETE FROM users WHERE username==?", (del_user,))
        conn.commit()
        return "Success"

def upd_user(user):
    conn = sqlite3.connect('project.db')
    print ("Opened database successfully")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=? ", (user['id'],))
    data = cursor.fetchall()
    print (data)
    if len(data) == 0:
        abort(404)
    else:
        key_list=user.keys()
        for i in key_list:
            if i != "id":
                print (user, i)
                # cursor.execute('''UPDATE users set {0}0? WHERE id=? ''', (i, user[i], user['id']))
                cursor.execute('''UPDATE users SET {0}=? WHERE id=?'''.format(i), (user[i], user['id']))
                conn.commit()
    return "Success"

def list_tweets():
    conn=sqlite3.connect('project.db')
    print("Opened database successfully");
    api_list=[]
    cursor = conn.cursor()
    cursor.execute ("SELECT * FROM tweets")
    data = cursor.fetchall()
    for row in data:
        tweets={}
        tweets['id'] = row[0]
        tweets['Tweet By'] = row[1]
        tweets['Body'] = row[2]
        tweets['Timestamp'] = row[3]
        api_list.append(tweets)
    conn.close()
    return jsonify({'tweets_list': api_list})

def add_tweet(new_tweets):
    conn = sqlite3.connect('project.db')
    print ("Opened database successfully");
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? ", (new_tweets['username'],))
    data = cursor.fetchall()
    if len(data)==0:
        abort(404)
    else:
        cursor.execute('''INSERT INTO tweets (username, body, tweet_time) values(?,?,?)''', (new_tweets['username'], new_tweets['body'], new_tweets['tweet_time']))
        conn.commit()
        return "Success"

def list_tweet(user_id):
    print (user_id)
    conn = sqlite3.connect('project.db')
    print ("Opened database successfully");
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tweets WHERE id=?", (user_id,))
    data = cursor.fetchall()
    print(data)
    if len(data) == 0:
        abort(404)
    else:
        user = {}
        user['id'] = data[0][0]
        user['username'] = data[0][1]
        user['body'] = data[0][2]
        user['tweet_time'] = data[0][3]
    conn.close()
    return jsonify(user)

@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('project.db')
    print ("Opened database successfully");
    api_list=[]
    cursor = conn.execute("SELECT buildtime, version, methods, links FROM apirelease")
    for row in cursor:
        a_dict = {}
        a_dict['buildtime'] = row[0]
        a_dict['version'] = row[1]
        a_dict['methods'] = row[2]
        a_dict['links'] = row[3]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'api_version': api_list}), 200

@app.route("/api/v1/users", methods=['GET'])
def get_users():
    return list_users()

@app.route("/api/v1/user", methods=['GET'])
def get_user_id():
    return user_filter()

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'full_name': request.json.get('full_name',""),
        'password': request.json['password'],
        'id': request.json['id'],
    }
    return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
        abort(400)
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print (user)
    return jsonify({'status': upd_user(user)}), 200

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

@app.route('/api/v2/tweets', methods=[('POST')])
def add_tweets():
    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['tweet_time']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    print (user_tweet)
    return jsonify({'status': add_tweet(user_tweet)}), 201

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
