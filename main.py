from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import subprocess


app = Flask(__name__)
app.config['SECRET_KEY'] = 'prudhviweb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# MySQL configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',        # Your MySQL username
    'password': 'prudhvi',        # Your MySQL password
    'database': 'users' # Your database name
}

# Initialize MySQL connection
mysql_conn = mysql.connector.connect(**mysql_config)

db = SQLAlchemy(app)  # Create an instance of SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))
    
@app.route('/')
def index():
    user_info = None

    if 'email' in session:
        email = session['email']

        # Use SQLAlchemy to check if the user's account exists in the database
        user = User.query.filter_by(email=email).first()

        if user:
            user_info = {'email': email, 'image_url': '/static/starboy.jpg'}  # Provide user image URL here

    return render_template('index.html', user_info=user_info)


@app.route('/public_index')
def public_index():
    return render_template('index.html', user_info=None)

def check_user_exists_php(email):
    # Define the PHP command to execute
    php_script = """
    <?php
    $email = %s;  // Escape the email value
    $conn = new mysqli("localhost", "root", "prudhvi", "users");
    $query = "SELECT * FROM users WHERE email='$email'";
    $result = $conn->query($query);
    $user_exists = $result->num_rows > 0;
    $conn->close();
    echo $user_exists;
    ?>
    """ % (subprocess.list2cmdline([email]))  # Escape the email value

    # Execute the PHP script and capture the output
    php_output = subprocess.run(['php', '-r', php_script], stdout=subprocess.PIPE, text=True).stdout.strip()

    # Convert PHP output to a boolean
    return php_output == '1'
   
# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_error = False

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql_conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and user[2] == password:
            session['email'] = email
            return redirect(url_for('index'))
        else:
            login_error = True

    # Render the login.html template without an error message initially
    return render_template('login.html', login_error=login_error)
# Pass login_error to template


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']
        new_password = request.form['password']

        cur = mysql_conn.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (new_name, new_email, new_password))
        mysql_conn.commit()
        cur.close()

        session['email'] = new_email

        return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/album_details/<int:album_id>')
def album_details(album_id):
    # Here, you can retrieve album details based on album_id from the database or any other data source
    # For demonstration purposes, we will use a dictionary to store album details
    albums = {
        1: {
            'name': 'Starboy',
            'artist': 'The Weeknd',
            'songs': ["Starboy","Party Monster","False Alarm","Reminder","Rockin","Six Feet Under"],
            'image_url': '/static/starboy.jpg',
            'year':2016,
        },
        2: {
            'name': 'Fighting Demons',
            'artist': 'Juice Wrld',
            'songs': [	"Burn",	"Already Dead",	"Rockstar in His Prime","My Life in a Nutshell"],
            'image_url': '/static/fightingdemons.jpg',
            'year':2022,
        },
        3: {
            'name': 'Beauty Behind the Madness',
            'artist': 'The Weeknd',
            'songs': ["The Hills","Acquainted","Earned It (Fifty Shades of Grey)","As You Are","Dark Times (featuring Ed Sheeran)"],
            'image_url': '/static/beauty.jpg',
            'year':2015,
        },
        4: {
            'name': 'SKINS',
            'artist': 'XXXTentacion',
            'songs': ["Guardian Angel",	"Bad!",	"Staring at the Sky",	"I Don't Let Go"],
            'image_url': '/static/skins.png',
            'year':2018,
        },
        # Add more albums and their details as needed
    }

    album_details = albums.get(album_id)
    if album_details:
        return render_template('album_details.html', album_details=album_details)
    else:
        return "Album not found", 404

# artist-details
@app.route('/artist_details/<string:artist_name>')
def artist_details(artist_name):
    # Here, you can retrieve artist details based on the artist_name from the database or any other data source
    # For demonstration purposes, we will use a dictionary to store artist details
    artists = {
        "The Weeknd": {
            'name': 'The Weeknd',
            'genre': 'R&B',
            'origin':'Toronto, Ontario,Canada',
            'description': 'Abel Makkonen Tesfaye, known professionally as the Weeknd, is a Canadian singer, songwriter, and record producer. He is noted for his unconventional music production, artistic reinventions, and his signature use of the falsetto register',
            'image_url': '/static/weeknd.jpg',
        },
        "Juice Wrld": {
            'name': 'Juice Wrld',
            'genre': 'Hip Hop/Rap',
            'origin':'Homewood, Illinois, U.S',
            'description': 'Jarad Anthony Higgins, known professionally as Juice Wrld, was an American rapper, singer, and songwriter. He was a leading figure in the emo rap and SoundCloud rap genres which garnered mainstream attention during the mid-to-late 2010s',
            'image_url': '/static/juicewrld.jpg',
        },
        "XXXTentacion": {
            'name': 'XXXTentacion',
            'genre': 'Hip Hop/Rap',
            'origin':'Broward County, Florida, U.S',
            'description': 'Jahseh Dwayne Ricardo Onfroy, known professionally as XXXTentacion, was an American rapper and singer-songwriter',
            'image_url': '/static/xxxtentacion.jpg',
        },
        # Add details for other artists
    }

    artist_details = artists.get(artist_name)
    if not artist_details:
        return "Artist not found"

    return render_template('artist_details.html', artist_details=artist_details)


if __name__ == '__main__':
    app.run(debug=True)