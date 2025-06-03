# Real-Time Anomaly Detection of Injection Attacks using Machine Learning Models in Cybersecurity

## 🧠 Overview
This project presents a real-time anomaly detection system for identifying **SQL Injection (SQLi)** and **Cross-Site Scripting (XSS)** attacks using machine learning models. It features a Flask-based API, live dashboard visualization, and system resource monitoring. The project also integrates foundational elements of **Large Language Models (LLMs)** and **chatbots** to assist in real-time responses and contextual analysis.

## 🎯 Objectives
- Detect injection-based attacks (SQLi, XSS) in real time.
- Display anomalies and threat metrics through an interactive dashboard.
- Use LLMs to enhance natural language understanding and chatbot capabilities.
- Enable future expansion for adaptive, explainable AI-driven cybersecurity.

## ⚙️ Features
- 📡 Real-time classification of web queries using Random Forest and Decision Tree models.
- 📊 Dynamic dashboard to track system metrics and detection logs.
- 🚨 Alert system with risk levels and detailed threat logging.
- 🤖 Integrated chatbot powered by LLM prompts for describing threats to users.
- 🔐 Logs user input, threat level, model confidence, and timestamps.

## 🛠️ Tech Stack
- **Languages:** Python, JavaScript
- **ML Frameworks:** Scikit-learn, Pandas, TF-IDF
- **Backend:** Flask, Socket.IO
- **Frontend:** Chart.js, HTML/CSS
- **LLMs & Tools:** Prompt-based querying of GPT for contextual threat explanations

## 🤖 Use of LLMs and Chatbots
- Developed a basic chatbot interface that interprets threat classifications using prompts to an LLM (e.g., OpenAI's GPT) for human-readable explanations.
- Used LLMs to explain the nature of detected injection patterns (e.g., explaining an SQL payload in simple language).
- Enables future integration of **LangChain**, **LangGraph**, or **RAG-based architectures** for deeper conversational capabilities.

## 📂 Project Structure
```
├── flask_api/
│   ├── app.py
│   ├── ensemble_model_sql.pkl
│   ├── ensemble_model_xss.pkl
│   └── alerts.json
├── dashboard/
│   └── templates/
├── logs/
├── chatbot/
│   └── explain_threat.py (uses OpenAI API)
├── requirements.txt
└── README.md
```

## 🚀 Getting Started
```bash
git clone https://github.com/yourusername/real-time-anomaly-detection.git
cd real-time-anomaly-detection
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python flask_api/app.py
```

Then open `http://localhost:5000` in your browser.

## 📈 System Performance
| Metric             | Value     |
|--------------------|-----------|
| SQLi Accuracy       | 98.4%     |
| XSS Accuracy        | 97.6%     |
| Response Time       | ~450 ms   |
| CPU Usage           | ~35%      |
| Memory Usage        | ~60%      |

## 🎥 Demo

[▶️ Watch the video demonstration](./Video%20demonstration.mp4)


## 🧪 Sample Query (via Postman or CURL)
```json
POST http://localhost:5000/predict
{
  "queryText": "SELECT * FROM users WHERE id='1' OR '1'='1';"
}
```

## 🔬 Future Research
- 🧠 Integrate explainable AI (XAI) with LLMs to justify model decisions.
- 🔁 Extend dataset with real-world threat data from honeypots.
- 🗣️ Enhance chatbot with memory and user-adaptive dialogue via LangChain or RAG pipelines.
- 🧪 Real-time streaming data ingestion (Kafka/Flume).
- 🧯 Deploy via Docker/Kubernetes for large-scale inference.

## 📄 Dissertation Report
A complete academic report explaining methodology, evaluation, and architecture is included:
- [📄 Dissertation_Report.pdf](./Pranav_Kumar_Sasikumar_230123766_Dissertation_Report.pdf)

## 👨‍💻 Author
**Pranav Kumar Sasikumar**  
MSc Data Analytics, University of Sheffield  
Email: [pk100815@gmail.com](mailto:pk100815@gmail.com)

## 📚 References
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP XSS](https://owasp.org/www-community/attacks/xss)
- [Scikit-learn](https://scikit-learn.org/)