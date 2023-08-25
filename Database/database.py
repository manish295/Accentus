import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import os
import urllib.parse as urlparse

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

class Database:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=host,
                database=dbname,
                user=user,
                password=password,
                port=port
            )
            self.cur = self.conn.cursor()
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS users(
                        user_id serial PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    );
                    
            ''')
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS stress (
                        id serial PRIMARY KEY,
                        user_id INT NOT NULL,
                        stress TEXT NOT NULL,
                        FOREIGN KEY(user_id)
                            REFERENCES users(user_id)
                            ON DELETE CASCADE
                    );
            ''')

            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS posts (
                        post_id serial PRIMARY KEY,
                        user_id INT NOT NULL,
                        title TEXT NOT NULL,
                        full_desc TEXT NOT NULL,
                        stress_level TEXT NOT NULL,
                        FOREIGN KEY(user_id)
                            REFERENCES users(user_id)
                            ON DELETE CASCADE
                    );
            ''')

            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS comments (
                        comment_id serial PRIMARY KEY,
                        post_id INT NOT NULL,
                        user_id INT NOT NULL,
                        comment TEXT NOT NULL,
                        FOREIGN KEY(post_id)
                            REFERENCES posts(post_id)
                            ON DELETE CASCADE
                    );
            ''')


        except Exception as err:
            print(err)
            self.close()

    
    def verify_password(self, username, password):
        try:
            self.cur.execute("SELECT user_id, password FROM users WHERE username = %(username)s", {"username": username})
            results = self.cur.fetchall()
            if len(results) == 0:
                print("user does not exist")
                return False
            else:
                for pwd in results:
                    if check_password_hash(pwd[1], password):
                        return pwd[0]
                print("incorrect password")
                return False

        except Exception as err:
            print(err)
            self.close()

    def add_user(self, username, password):
        try:
            password = generate_password_hash(password)
            self.cur.execute("INSERT INTO users(username, password) VALUES(%(username)s, %(password)s)", {'username': username, 'password': password})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def tag_user(self, user_id, stress_level):
        try:
            self.cur.execute("INSERT INTO stress(user_id, stress) VALUES(%(user_id)s, %(stress_level)s)", {'user_id': user_id, 'stress_level': stress_level})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def alter_stress_level(self, user_id, stress_level):
        try:
            self.cur.execute("UPDATE stress SET stress = %(stress_level)s WHERE user_id = %(user_id)s", {'stress_level': stress_level, 'user_id': user_id})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def check_if_already_tagged(self, user_id):
        try:
            self.cur.execute("SELECT * FROM stress WHERE user_id=%(user_id)s", {"user_id": user_id})
            result = self.cur.fetchall()
            if len(result) == 0:
                return False
            else:
                return True
        except Exception as err:
            print(err)
            self.close()
    
    def add_post(self, user_id, title, full_desc):
        try:
            stress_level = self.get_user_stress(user_id)
            self.cur.execute("INSERT INTO posts(user_id, title, full_desc, stress_level) VALUES(%(user_id)s, %(title)s, %(full_desc)s, %(stress_level)s)", {'user_id': user_id, 'title': title, 'full_desc': full_desc, 'stress_level': stress_level})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def add_comment(self, post_id, user_id, comment):
        try:
            self.cur.execute(
                "INSERT INTO comments(post_id, user_id, comment) VALUES(%(post_id)s, %(user_id)s, %(comment)s)",
                {'post_id': post_id, 'user_id': user_id, 'comment': comment})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    
    def get_username(self, user_id):
        try:
            self.cur.execute("SELECT username FROM users WHERE user_id= %(user_id)s", {'user_id': user_id})
            result = self.cur.fetchall()
            if len(result) == 0:
                return None
            result = result[0][0]
            return result
        except Exception as err:
            print(err)
            self.close()

    def get_comments(self, post_id):
        try:
            self.cur.execute("SELECT user_id, comment FROM comments WHERE post_id=%(post_id)s", {'post_id': post_id})
            results = self.cur.fetchall()
            if len(results) == 0:
                return None
            else:
                data = []
                for result in results:
                    user_id = result[0]
                    name = self.get_username(user_id)
                    comment = result[1]
                    data.append({'name': name, 'comment': comment})
                return data
        except Exception as err:
            print(err)
            self.close()

    def get_posts(self, stress_level):
        try:
            self.cur.execute("SELECT post_id, title, user_id FROM posts WHERE stress_level = %(stress_level)s", {"stress_level": stress_level})
            results = self.cur.fetchall()
            if len(results) == 0:
                return None 
            p = []

            length = len(results)
            for x in range(0, length):
                dicts = {"post_id" : results[x][0], "title": results[x][1], "user_id": results[x][2]}
                p.append(dicts)
            

            return p

        except Exception as err:
            print(err)
            self.close()
    

    def get_post_desc(self, post_id):
        try:
            self.cur.execute("SELECT user_id, full_desc, title FROM posts WHERE post_id = %(post_id)s", {"post_id": post_id})
            result = self.cur.fetchall()
            if len(result) == 0:
                return None
            result = result[0]
            r_dict = {}
            r_dict["full_desc"] = result[1]
            r_dict["user_id"] = result[0]
            r_dict["title"] = result[2]
            return r_dict
            
        
        except Exception as err:
            print(err)
            self.close()

    def get_user_stress(self, user_id):
        try:
            self.cur.execute("SELECT stress FROM stress WHERE user_id=%(user_id)s", {'user_id': user_id})
            results = self.cur.fetchall()
            if len(results) == 0:
                return None
            result = results[0]
            result = result[0]
            return result
        
        except Exception as err:
            print(err)
            self.close()
    
    def get_users(self, intensity=None):
        try:
            if intensity == None:
                self.cur.execute("SELECT username FROM users")
                results = self.cur.fetchall()
                if len(results) == 0:
                    return None
                r = []
                for name in results:
                    r.append(name[0])
                return r
            else:
                self.cur.execute("SELECT user_id FROM stress WHERE stress = %(intensity)s", {"intensity": intensity})
                results = self.cur.fetchall()
                if len(results) == 0:
                    return None
                r = []
                for id in results:
                    r.append(id[0])
                return r
        except Exception as err:
            print(err)
            self.close()

    

    def close(self):
        self.conn.close()

