from flask import Flask,render_template,flash,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterationForm,LoginForm
import pickle
import numpy


app = Flask(__name__)
app.config['SECRET_KEY'] = '5d8b4f9363f6662ef10f21937ca6907e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
filename = 'IPL_Score_prediction.pkl'
lm = pickle.load(open(filename,'rb'))

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title="Home")


@app.route("/register",methods=['GET','POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('predict'))
    return render_template('Register.html',title = 'Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "nd36675@gmail.com" and form.password.data == "nishant":
            flash(f'Account created successfully','success')
            return redirect(url_for('predict'))
        else:
            flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('login.html',title = 'login',form=form)

@app.route("/predict",methods=['GET','POST'])
def predict():
    return render_template('predict.html')

@app.route("/score",methods=['POST'])
def score():
    temp_array = []

    if request.method == 'POST':

        batting_team = request.form['batting-team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1]

        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1]

        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])

        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]

        data = numpy.array([temp_array])
        my_prediction = int(lm.predict(data)[0])

        return render_template('final_score.html',title='prediction',lower_limit = my_prediction-10, upper_limit = my_prediction+5)

if __name__ == "__main__":
    app.run(debug=True,port=5001)