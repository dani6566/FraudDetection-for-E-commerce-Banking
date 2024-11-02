# FraudDetection-for-E-commerce-Banking

## Overview
**FraudDetection-for-E-commerce-Banking** is a project developed by Adey Innovations Inc., a leader in financial technology solutions. The objective of this project is to build a robust pipeline to detect fraudulent transactions in real-time for e-commerce and banking transactions, using advanced machine learning and data engineering techniques. By leveraging a scalable and efficient data architecture, this project aims to enhance transaction security, reduce financial losses, and bolster trust with customers and financial institutions.

## Project Architecture
The project comprises the following key components:

1. **Data Collection**: 
   - Data is collected from multiple sources, including transaction records from banking APIs, e-commerce platforms, and custom scraping scripts.
   - Data includes various attributes such as device type, geolocation, transaction amount, timestamp, and more.
  
2. **Data Pipeline**:
   - A fully automated ETL (Extract, Transform, Load) pipeline processes raw data into structured formats.
   - **Data Cleaning**: Includes handling missing values, standardizing timestamps, and validating transaction fields.
   - **Transformation**: Aggregates data by time, country, and device/browser to facilitate trend analysis.
   - **Loading**: Cleaned and transformed data is loaded into a data warehouse, ensuring availability for further analysis.

3. **Modeling**:
   - **Machine Learning**: Models are trained to detect fraud patterns using transaction history, user behaviors, and geolocation data.
   - **Deep Learning**: Additional models focus on recognizing complex fraud patterns, especially in high-frequency transaction environments.
   - **Deployment**: Model inference is available via REST API endpoints for real-time fraud detection.

4. **Dashboard**:
   - An interactive dashboard provides an overview of fraud cases, transaction history, and geolocation distribution, enabling easy monitoring and reporting.
   - Features include fraud case maps, trends over time, and transaction analytics by device/browser.

## Getting Started

### Prerequisites
To set up and run this project locally, you need:
- **Python 3.11+**
- **Flask** for API development
- **Dash** and **Plotly** for dashboarding
- **pandas** and **NumPy** for data manipulation
- **scikit-learn** and **TensorFlow/PyTorch** (for model training)

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/dani6566/FraudDetection-for-E-commerce-Banking.git
    cd FraudDetection-for-E-commerce-Banking
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate   # For Windows, use `env\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Load Sample Data**:
   - Place sample transaction data files in the `/data` directory. Ensure CSVs are named as specified in the project.

### Running the API and Dashboard

1. **Run the Flask API**:
    ```bash
    python serve_data.py
    ```
   - The API will be available at `http://localhost:5000`.

2. **Run the Dashboard**:
    ```bash
    python dashboard.py
    ```
   - Access the dashboard at `http://localhost:8050`.

## Usage

### API Endpoints
The API includes the following key endpoints:
- `/summary`: Returns summary statistics for transactions and fraud cases.
- `/fraud-trends`: Provides fraud trends over time.
- `/fraud-by-country`: Lists fraud cases by country.
- `/predict-transaction`: Accepts transaction data in JSON format to predict fraud likelihood.

### Dashboard
The dashboard allows for visualization of:
- **Total Transactions, Total Fraud Cases, and Fraud Percentage**
- **Fraud Trends**: A line chart for fraud cases over time.
- **Fraud by Country**: A world map showcasing fraud distribution.
- **Fraud by Device and Browser**: Bar charts for device/browser fraud cases.

## Contributing
We welcome contributions! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, please reach out to the data engineering team at Adey Innovations Inc.

---

*Built by Adey Innovations Inc., a leader in financial technology, to secure transactions for e-commerce and banking.*
