from flask import Flask, jsonify, render_template_string , request
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the fraud data
fraud_data = pd.read_csv('./Data/Fraud_Data.csv')
clean_df = pd.read_csv('./Data/clean_dataset.csv')
transaction_history_data = fraud_data.copy()

# HTML template for the home page with enhanced color styling
# HTML template for the home page with enhanced color styling
home_page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fraud Detection Dashboard API</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            background-color: #f4f5f7;
            color: #333;
        }
        .navbar {
            background-color: #006699;
        }
        .navbar-brand, .nav-link {
            color: #ffffff !important;
        }
        .navbar-brand:hover, .nav-link:hover {
            color: #cce7ff !important;
        }
        .container {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #006699;
        }
        p {
            font-size: 1.1em;
            line-height: 1.6;
        }
        footer {
            margin-top: 20px;
            color: #666;
        }
        .btn {
            background-color: #006699;
            color: #ffffff;
            margin-top: 15px;
        }
        .btn:hover {
            background-color: #004466;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <a class="navbar-brand" href="/">Adey Innovations Inc.</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link" href="http://127.0.0.1:8050/">Summary</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/transaction-history">Transaction History</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="http://127.0.0.1:8050/">Fraud by Country</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="http://127.0.0.1:8050/">Browser Fraud</a>
                </li>
            </ul>
        </div>
    </nav>
    
    <div class="container mt-5">
        <h1 class="text-center">Fraud Detection Dashboard API</h1>
        <p class="mt-4">
            Adey Innovations Inc. is a leading financial technology company focused on enhancing transaction security through effective fraud detection systems. Our advanced technology solutions target fraud prevention in both e-commerce and banking, providing a secure environment for financial transactions.
        </p>
        <p>
            By implementing state-of-the-art machine learning models, geolocation analysis, and transaction pattern recognition, we improve fraud detection accuracy, reduce financial losses, and build trust with customers and financial institutions. Our system allows for efficient real-time monitoring and response, empowering businesses to act swiftly and minimize risks.
        </p>
        <a href="/summary" class="btn">Get Started with Summary</a>
    </div>

    <footer class="text-center mt-5">
        <p>&copy; 2024 Adey Innovations Inc. All rights reserved.</p>
    </footer>
</body>
</html>
"""

view_page_html =  """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fraud Detection Dashboard API</title>
    </head>
    <h1 class="text-center" style="color:#2C3E50;">Fraud Detection Dashboard</h1>
    <p style="color:#34495E;">
        Adey Innovations Inc. is dedicated to enhancing transaction security through advanced fraud detection...
    </p>
    <hr style="border-top: 2px solid #2C3E50;">

    <!-- Form for transaction prediction -->
    <h2 style="color:#2C3E50;">Predict a Transaction</h2>
    <form id="transaction-form">
        <label for="device_id">Device ID:</label>
        <input type="text" id="device_id" name="device_id" required><br>

        <label for="browser">Browser:</label>
        <input type="text" id="browser" name="browser" required><br>

        <label for="amount">Amount:</label>
        <input type="number" id="amount" name="amount" required><br>

        <label for="country">Country:</label>
        <input type="text" id="country" name="country" required><br>

        <label for="purchase_time">Purchase Time (YYYY-MM-DD HH:MM):</label>
        <input type="text" id="purchase_time" name="purchase_time" required><br>

        <button type="submit" style="background-color: #2C3E50; color: white; padding: 8px 16px; border: none;">Predict</button>
    </form>

    <p id="prediction-result" style="color: #2C3E50; font-weight: bold; margin-top: 15px;"></p>
</html>
    <script>
        document.getElementById('transaction-form').onsubmit = async function(e) {
            e.preventDefault();

            // Collect form data
            const data = {
                device_id: document.getElementById('device_id').value,
                browser: document.getElementById('browser').value,
                amount: parseFloat(document.getElementById('amount').value),
                country: document.getElementById('country').value,
                purchase_time: document.getElementById('purchase_time').value
            };

            // Send data to the prediction endpoint
            const response = await fetch('/predict-transaction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            document.getElementById('prediction-result').textContent = result.message;

            // Add transaction to history table if needed
            if (!response.ok) return;

            fetch('/add-to-history', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(result.transaction)
            });
        };
    </script>
    """

@app.route('/')
def home():
    return render_template_string(home_page_html)

# API to serve summary statistics
@app.route('/summary', methods=['GET'])
def get_summary():
    total_transactions = int(len(fraud_data))
    total_fraud_cases = float(fraud_data['class'].sum())
    fraud_percentage = float((total_fraud_cases / total_transactions) * 100)
    
    summary = {
        'total_transactions': total_transactions,
        'total_fraud_cases': total_fraud_cases,
        'fraud_percentage': fraud_percentage
    }

    return jsonify(summary)

# API to serve fraud trends over time
@app.route('/fraud-trends', methods=['GET'])
def fraud_trends():
    fraud_data['purchase_time'] = pd.to_datetime(fraud_data['purchase_time'])
    fraud_cases_over_time = fraud_data[fraud_data['class'] == 1].groupby(fraud_data['purchase_time'].dt.strftime('%Y-%m-%d')).size().to_dict()
    return jsonify(fraud_cases_over_time)


# Function to style rows based on fraud status
def get_row_style(is_fraud):
    return 'background-color: #ffcccc;' if is_fraud else 'background-color: #ccffcc;'

# Placeholder for ML model function
def predict_fraud(transaction):
    # Dummy prediction logic; replace with actual model prediction
    return np.random.choice([0, 1], p=[0.95, 0.05])  # 95% chance of non-fraud

# API to serve transaction history in a styled HTML table with pagination
@app.route('/transaction-history', methods=['GET'])
def transaction_history():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = clean_df[start:end]

    # Build an HTML table with inline styles
    table_html = f"""
    <h2 style="color:#2C3E50;">Transaction History (Page {page})</h2>
    <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#2C3E50; color:white;">
            <th style="padding:8px; border: 1px solid #ddd;">User ID</th>
            <th style="padding:8px; border: 1px solid #ddd;">Amount</th>
            <th style="padding:8px; border: 1px solid #ddd;">Country</th>
            <th style="padding:8px; border: 1px solid #ddd;">Device</th>
            <th style="padding:8px; border: 1px solid #ddd;">Browser</th>
            <th style="padding:8px; border: 1px solid #ddd;">Time</th>
            <th style="padding:8px; border: 1px solid #ddd;">Fraud</th>
        </tr>
    """

    for _, row in paginated_data.iterrows():
        is_fraud = row['class'] == 1
        row_style = get_row_style(is_fraud)
        fraud_text = "Yes" if is_fraud else "No"

        table_html += f"""
        <tr style="{row_style}">
            <td style="padding:8px; border: 1px solid #ddd;">{row['user_id']}</td>
            <td style="padding:8px; border: 1px solid #ddd;">{row['purchase_value']}</td>
            <td style="padding:8px; border: 1px solid #ddd;">{row['country']}</td>
            <td style="padding:8px; border: 1px solid #ddd;">{row['device_id']}</td>
            <td style="padding:8px; border: 1px solid #ddd;">{row['browser']}</td>
            <td style="padding:8px; border: 1px solid #ddd;">{row['purchase_time']}</td>
            <td style="padding:8px; border: 1px solid #ddd; font-weight:bold; color:{"#E74C3C" if is_fraud else "#27AE60"};">{fraud_text}</td>
        </tr>
        """
    
    table_html += "</table>"

    # Add pagination navigation
    table_html += f"""
    <div style="margin-top: 20px;">
        <a href="/transaction-history?page={page - 1}&per_page={per_page}" style="margin-right: 10px; color: #3498DB;" {'hidden' if page <= 1 else ''}>Previous</a>
        <a href="/transaction-history?page={page + 1}&per_page={per_page}" style="color: #3498DB;">Next</a>
    </div>
    """

    return render_template_string(table_html)
# API to create a transaction and predict fraud likelihood
@app.route('/predict-transaction', methods=['POST'])
def view():
    return render_template_string(view_page_html)

def predict_transaction():
    transaction_data = request.json

    # Predict fraud
    is_fraud = predict_fraud(transaction_data)

    return jsonify({
        'transaction': transaction_data,
        'is_fraud': bool(is_fraud),
        'message': "Fraudulent transaction detected" if is_fraud else "Transaction is legitimate"
    })

# Endpoint to add predicted transaction to history
@app.route('/add-to-history', methods=['POST'])
def add_to_history():
    transaction_data = request.json
    transaction_data['class'] = 1 if transaction_data.get('is_fraud') else 0

    global transaction_history_data
    transaction_history_data = transaction_history_data.append(transaction_data, ignore_index=True)

    return jsonify({'status': 'Transaction added to history'}), 200


# API to serve fraud cases by geography
@app.route('/fraud-by-country', methods=['GET'])
def fraud_by_country():
    fraud_country_df = clean_df[clean_df['class'] == 1].groupby('country').size().to_dict()
    return jsonify(fraud_country_df)

# API to serve fraud by devices and browsers
@app.route('/fraud-by-device-browser', methods=['GET'])
def fraud_by_device_browser():
    fraud_by_device = fraud_data[fraud_data['class'] == 1].groupby('device_id').size().to_dict()
    fraud_by_browser = fraud_data[fraud_data['class'] == 1].groupby('browser').size().to_dict()
    return jsonify({'fraud_by_device': fraud_by_device, 'fraud_by_browser': fraud_by_browser})

if __name__ == '__main__':
    app.run(debug=True)
