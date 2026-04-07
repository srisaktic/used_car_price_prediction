<h1 align="center">🚗 BMW Price Prediction App</h1>

<p align="center">
  Predict resale prices of BMW cars using Machine Learning 🚀
</p>

<p align="center">
  <a href="http://3.150.203.235:8502/">
    <img src="https://img.shields.io/badge/Live Demo-Click Here-green?style=for-the-badge" />
  </a>
</p>

---

## 🎯 Project Overview

<p align="center">
A complete end-to-end Machine Learning system that predicts the resale price of BMW cars based on features like model, year, mileage, engine size, and fuel type.
</p>

---

## ⚙️ How It Works

<table align="center">
<tr>
<td>

🔹 **Data Preprocessing**  
Cleaned data and engineered features (age, mileage/year, etc.)

🔹 **Model Training**  
Tested multiple models → selected **XGBoost (R² = 0.96)**

🔹 **Backend (FastAPI)**  
Handles prediction requests

🔹 **Frontend (Streamlit)**  
Interactive UI for user input

🔹 **Containerization**  
Docker + Docker Compose

🔹 **Deployment**  
AWS EC2 with Elastic IP

</td>
</tr>
</table>

---

## 🧰 Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,streamlit,docker,aws,postgres" />
</p>

<p align="center">
<b>ML:</b> Scikit-learn, XGBoost &nbsp; | &nbsp;
<b>Backend:</b> FastAPI &nbsp; | &nbsp;
<b>Frontend:</b> Streamlit &nbsp; | &nbsp;
<b>Cloud:</b> AWS EC2
</p>

---

## 🧱 Architecture

<p align="center">
<b>User → Streamlit UI → FastAPI → XGBoost Model → Prediction</b>
</p>

---

## 📂 Project Structure

```bash
bmw-price-prediction/
│
├── backend/          # FastAPI service
├── frontend/         # Streamlit UI
├── model/            # Trained model
├── data/             # Dataset
├── notebooks/        # Training notebooks
├── docker-compose.yml
└── README.md
