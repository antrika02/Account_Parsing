from flask import Flask, request, jsonify, render_template
import ollama
import requests
import json

app = Flask(__name__, template_folder="templates")

def extract_accounting_data(sentence):
    prompt = f"""
    You are an intelligent accounting model of a company. Extract structured data in JSON format from the following sentence related to accounting tasks. Ensure the output matches the JSON structure:

    {{
      "transaction_type": "sale/purchase/refund/payment/receipt",
      "details": {{
        "product_name": "string",
        "quantity": "integer",
        "price_per_unit": "float",
        "total_amount": "float",
        "date": "string",
        "party_name": "string",
        "party_type": "customer/supplier"
        }}
      }}
    }}
    
    NOTE: Understand all the dialects of speech, convert it into English, and then extract the data in ENGLISH ONLY.
  
    If the sentence mentions giving a payment, categorize it as a `payment`. Ensure that if a specific amount is mentioned, it is recorded in the `total_amount`. The `party` field should contain the name of the party receiving the payment (supplier).
    
    If the sentence mentions receiving  a payment, categorize it as a `receipt`. Ensure that if a specific amount is mentioned, it is recorded in the `total_amount`. The `party` field should contain the name of the party making the payment (customer).
    
    Also add additional information if provided like discounts, currency, bank details of customer or supplier like bank name and further details, payment method, and any other necessary information. Omit it or make other values null.
    
    Add currency in price_per_unit or total_amount if provided and default currency would be ₹. 
    Every details other that transaction_type should be in "details".
    
    If the bought item price < original item price, then original item price - bought item price = discounted_amount, and in this case, mention original_price. Also calculate discount_percentage = (discount_amount/original_price)*100. In this case, original_price = price_per_unit, total_amount = price per unit * quantity. Add discounted_total_amount.
    
    Based on the given input, you should strictly follow the details provided and should not assume or infer missing information and include all necessary data.
    As a company, if someone buys something from us, that is our sale, and if someone sells us something, that is our purchase.
    
    NOTE: Don't assume informtion from yourself and provide only json format and nothing else. Only use informtion from the given data provided. 
    
    You need to omit data thata is not necessry according to the sentence. 
    
    NOTE: ONlY JSON without extra words and don't assume.
    
    Sentence: {sentence}
    """
    
    response = ollama.generate("llama3.1:latest", prompt)

    response_text = response.get("response", "").strip()

    print("Raw response:", response_text)

    try:
        response = requests.post("http://eksai.ddns.net:94/ekallied_api/ek_api/updTransAI.ashx", data={"raw_response": response_text})
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        return {"status": "success", "message": "Voucher entry is successful!", "raw_response": response_text}

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e), "raw_response": ""}

@app.route('/acc')
def index():
    return render_template('index.html')  

@app.route('/acc/chat', methods=['POST'])
def handle_accounting():
    try:
        data = request.json
        sentence = data.get('sentence', '')
        if not sentence:
            return jsonify({"status": "error", "message": "No sentence provided"}), 400

        result = extract_accounting_data(sentence)

        return jsonify(result)
    except Exception as e:
        print(f"Error handling request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5527) 
