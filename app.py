from flask import *   #it connects both frontend and backend
from flask_sqlalchemy import SQLAlchemy #connection to database
from flask_bcrypt import Bcrypt #for password encryption

import os
from werkzeug.utils import secure_filename #server
import pandas as pd #load and display dataset

from sklearn.ensemble import RandomForestClassifier #to train the model sklearn package
from sklearn.model_selection import train_test_split
import joblib
import matplotlib
matplotlib.use('Agg')# use non-GUI backend
import matplotlib.pyplot as plt #plotting graph
import seaborn as sns #plotting graph
import numpy as np #numerical calculations
from sklearn.metrics import accuracy_score, confusion_matrix

app=Flask(__name__)
app.secret_key='your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/ml_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db= SQLAlchemy(app)

bcrypt= Bcrypt(app)


class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), unique=True, nullable=False)
    email= db.Column(db.String(100), unique=True, nullable=False)
    password= db.Column(db.String(100), nullable= False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('registration successful! please log in.' ,'success')
            return redirect(url_for('login'))
        except:
            flash('Error: Username or email already exists.','danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password= request.form['password']
        user=User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password,password):
            session['user_id']= user.id
            session['name']=user.name
            flash('login successfull','success')
            return redirect(url_for('dashboard'))
        else:
            flash('invalid email or password.please try agaion.','danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('please log in to access the dashboard.','warning')
        return redirect(url_for('login'))
    name=session['name']
    return render_template('dashboard.html',name=name)

@app.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id',None)
    session.pop('username',None)
    flash('you have been logged out.','info')
    return redirect(url_for('login'))

UPLOAD_FOLDER=os.path.join(os.path.abspath(os.getcwd()),'uploads')
ALLOWED_EXTENSIONS={'csv'}

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS

@app.route('/upload',methods=['GET','POST'])
def upload():
    global uploaded_data
    file_uploaded=False
    columns,data=[],[]
    if request.method=='POST':
        if 'file' not in request.files:
            flash('no file part','danger')
            return redirect(request.url)
        file=request.files['file']
        if file.filename=='':
            flash('no file selected.','warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(file_path)
            file_uploaded=True
            flash('file uploaded successfully!','success')
            try:
                uploaded_data=pd.read_csv(file_path)
                columns=uploaded_data.columns.tolist()
                data=uploaded_data.head(10).values.tolist()
                return render_template('upload.html',file_uploaded=file_uploaded,columns=columns,data=data)
            except Exception as e:
                flash(f'error reading the file:{e}','danger')
                return redirect(request.url)
        flash('invalid file type.please upload a csv file.','danger')
        return redirect(request.url)
    return render_template('upload.html')
# random forest classifier algorith used
@app.route('/train', methods=['GET','POST'])
def train():
    global uploaded_data
    if uploaded_data is None:
        flash('NO dataset uploaded.','warning')
        return redirect(url_for('upload'))
    try:
        X = uploaded_data.iloc[:, :-1]
        y = uploaded_data.iloc[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)
        rf_model = RandomForestClassifier(n_estimators=100,random_state=42)
        rf_model.fit(X_train, y_train)

        if not os.path.exists('models'):
            os.makedirs('models')
        joblib.dump(rf_model, "models/model.pkl")# model creation
        y_pred = rf_model.predict(X_test)
        acc = round(accuracy_score(y_test, y_pred) * 100)
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(y), yticklabels=np.unique(y))
        plt.title(f"Confusion Matrix (Accuracy: {acc}%")
        plt.xlabel("predicted")
        plt.ylabel("Actual")
        cm_path = os.path.join('static', 'images', 'confusion_matrix.png')
        plt.savefig(cm_path)
        plt.close()

        flash(f'Training Successful! Accuracy: {acc}%', 'success')
        return render_template('train.html', accuracy=acc, confusion_matrix=cm_path)

    except Exception as e:
        flash(f"Error during training: {e}", 'danger')
        return redirect(url_for('upload'))

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        inputs={
            "Pregnancies": int(request.form['Pregnancies']),
            "Glucose": float(request.form['Glucose']),
            "BloodPressure": float(request.form['BloodPressure']),
            "SkinThickness":  float(request.form['SkinThickness']),
            "Insulin":  float(request.form['Insulin']),
            "BMI":  float(request.form['BMI']),
            "DiabetesPedigreeFunction":  float(request.form['DiabetesPedigreeFunction']),
            "Age":  float(request.form['Age']),
        }
        input_values=list(inputs.values())
        model=joblib.load("models/model.pkl")
        prediction=model.predict([input_values])[0]
        result="Diabetes Detected" if prediction == 1 else "no diabetes detected"
        return render_template('result.html',inputs=inputs,result=result)
    return render_template('predict.html')

@app.route('/visualize',methods=['GET','POST'])
def visualize():
    global uploaded_data
    if uploaded_data is None:
        flash('no dataset uploaded.','warning')
        return redirect(url_for('upload'))
    scatter_plot=generate_scatter_plot(uploaded_data)
    return render_template('visualize.html',scatter_plot=scatter_plot)

def generate_scatter_plot(data):
    data['Pregnancies']=data['Pregnancies'].apply(lambda x: int(x) if not pd.isnull(x)else 0)
    numerical_columns=data.select_dtypes(include=['float','int']).columns
    if len(numerical_columns) >=2 :
        plt.figure(figsize=(8,6))
        sns.scatterplot(x=data['Pregnancies'],y=data['Glucose'])
        plt.title("Scatter Plot:Pregnancies vs Glucose")
        plt.xlabel("Pregnancies")
        plt.ylabel("Glucose")
        max_pregnancies=data['Pregnancies'].max()
        plt.xticks(ticks=np.arange(0,max_pregnancies+1,1))
        filepath=os.path.join('static','images','scatter_plot.png')
        plt.savefig(filepath)
        plt.close()
        return filepath
    return None
                                                             
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=False, host='0.0.0.0',port=5000)

    

        














