# ⚡ Stochastic Workflow Optimization Engine

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![SimPy](https://img.shields.io/badge/Simulation-SimPy-green)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)

## 📌 Executive Summary
This project implements a **Digital Twin** of a high-volume service center (e.g., Automated Car Wash, EV Charging Network) using **Discrete Event Simulation (DES)**. 

It provides an interactive dashboard to analyze stochastic bottlenecks, optimize resource allocation, and calculate ROI based on Service Level Agreements (SLA).

## 🚀 Key Features
* **Stochastic Modeling:** Simulates random Poisson arrivals and Exponential service times.
* **Comparative Analysis:** Runs "Baseline" vs. "Optimized" models side-by-side.
* **Churn Prediction:** Calculates customer loss probability (Balking) based on queue capacity ($M/M/1/K$).
* **High-Volume Architecture:** Capable of simulating **50,000+ minutes** of operations with optimized data visualization.

## 📊 Results (Case Study)
| Metric | Baseline (1 Server) | Optimized (2 Servers) | Improvement |
| :--- | :--- | :--- | :--- |
| **Avg Wait Time** | 20.00 min | 0.88 min | **95% Reduction** |
| **Churn Rate** | 1.71% | < 0.1% | **Revenue Protected** |
| **Queue Health** | Heavy Tail | Zero-Inflated | **Stable** |

## 🛠️ Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/stochastic-workflow-optimizer.git](https://github.com/YOUR_USERNAME/stochastic-workflow-optimizer.git)
    cd stochastic-workflow-optimizer
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Dashboard**
    ```bash
    streamlit run app.py
    ```

## 🧠 Tech Stack
* **Simulation Logic:** `SimPy` (Process-based DES)
* **Frontend:** `Streamlit` (Interactive Web App)
* **Visualization:** `Plotly` (Interactive Charts), `Pandas`