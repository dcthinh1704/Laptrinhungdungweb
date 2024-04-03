from flask import render_template, url_for, flash, redirect, request, send_file, send_from_directory, session, jsonify
from app import app, socket
import os
import sqlite3  
import bcrypt
import uuid
from werkzeug.utils import secure_filename
import re
#Import required library      





# Settings the utils
curr_dir = os.path.dirname(os.path.abspath(__file__))
print(curr_dir)

def is_valid_random_string(random_string):
    # Check if the random string matches the expected format (you can adjust this based on your requirements)
    return len(random_string) == 32 and all(c in '0123456789abcdef' for c in random_string)


# Checks file extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# ConnectDB
def getDB():
    conn = sqlite3.connect(os.path.join(curr_dir, "openu.db"))
    cursor = conn.cursor()
    return cursor, conn


# Register route -----------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    try:
        if request.method == "POST":
            emailAddr = request.form['email'].strip()
            username = request.form['username'].strip()
            password = request.form['password'].strip()

            cursor, conn = getDB()
            rows = cursor.execute("SELECT username FROM user WHERE emailAddr = ?", (emailAddr,)).fetchall()

            if rows:
                message = "User already exists"
            else:
                # Generate ID and hash password
                id = str(uuid.uuid4())
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                print(hashed_password)

                # Create sessions
                session['loggedin'] = True
                session['id'] = id


                # Adding data to db
                query = "INSERT INTO user (id, username, emailAddr, password) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (id, username, emailAddr, hashed_password))
                conn.commit()

                # Create folder to save user's uploads
                user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], id)
                if not os.path.exists(user_upload_folder):
                    os.makedirs(user_upload_folder)

                message = "Registration successful"
                return redirect('/home')
    # Catch error
    except Exception as error:
        print(f"ERROR: {error}", flush=True)
        return "You broke the server :(", 400

    return render_template("register.html", message=message)



# Login route -----------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if (request.method == "POST"):

            emailAddr = request.form['email'].strip()
            password = request.form['password'].strip()

            # Get user data
            cursor, conn = getDB()
            user_info = cursor.execute("SELECT id, password FROM user WHERE emailAddr = ?",(emailAddr,)).fetchone()

            if user_info:
                id, hashed_password = user_info

                # Check if password is equal to hash
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    session['loggedin'] = True
                    session['id'] = id
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],session.get('id'))
                    #notes_list = os.listdir(file_path)

                    return redirect('/home')   
                else:
                     return render_template('login.html', message="Wrong Email or Password aa")
            else:
                return render_template('login.html', message="Wrong Email or Password gg")
        return render_template("login.html")
    except Exception as error:
        print(f"ERROR: {error}", flush=True)
        return "You broke the server :(", 400


@app.route("/")
@app.route("/home")
def home():
    if session.get('loggedin') == True:
        cursor, conn = getDB()
        id = session['id']
        cursor.execute("SELECT id FROM user WHERE id = ?",(id,)).fetchone()
        if id:        
            blog_info = cursor.execute("SELECT title, content FROM blogPosts WHERE publish = 1 ORDER BY RANDOM() LIMIT 5").fetchall()

            #print(blog_info)
            return render_template('index.html', blog_info=blog_info)
        return redirect('/login')
    else:
        return redirect('/login')




# Profile route -----------------------------------------------
@app.route('/profile')
def profile():
    if session.get('loggedin') == True:
        cursor,conn = getDB()
        id = session['id']
        
        cursor.execute("SELECT id FROM user WHERE id = ?",(id,)).fetchone()
        if id:   
            userName = cursor.execute("SELECT username FROM user WHERE id = ?",(id,)).fetchone()
            username = userName[0]
            print(username)
            blog_info = cursor.execute("SELECT id, title, authorname, publish FROM blogPosts WHERE userID = ?",(id,)).fetchall()
            
            print(blog_info)

            # Render avatar for 
            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], id)
            avatar_path_full = avatar_path + '/avatar.jpg'
            print(avatar_path_full)     
            if os.path.exists(avatar_path):
                profile_pic = id + '/' + 'avatar.jpg'


            return render_template('profile.html', username=username, blog_info=blog_info,profile_pic=profile_pic)
        return redirect('/login')
    else:
        return redirect('/login')


