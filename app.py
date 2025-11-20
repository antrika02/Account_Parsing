import ollama
import json
import re

def extract_accounting_data(sentence):
    prompt = f"""
    You are an intelligent accounting model of a company. Extract structured data in JSON format from the following sentence related to accounting tasks. Ensure the output matches the JSON structure:

    {{
      "transaction_type": "sale/purchase/refund",
      "details": {{
        "product_name": "string",
        "quantity": "integer",
        "price_per_unit": "float",
        "total_amount": "float",
        "date": "string",
        "party": {{
          "name": "string",
          "type": "customer/supplier"
        }}
      }}
    }}
    
    Understand all the dialects of sppech convert in english and then extract.
    
    Also add additional information if provided like discounts, bank details of customer or supplier like baank name and further details, payment method and any other necessary information. Omit it or make other values null.
    
    If bought item price < original item price , then original item price - bought item price = discounted_amount and in this case mention original_price. Also calculate discount_percentge = (discount_amount/original_price)*100. In this case original_price = price_per_unit , total_amonut = price_per unit * quantity. add discounted_total_amount.
    
    Based on the given input, you should strictly follow the details provided and should not assume or infer missing information and include all neccesary data.
    As a company if someone buys something from us that is our sales and if someone sell us something that is our purchase. 
    
    Also transaction_type should be considered in different jsonobject only when types given are more than one. Else only one type should be mentioned.
    Sentence: {sentence}
    """
    response = ollama.generate("llama3.1:latest", prompt)

    # Print the raw response to debug
    #print("Raw response:", response)

    # Extract the raw JSON string from the response
    response_text = response.get("response", "").strip()

    # Clean the response (remove the code block formatting)
    json_string = re.sub(r'```json\n|\n```', '', response_text).strip()

    print("Cleaned response:", json_string)  # Debug cleaned response

def main():
    while True:
        sentence = input("Enter an accounting sentence (or type 'exit' to quit): ")
        if sentence.lower() == 'exit':
            print("Exiting the program.")
            break
        result = extract_accounting_data(sentence)

# Start the program
main()


