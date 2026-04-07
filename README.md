# 🚗 BMW Price Prediction App

An end-to-end machine learning application that predicts the resale price of BMW cars based on vehicle specifications such as model, year, mileage, engine size, fuel type, and transmission.

This project covers the full workflow from data preprocessing and model training to API development, frontend integration, containerization, and cloud deployment.

---

## 🎯 Project Goal

The goal of this project is to build a production-ready ML application that can estimate the resale value of BMW cars using historical vehicle data.

It demonstrates how a machine learning model can be integrated into a complete software system with:

- a trained prediction model
- a backend API for inference
- a frontend UI for user interaction
- Dockerized services for portability
- deployment on AWS EC2

---

## 🌐 Live Demo

**Application URL:** http://3.150.203.235:8502/

---

## ⚙️ How It Works

### 1. Data Preprocessing
The raw dataset was cleaned and transformed to improve model performance. Feature engineering was applied to create additional useful variables such as:

- car age
- mileage per year
- tax per engine size
- other normalized vehicle attributes

### 2. Model Training
Multiple regression models were trained and evaluated, including:

- Linear Regression
- Random Forest Regressor
- XGBoost Regressor

After comparing performance, **XGBoost** was selected as the final model because it achieved the best results with an **R² score of 0.96**.

### 3. Backend API
A **FastAPI** service was built to handle prediction requests.  
The API receives user input, preprocesses the values in the required format, loads the trained model, and returns the predicted price.

### 4. Frontend UI
A simple and interactive **Streamlit** interface allows users to:

- enter BMW car details
- submit the form
- instantly receive the predicted resale price

### 5. Containerization
Both the frontend and backend were containerized using **Docker**, making the application easier to run consistently across environments.

### 6. Deployment
The application was deployed on **AWS EC2** using:

- Docker
- Docker Compose
- Elastic IP

This setup allows the UI and backend to run together as separate services in a cloud environment.

---

## 🧰 Tech Stack

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost

### Backend
- FastAPI

### Frontend
- Streamlit

### DevOps / Deployment
- Docker
- Docker Compose
- AWS EC2

---

## 🧱 System Architecture

```text
User → Streamlit UI → FastAPI Backend → XGBoost Model → Prediction
