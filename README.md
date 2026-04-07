🚗 BMW Price Prediction App

🎯 Goal

Predict the resale price of BMW cars based on specs like model, year, mileage, engine size, fuel type, etc.
It’s a complete end-to-end ML project — from training a model to deploying it live on AWS EC2.

👉 Live Demo: http://3.150.203.235:8502/￼

⸻

⚙️ How It Works
	1.	Data Preprocessing – Cleaned and engineered features (age, mileage/year, tax per engine, etc.)
	2.	Model Training – Tested Linear Regression, Random Forest, and XGBoost → chose XGBoost (R² = 0.96)
	3.	Backend (FastAPI) – Handles prediction requests from the UI
	4.	Frontend (Streamlit) – Simple interface where users enter car details and get instant price predictions
	5.	Containerization (Docker) – Both API and UI are containerized for easy deployment
	6.	Deployment (AWS EC2) – Hosted on a free-tier EC2 instance using Docker Compose and Elastic IP

⸻

🧰 Tech Stack
	•	Python, Pandas, NumPy, Scikit-learn, XGBoost – ML pipeline
	•	FastAPI – Backend API
	•	Streamlit – Frontend UI
	•	Docker + Docker Compose – To run API and UI together
	•	AWS EC2 – For cloud deployment

⸻

🧱 Architecture

User → Streamlit UI → FastAPI Backend → XGBoost Model → Prediction


⸻

💻 Run Locally

git clone https://github.com/yourusername/bmw-price-predictor.git
cd bmw-price-predictor
docker compose up --build

Then open http://localhost:8502/ in your browser.

⸻

🚀 Key Learnings
	•	Built and connected ML models with APIs and UI
	•	Managed microservices using Docker Compose
	•	Deployed a full ML app to AWS EC2
	•	Gained hands-on MLOps and cloud deployment experience

⸻

👨‍💻 Author

Sri Sakticharan Nirmal Kumar
Master’s in Data Science – NYIT
📧 srisakticharan4@gmail.com
