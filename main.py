from flask import Flask, render_template, url_for, request, redirect, flash,session
# import sqlite3
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)




# configuration

app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.secret_key="secret_key"


database=SQLAlchemy(app)



# definition model


class User(database.Model):
    id= database.Column(database.Integer , primary_key=True, autoincrement=True)
    nom=database.Column(database.String(50), nullable=False)
    email=database.Column(database.String(100), nullable=False)
    password= database.Column(database.String(100), nullable=True)


# def database():
#     # creation + connection
#     conn=sqlite3.connect('CFAT.db')
    
#     # requete sql pour la creation d'une table
#     conn.execute('''
#                  create table IF NOT EXISTS user( 
#                  id INTEGER PRIMARY KEY AUTOINCREMENT,
#                  name VARCHAR(50),
#                  email VARCHAR(100),
#                  password VARCHAR(100)
                 
#                  )''')
#     conn.commit()
#     conn.close()
    
    
# database()
    



@app.route('/')
def index():
    
    
    # connection
    # conn= sqlite3.connect('CFAT.db')
    
    # excution
    # requete= conn.execute('select * from user')

    # users= requete.fetchall()
    # conn.commit()
    # conn.close()    
    return render_template('index.html', title="Acceuil")


@app.route('/propos')
def propos():
    
    return render_template('propos.html', title="propos")

@app.route('/contact')
def Contact():
    
    return render_template('contact.html', title="Contact")







@app.route('/login', methods=["POST", "GET"])
def login():
    
    if request.method=='POST':
        email= request.form['email']
        password= request.form['password'] 
        # connection
       
        try: 
            
           user= User.query.filter_by(email=email).first()
            
           if user and user.password==password:
                session['user_id']=user.id
                return redirect(url_for('index'))
           else:
               
                flash('password ou email incorrect', 'erreur')
   
            
        except:
            
            flash('erreur de recuparation de donnees', 'erreur')
    
    return render_template('login.html', title='login')



@app.route('/registre', methods=["POST", "GET"])
def registre():
    
    if request.method=='POST':
        nom= request.form['nom']
        email= request.form['email']
        password=request.form['password']
        password2= request.form['password2']
        
        if password == password2:
            user= User(nom=nom, email=email, password=password)
            database.session.add(user)
            database.session.commit()
            if 'user_id' in session:
                return redirect(url_for('tableauBord'))
            return redirect(url_for('login'))
        else:
            flash('il faut que le deux soit identique')
    return render_template('registre.html', title='registre')

@app.route('/sedeconnecter')
def logout():
    session.clear()
    
    return redirect(url_for('index'))




@app.route('/tableauBord')
def tableauBord():
    if 'user_id' not in session:
        flash('veuillez se connecter')
        return redirect(url_for('login'))

    else:
        users=User.query.all()
    
        
    return render_template('tableauBord.html', users=users)

if __name__=="__main__":
    with app.app_context():
        database.create_all()
    app.run(debug=True)