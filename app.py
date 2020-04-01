from flask import Flask
from flask import jsonify, request
import json
import sqlite3

app = Flask (__name__)

@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('Projects.db')
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

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route("/api/v1/users", methods=['GET'])
def get_users():
    return list_users()

def list_users():
    conn=sqlite3.connect('Users.db')
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

@app.route("/api/v1/user", methods=['GET'])
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

        conn = sqlite3.connect('Users.db')
        cur = conn.cursor()

        results = cur.execute(query, to_filter).fetchall()

        return jsonify(results)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
