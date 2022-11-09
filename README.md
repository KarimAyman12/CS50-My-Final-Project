# PIGEON EMAIL - CS50x Final Project
#### Video Demo:  https://youtu.be/gJU2xEQmU-c
## Explaining the project
My final project is an Email website that allows users to send, receive and manage emails.
The project is based on a pyhton framework "Flask" combined with SQLite, JavaScript, CSS and Bootstrap to make it more aesthetic and Interactive.
All information about users, emails are stored in project.db.
I used CS50.SQL extension to connect the database to application and sqlite3 to manager it.

## Features

- [Flask Web Framework](https://flask.palletsprojects.com/en/2.2.x/)
- [SQLite](https://www.sqlite.org/index.html)
- [CS50 Library](https://github.com/cs50/libcs50)
- [Python](https://www.python.org/)
- [HTML](https://html.com/)
- [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
- [Bootstrap](https://getbootstrap.com/)
- [JavaScript](https://www.javascript.com/)

I've used Flask web framework python-based with Sqlite Manage SQL databases,
i used cs50.SQL object to configure CS50 Library to use SQLite database engine.
and of course i used python to build up the flask app besides HTML, CSS and Bootsrap to make the webpage more aesthetic, and with JavaScript to make it more interactive.

### Database:
I needed two tables for my database:

- First, table users. Which stores id as a primary key, username(Email) and hash (for password).

- Second, table emails. Which stores id as a primary key, sender, recipient, subject, body and timestamp.

### Routing

Each route checks if the user is authenticated. It means if correct mail and password were supplied. So for example a user cannot enter /compose route without registering or logging in.

### Sessions

The webpage uses sessions to confirm that user is registered. Once the user logins, his credentials are checked. Once everything passes a session is created (serialized and deserialized) and stored in the cookies. The server attaches user to subsequent requests, so the back-end can easily access the details, like emails details: sender, recipient, etc.

### Database

Database stores all users, emails. The tables, like emails uses foreign keys to relate users to emails.
For example, emails use username in users table as a foriegn key to relate an email to its sender or its recipient.
```python
@app.route("/sent")
@login_required
def sent():
    """Show Sent Emails"""
    userID = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userID)
    username = usernameDB[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE sender = ?", username)
    return render_template("sent.html", emails=emails)
```

Validations for regesterition:
``` python
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not email or not password or not confirm :
            return apology("No Empty Fields !")

        if password != confirm :
            return apology("Password Do Not Match !")

        hash = generate_password_hash(password)

        try:
            #INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
            newUser = db.execute("INSERT INTO users (username, hash) VALUES (? ,?)", email, hash)
        except:
            return apology("Email Already Used !")
```
## Animations and Aesthetics
the Webpage includes Floating placeholder implemented by bootstrap's floating placeholder by adding in Register, Login Routes.
``` HTML
<div class="form-floating mb-3" style="width:250px; margin:auto;">
            <input type="email" class="form-control" id="floatingInput" name="username" placeholder="name@example.com">
            <label for="floatingInput">Email Address</label>
        </div>
        <div class="form-floating mb-3" style="width:250px; margin:auto;">
            <input class="form-control" id="floatingInput" name="password" placeholder="Password" type="password">
            <label for="floatingInput">Password</label>
        </div>
```

I have implemented animated colorful border in composing, replying forms using CSS animation attribute with hue-rotate() function.
``` CSS
.anim-frame
{
    background: linear-gradient(to right, var(--cores-dancantes));
    border-radius: 10px;
    position: relative;
    z-index: 999;
    animation: coresDancantes 2s linear infinite;

}
@keyframes coresDancantes {
    100% {
        filter: hue-rotate(360deg);
    }
}
```
## Interactivity
the webpage have a show password checkbox when logging in or registering, and it was implemented by JavaScript combined with CSS type attribute.

``` JavaScript
document.querySelector("#show-password").addEventListener("input", function() {
            document.querySelector('[name="password"]').type = this.checked ? "text" : "password";
            document.querySelector('[name="confirm"]').type = this.checked ? "text" : "password";
          });
```
the webpage also shows a message "No Received Emails Yet!" or "No Sent Emails Yet!" if there's no emails was loaded from the database, and this was implemented using JavaScript if condition statment.
```javascript
var x = document.getElementById("no_email");
        if(document.querySelectorAll('.email').length > 0){
            x.style.display = "none";
        }
```
I added a dynamic counter for emails, which is shown in inbox and sent routes by using CSS section counter by adding id = "counter" in the wanted element tag.
``` CSS
tbody
{
    counter-reset: section;
}
#counter::before
{
    counter-increment: section;
    content: counter(section);
}
```
## About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you, This is CS50.

- Where I get CS50 course?
https://cs50.harvard.edu/x/

[LinkedIn Karim Ayman](https://www.linkedin.com/in/karim-ayman-9711b0193)