# Settings user information route -------------------------------
@app.route('/settings', methods=["GET", "POST"])
def settings():
    id = session.get('id')
    cursor, conn = getDB()
    
    # Check if id exist in database
    cursor.execute("SELECT id FROM user WHERE id = ?",(id,)).fetchone()
    if not id:        
        return redirect(url_for('login'))  # Redirect to login page if user's id doesn't exist
    

    user_info = cursor.execute("SELECT name, username, emailAddr, password FROM user WHERE id = ?", (id,)).fetchone()

    # Setting the data of user to output to screen
    name, username, emailAddr, hashed_password = user_info
    print(hashed_password)


    profile_pic = None

    # Change the upload folder to inside the user id
    user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], id)

    if request.method == "POST":
        
        # Check if the user sent updated information for name, username, or email
        if 'name' in request.form:
            new_name = request.form['name']
            cursor.execute("UPDATE user SET name = ? WHERE id = ?", (new_name, id))
            conn.commit()
            name = new_name

        if 'username' in request.form:
            new_username = request.form['username']
            cursor.execute("UPDATE user SET username = ? WHERE id = ?", (new_username, id))
            conn.commit()
            username = new_username

        if 'email' in request.form:
            new_email = request.form['email']
            cursor.execute("UPDATE user SET emailAddr = ? WHERE id = ?", (new_email, id))
            conn.commit()
            emailAddr = new_email   

        if 'password' in request.form:
            new_password = request.form['password']
            if new_password:

                if bcrypt.checkpw(new_password.encode('utf-8'), hashed_password):
                    print('Please provide a password different from your old one!')
                    return redirect(request.url)
                else:   
                    new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("UPDATE user SET password = ? WHERE id = ?", (new_hashed_password, id))
                    conn.commit()
                    password = new_hashed_password
            else:
                pass
    

        # Check if the user upload a requests with a profile pic
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename('avatar.jpg')
            file_path = os.path.join(user_upload_folder, filename)
            file.save(file_path)
            profile_pic = id + '/' + filename
            print(profile_pic)

            flash('File uploaded successfully')
            return render_template('settings.html', name=name, username=username, email=emailAddr, profile_pic=profile_pic)  # Redirect to the settings page
        
        else:
            flash('Invalid file format.')
            return redirect(request.url)
        

    avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], id)
    avatar_path_full = avatar_path + '/avatar.jpg'
    print(avatar_path_full)     
    if os.path.exists(avatar_path):
        profile_pic = id + '/' + 'avatar.jpg'

    # Render the page with the user info that we retrieve
    return render_template('settings.html', name=name, username=username, email=emailAddr, profile_pic=profile_pic)

# Logout route -----------------------------------------------
@app.route('/logout')
def logout():
    session.pop('loggedin')
    session.pop('id')
    return redirect('/login')


# Called to when create blog ----------------------------------
@app.route("/save_blog", methods=["GET", "POST"])
def save_blog():

    id = session.get('id')
    cursor, conn = getDB()
    
    # Check if id exist in database
    cursor.execute("SELECT id FROM user WHERE id = ?",(id,)).fetchone()
    if not id:        
        return redirect(url_for('login'))  # Redirect to login page if user's id doesn't exist

    # Retrieve data from database based on the id
    user_info = cursor.execute("SELECT id, username FROM user WHERE id = ?", (id,)).fetchone()
    username = user_info[1]



    if (request.method == "POST"):
        try:
            blogTitle = request.json.get('blogTitle')
            blogContent = request.json.get('blogContent')

            # Execute and save the database
            cursor.execute("INSERT INTO blogPosts (userID, title, content, authorname) VALUES (?, ?, ?, ?)", (id, blogTitle, blogContent, username,))
            conn.commit()
            conn.close()

            return "Blog successfully upload!"
        
        except Exception as error:
            print(f"ERROR: {error}", flush=True)
            return "You broke the server :(", 400
        
    else:
        return None
    

