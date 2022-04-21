from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import random

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top_ten-movie-collections.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, unique=False, nullable=True)
    review = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "{'id':%s, 'title':'%s', 'year':%s, 'description':'%s', 'rating':%s, 'ranking':%s, 'review':'%s', " \
               "'img_url':'%s'}" % (self.id, self.title, self.year, self.description, self.rating,
                                    self.ranking, self.review, self.img_url)

class AddNewMovie(FlaskForm):
    title = StringField('Movie Name', validators=[DataRequired()])
    year = StringField('Year of Relese', validators=[DataRequired()])
    description = StringField('Description')
    rating= StringField('Rate the Movie', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    movie_poster = StringField('Movie Poster URL', validators=[DataRequired()])
    submit = SubmitField('Add')

@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()

    db.session.commit()

    return render_template("index.html", movies=all_movies)

@app.route('/id:<num>', methods=['GET', 'POST'])
def update(num):
    all_movies = Movie.query.all()

    num = int(num)
    if request.method == 'POST':
        rating = request.form['rating']
        review = request.form['review']
        movie_id = num
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.rating = round(10-float(rating),2)
        movie_to_update.review = review
        db.session.commit()


        return redirect('http://127.0.0.1:5000')

    return render_template('edit.html', movie=all_movies, num=num)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddNewMovie()
    if form.validate_on_submit():
        new_movie = Movie(title=f"{form.title.data}" , year=f"{form.year.data}" , rating=f"{round(10-float(form.rating.data),2)}",
                           description=f"{form.description.data}", review=f"{form.review.data}",
                          img_url=f"{form.movie_poster.data}", ranking=random.randint(1,20) )
        db.session.add(new_movie)
        db.session.commit()
        return redirect('http://127.0.0.1:5000')

    return render_template('add.html', form=form)

@app.route('/<int:num>')
def Delete(num):
    movie_id = num
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect('http://127.0.0.1:5000')




if __name__ == '__main__':
    app.run(debug=True)



