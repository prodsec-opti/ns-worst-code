from flask import Flask, request, render_template_string
import sqlite3

app = Flask(_name_)

# Initialize a simple SQLite database
def init_db():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
    conn.commit()
    conn.close()

# Vulnerable to SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vulnerable SQL query without parameterized inputs
        conn = sqlite3.connect("example.db")
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing Query: {query}")
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"Welcome, {user[1]}!"
        else:
            return "Invalid credentials!"

    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Vulnerable to XSS
@app.route('/profile', methods=['GET'])
def profile():
    # Assume 'name' is passed as a query parameter
    name = request.args.get('name', '')

    # Render unescaped user input (vulnerable to XSS)
    html = f"<h1>Welcome, {name}!</h1>"
    return render_template_string(html)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
