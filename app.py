from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route('/check_subscription/<subscription_code>', methods=['GET'])
def check_subscription(subscription_code):
    url = f"https://api.paystack.co/subscription/{subscription_code}"
    headers = {
        "Authorization": "Bearer sk_live_ca56f5de9a6ec2553c20792cfa92d61f8a2a815c"  # Replace with your own secret key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:  # Check if Paystack API call is successful
        data = response.json()
        if data['status']:  # Check if the request was successful
            subscription_status = data['data']['status']  # Subscription status
            # You can check the status and return a message accordingly
            if subscription_status == 'active':
                return jsonify({"message": "Subscription is active"}), 200
            elif subscription_status == 'complete':
                return jsonify({"message": "Subscription has been completed"}), 200
            elif subscription_status == 'cancelled':
                return jsonify({"message": "Subscription has been cancelled"}), 200
            elif subscription_status == 'expired':
                return jsonify({"message": "Subscription has expired"}), 200
            else:
                return jsonify({"message": "Unknown subscription status"}), 400
        else:
            return jsonify({"message": "Failed to retrieve subscription status"}), 400
    else:
        return jsonify({"message": "Error connecting to Paystack API"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
