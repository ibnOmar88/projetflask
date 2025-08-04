from model import *
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




@app.route('/modifier/<int:id>', methods=['POST', 'GET'])
def modifier(id):
    user= User.query.get_or_404(id)
    
    
    if request.method=='POST':
        nom= request.form['nom']
        email= request.form['email']
        password=request.form['password']
        
        user.nom=nom
        user.email=email
        user.password=password
        
        database.session.commit()
        return redirect(url_for('tableauBord'))
    
    
    return render_template('modifier.html', title='modifier', user=user)



@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    user= User.query.get_or_404(id)
    
    
    if user:
        database.session.delete(user)
        database.session.commit()
        return redirect(url_for('tableauBord'))
    
    
    return render_template('tableauBord.html', title='modifier', user=user)



@app.route('/carte',  methods=["POST", "GET"])
def carte():
     if request.method=='POST':
        Numero= request.form['Numero']
        IdUser= request.form['idUser']
        
        carte= CarteIdentite(NumeroID=Numero,user_id=IdUser)
        database.session.add(carte)
        database.session.commit()
    
     return redirect(url_for('tableauBord'))








# --------------------------------------Article -----------------------------------
@app.route('/Article')
def Article():
    
    # articles= Article.query.all()
    
    
    return render_template('Article.html', title='Article')



@app.route('/addArticle', methods=["POST", "GET"])
def AddArticle():
    
    if request.method=='POST':
        titre= request.form['titre']
        contenu= request.form['contenu']
        id_user=session['user_id']
       
        article= Article(titre=titre, contenu=contenu, user_id=id_user)
        database.session.add(article)
        database.session.commit()
            
    return render_template('addArticle.html', title='registre')

if __name__=="__main__":
    with app.app_context():
        database.create_all()
    app.run(debug=True, port=3000)