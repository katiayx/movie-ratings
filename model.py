from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    """User for website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64))
    last_name = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)


    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        """Provide basic info on user."""

        return "<User user_id=%s email=%s password=%s age=%s zipcode=%s>" % (self.user_id,
                                                                            self.email)

class Rating(db.Model):
    """Store rating score"""

    __tablename__ = "ratings"


    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    movie = db.relationship("Movie", backref=db.backref("ratings"), order_by=rating_id)
    user = db.relationship("User", backref=db.backref("ratings"), order_by=rating_id)
    

    def __repr__(self):
        """Provides user rating on a movie"""

        return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (self.rating_id,
                                                                          self.score)



class Movie(db.Model):
    """Store movie information"""

    __tablename__="movies"

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    release_date = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(300))

    def __repr__(self):
        """Provides movie info"""

        return "<Movie info movie_id=%s movie_title=%s release_at=%s imdb_url=%s>" % (self.movie_id,
                                                                                        self.title,
                                                                                        self.release_date,
                                                                                        self.imdb_url) 

def connect_to_db(app):
    """connect to database"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
