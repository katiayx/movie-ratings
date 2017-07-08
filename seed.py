"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import datetime
from sqlalchemy import func

from model import User, Rating, Movie, connect_to_db, db
from server import app


def load_users():
    """Load users from users file into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for i, row in enumerate(open("seed_data/users")):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(age=age, zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        if i % 100 == 0:
            print i 

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from movies file into database."""

    print "Movies"

    Movie.query.delete()

    for i, row in enumerate(open("seed_data/movies")):
        row = row.rstrip() 
        movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

        #convert it to an actual datetime object.
        if released_str:
            release_date = datetime.datetime.strptime(released_str, "%d-%b-%Y").date()
        else:
            release_date = None

        # Remove the (YEAR) from the end of the title.
        title = title[:-7]   # " (YEAR)" == 7

        movie = Movie(title=title, release_date=release_date, imdb_url=imdb_url)

        db.session.add(movie)

        if i % 100 == 0:
            print i 

    db.session.commit()


def load_ratings():
    """Load ratings from ratings file into database."""

    print "Ratings"

    Rating.query.delete()

    for i, row in enumerate(open("seed_data/ratings")):
        row = row.rstrip() 

        user_id, movie_id, score, timestamp = row.split("\t")

        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)

        # We don't care about the timestamp, so we'll ignore this

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)

        # provide some sense of progress
        if i % 1000 == 0:
            print i

            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.

            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
