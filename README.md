🩺 Diabetes Prediction Web App

A Flask-based web application that allows users to upload datasets, train a machine learning model, visualize data, and predict diabetes outcomes using medical parameters.

📌 Overview

This project integrates Machine Learning + Web Development to build an intelligent system for diabetes prediction. It uses a Random Forest Classifier trained on medical data and provides an interactive UI for users to:

Upload datasets
Train ML models
Visualize results
Predict diabetes in real-time
🚀 Features
🔐 User Authentication
Secure Registration & Login
Password hashing using Bcrypt
Session management
📂 Dataset Handling
Upload CSV files
Preview dataset (top rows)
🤖 Model Training
Random Forest Classifier
Train-test split (80/20)
Model saved using Joblib
📊 Data Visualization
Confusion Matrix (accuracy evaluation)
Scatter Plot (Pregnancies vs Glucose)
🔮 Prediction System
Input health parameters
Predict diabetes instantly
🛠️ Tech Stack
Category	Technology
Backend	Flask (Python)
Database	MySQL (SQLAlchemy)
ML Algorithm	Random Forest (Scikit-learn)
Data Handling	Pandas, NumPy
Visualization	Matplotlib, Seaborn
Security	Flask-Bcrypt
Model Storage	Joblib
🧠 Machine Learning Workflow
Upload dataset (CSV)
Split into features (X) and target (y)
Train Random Forest model
Evaluate using:
Accuracy Score
Confusion Matrix
Save model (model.pkl)
Use model for prediction
📥 Input Parameters

The model takes the following inputs:

Pregnancies
Glucose
Blood Pressure
Skin Thickness
Insulin
BMI
Diabetes Pedigree Function
Age
📤 Output
✅ Diabetes Detected
❌ No Diabetes Detected
📊 Visual Outputs
Confusion Matrix Heatmap
Scatter Plot (Pregnancies vs Glucose)
⚙️ Installation & Setup
1️⃣ Clone the Repository
cd diabetes-prediction-app
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Configure Database

Update your MySQL configuration in app.py:

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
4️⃣ Run the Application
python app.py
5️⃣ Open in Browser
http://localhost:5000

💡 Future Enhancements
Add more ML models (SVM, Logistic Regression)
Improve UI/UX design
Deploy on cloud (AWS / Heroku)
Add real-time dashboard analytics
Support multiple datasets
🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

📜 License

This project is open-source and available under the MIT License.

👩‍💻 Author

Sahana R
