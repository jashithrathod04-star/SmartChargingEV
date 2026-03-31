# ⚡ SmartCharging Analytics: Uncovering EV Behavior Patterns  

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://idai105-1000436-nishthapriyeshshah-sa.streamlit.app/)  
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)  
[![Data Mining](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)]()  

An advanced **Business Intelligence & Data Mining Dashboard** built using **Streamlit**, applying machine learning and statistical analysis to uncover hidden patterns in EV charging station usage.

---

# 🎓 Academic Details
- **Developer:** Jashith Hemendra Rathod   
- **WACP No:** 1000422  
- **CRS Subject:** Artificial Intelligence  
- **Course:** Data Mining (IBCP)  
- **Institution:** Aspen Nutan Academy  

---

# 📌 Project Title & Scope

## Project Title
**SmartCharging Analytics: Uncovering EV Behavior Patterns**

## Scope
This project analyzes global EV charging station data to:
- Understand user behavior patterns  
- Identify high-demand infrastructure  
- Detect anomalies and inefficiencies  
- Support data-driven urban planning decisions  

---

# 🎯 Project Objectives (Rubric Alignment)

| Objective | Implementation |
|----------|--------------|
| Data Understanding | Dataset exploration + feature explanation |
| Data Preprocessing | Cleaning, encoding, normalization |
| Data Visualization | Histograms, heatmaps, boxplots, maps |
| Machine Learning | Clustering, association rules |
| Insights & Reporting | Actionable business conclusions |
| Deployment | Live Streamlit dashboard |

---

# 🚀 Live Dashboard
👉 https://idai105-1000436-nishthapriyeshshah-sa.streamlit.app/

---

# 🧹 Stage 1–2: Data Preprocessing & Preparation

### Steps Performed:
1. Duplicate Removal using `Station ID`  
2. Handling Missing Values  
   - Median → Ratings  
   - Mode → Renewable Energy  
   - Default → Connector Types  
3. Categorical Encoding  
4. Feature Engineering (Availability → Hours)  
5. Normalization using `StandardScaler`  

---

# 📊 Stage 3: Exploratory Data Analysis

### Visualizations Implemented:
- Histograms → Usage distribution  
- Line Charts → Demand growth over years  
- Boxplots → Cost variation across operators  
- Heatmaps → Charger type vs availability  
- Scatter Plots → Correlation analysis  

---

# 🧠 Stage 4: Clustering

### Algorithm:
- K-Means Clustering  
- PCA (Dimensionality Reduction)

### Method:
- Elbow Method for optimal clusters  

### Output:
- High Demand Premium Stations  
- Standard Commuter Stations  
- Underutilized Rural Stations  

### Visualization:
- Interactive Map using Latitude & Longitude  

---

# 🔗 Stage 5: Association Rule Mining

### Algorithm:
- Apriori Algorithm  

### Metrics:
- Support  
- Confidence  
- Lift  

### Example Insight:
- DC Fast + Renewable Energy → High Usage  

---

# ⚠️ Stage 6: Anomaly Detection

### Techniques:
- IQR  
- Z-Score  
- Local Outlier Factor  

### Findings:
- High-cost low-usage stations  
- Low-rating high-maintenance stations  
- Abnormal usage spikes  

---

# 📈 Stage 7: Insights & Reporting

### Key Insights:
1. Fast chargers increase usage significantly  
2. Higher ratings lead to higher demand  
3. Urban stations dominate usage  
4. Stable pricing improves trust  
5. Anomalies indicate maintenance issues  

---

# 🖥️ Dashboard Features

- Interactive filters  
- Real-time charts  
- Map visualization  
- Machine learning integration  
- Clean UI/UX  

---

# 🧾 Rubric Mapping

| Rubric Criteria | Status |
|----------------|--------|
| Data Understanding | ✔ |
| Data Cleaning | ✔ |
| Visualization | ✔ |
| Machine Learning | ✔ |
| Insights | ✔ |
| Deployment | ✔ |

---

# 🏆 Guideline Compliance Checklist

- ✔ Histogram  
- ✔ Line Chart  
- ✔ Heatmap  
- ✔ Boxplot  
- ✔ Scatter Plot  
- ✔ Clustering  
- ✔ Association Rules  
- ✔ Anomaly Detection  
- ✔ Map Visualization  

---
# 📂 Repository Structure
IDAI105-1000422-Jashith-Hemendra-Rathod/
│
├── app.py
├── dataset.csv
├── requirements.txt
├── SCREENSHOTS/
└── README.md



---

# 🛠️ Installation

bash
git clone <repo-link>
cd project-folder
pip install -r requirements.txt
streamlit run app.py



# 📚 References
-Scikit-Learn
-Mlxtend
-Plotly
-Folium
-Streamlit


