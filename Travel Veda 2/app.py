from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'your_secret_key'
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='travelveda'
    )
    return connection
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('signin'))
    return render_template('signup.html')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."
        
    return render_template('signin.html')
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signin'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itineraries WHERE user_id = %s", (user_id,))
    itineraries = cursor.fetchall()
    cursor.execute("""
        SELECT i.id, i.title, IFNULL(SUM(e.amount), 0) AS total_spent, i.budget
        FROM itineraries i
        LEFT JOIN expenses e ON i.id = e.itinerary_id
        WHERE i.user_id = %s
        GROUP BY i.id
    """, (user_id,))
    budgets = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', itineraries=itineraries, budgets=budgets)
@app.route('/view_itinerary')
def view_itinerary():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signin'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itineraries WHERE user_id = %s", (user_id,))
    itinerary = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('view_itinerary.html', itinerary=itinerary)
@app.route('/calendar')
def calendar():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signin'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itineraries WHERE user_id = %s", (user_id,))
    itineraries = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('calendar.html', itineraries=itineraries)
@app.route('/expense_tracker')
def expense_tracker():
    return render_template('expense_tracker.html')
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        profile_picture = request.files['profile_picture']
        email = request.form['email']
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        if profile_picture:
            profile_picture_path = f'static/uploads/{profile_picture.filename}'
            profile_picture.save(profile_picture_path)
            cursor.execute('UPDATE users SET profile_picture = %s WHERE id = %s', (f'uploads/{profile_picture.filename}', user_id))
        
        cursor.execute('UPDATE users SET email = %s WHERE id = %s', (email, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('profile'))
    
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('profile.html', user=user)
@app.route('/blogs')
def blogs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM blogs')
    blogs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('blogs.html', blogs=blogs)
@app.route('/blog/<int:blog_id>')
def blog_post(blog_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM blogs WHERE id = %s', (blog_id,))
    blog = cursor.fetchone()
    
    cursor.execute('SELECT * FROM comments WHERE blog_id = %s', (blog_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('blog_post.html', blog=blog, comments=comments)
@app.route('/create_blog_post', methods=['GET', 'POST'])
def create_blog_post():
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        content = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO blogs (title, summary, content) VALUES (%s, %s, %s)', (title, summary, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('blogs'))
    
    return render_template('create_blog_post.html')
@app.route('/add_comment/<int:blog_id>', methods=['POST'])
def add_comment(blog_id):
    comment = request.form['comment']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO comments (blog_id, content) VALUES (%s, %s)', (blog_id, comment))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('blog_post', blog_id=blog_id))


@app.route('/update_profile', methods=['POST'])
def update_profile():
    # Logic to handle profile update
    # For example, save the uploaded file and update user info in the database
    return redirect(url_for('profile'))

from flask import jsonify
@app.route('/itinerary/<int:itinerary_id>')
def itinerary_data(itinerary_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM itineraries WHERE id = %s', (itinerary_id,))
    itinerary = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return jsonify(itinerary)  # Use jsonify to return a proper JSON response

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('signin'))
if __name__ == '__main__':
    app.run(debug=True)