# Route will be called when update publish or not
@app.route("/update_published", methods=["POST"])
def published():
    id = session.get('id')
    cursor, conn = getDB()
    
    # Check if id exist in database
    cursor.execute("SELECT id FROM user WHERE id = ?",(id,)).fetchone()
    if not id:        
        return redirect(url_for('login'))  # Redirect to login page if user's id doesn't exist

    try:
        blogID = request.json.get('blogID')
        published = request.json.get('published')
        
        cursor.execute("UPDATE blogPosts SET publish = ? WHERE id = ?", (published, blogID))
        conn.commit()
        conn.close()
        return 'Updated'

    except Exception as error:
        print(f"ERROR: {error}", flush=True)
        return "You broke the server :(", 400
    
#-------------------------------- Will look later -----------------------------------------------
# Routes to render out each individual blog when press on the title of a blog
'''
@app.route('/blog/<int:blog_id><string:random_string>')
def view_blog(blog_id, random_string):
    # Validate the random string to ensure it matches the expected format
    if not is_valid_random_string(random_string):
        return render_template('error.html', message='Invalid URL'), 400

    cursor, conn = getDB()

    # Fetch the blog post from the database based on the provided blog_id
    blog_post = cursor.execute("SELECT title, content FROM blogPosts WHERE id = ?", (blog_id,)).fetchone()

    # Check if the blog post exists
    if blog_post:
        return "hello"
    else:
        # If the blog post does not exist, render an error page or redirect to another page
        return "lmao", 404
'''
#-----------------------------------------------------------------------------------------------   

# Routes for generating new chat by searching for users
from flask import jsonify

@app.route('/new_chat', methods=["POST"])
def new_chat():
    id = session.get('id')
    cursor, conn = getDB()
    
    # Check if id exists in the database
    if not id:        
        return redirect(url_for('login'))  # Redirect to login page if the user's id doesn't exist
    
    try:
        if request.method == "POST":
            if 'search_input' in request.form:
                search_input = request.form['search_input']
                # Check if the input matches the format of an email address
                if re.match(r'^[\w\.-]+@[\w\.-]+$', search_input):
                    # Search for the user in the database based on the provided email address
                    recipient_info = cursor.execute("SELECT id, username, emailAddr FROM user WHERE emailAddr = ?", (search_input,)).fetchone()
                else:
                    # Search for the user in the database based on the provided username
                    recipient_info = cursor.execute("SELECT id, username, emailAddr FROM user WHERE username = ?", (search_input,)).fetchone()
                    
                if recipient_info:
                    recipient_id, recipient_username, recipient_email = recipient_info
                    # Check if a chat already exists between the current user and the recipient
                    chat_exists = cursor.execute("SELECT id FROM chat WHERE (userID1 = ? AND userID2 = ?) OR (userID1 = ? AND userID2 = ?)", (id, recipient_id, recipient_id, id)).fetchone()
                    if chat_exists:
                        return jsonify({'error': 'Chat already exists'}), 400
                    else:
                        # Proceed with creating a new chat
                        # First, insert the new chat into the database
                        
                        chat_id = str(uuid.uuid4())

                        cursor.execute("INSERT INTO chat (id, userID1, userID2) VALUES (?, ?, ?)", (chat_id, id, recipient_id))
                        conn.commit()
                        # Retrieve the chat ID of the newly created chat
                        new_chat_id = cursor.lastrowid

                        
                        # Create room id equal to message id to make eassier query nd understanding
                        chat_roomID = chat_id
                        cursor.execute("INSERT INTO messages (room_id) VALUES (?)", (chat_roomID))


                        return jsonify({'success': 'New chat created successfully', 'chat_id': new_chat_id}), 200
                else:
                    return jsonify({'error': 'User not found'}), 404

    except Exception as error:
        print(f"ERROR: {error}", flush=True)
        return "Internal Server Error", 500

@app.route('/new_chat_form', methods=["GET", "POST"])
def new_chat_form():
    return render_template('test_chatHTML.html')