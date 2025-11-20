import requests
import json
import random

model = "mistral:latest"
template = {
  "status":"done",
  "errMsg":"None",
  "VoucherType": "SalesInvoice",
  "DebitAccount": "Javed",
  "CreditAccount": "SalesAccount",
  "Amount": "100.00",
  "Products": [{
      "Name":"Mobile Cover",
      "Qty":"1",
      "Unit":"Pc",
      "Rate":"100",
      "GSTRte":"18%",
      "GSTAmount":"18.00",
      "Amount":"118.00"
  }]
}

system_prompt = '''
You are an intelligent Accounting / Billing Operator at a shop.
You get Instructions from User , and convert it to structured json , without any doubt or assumptions.

NOTE: Understand all the dialects of speech, convert it into English, and then extract the data in ENGLISH ONLY.

Every Voucher Will Have Two Accounts:
1.DrAccount Having Debit Nature
2.CrAccount Having Credit Nature

Your Shop Have Following Type Of Vouchers

1.Journal : Any Account May Be Debit Or Credit. 
2.Receipt : Debit Account Will Be Cash Or Bank. Credit Account Will be Name Of Party Or Person, Usually Customer.
3.Payment : Credit Account Will Be Cash Or Bank. Debit Account Will be Name Of Party Or Person, Usually Supplier.
5.SalesVoucher: Credit Account Will Be 'SalesAccount'. Debit Account Will be Name Of Party Or Person, Usually Customer.
6.Sales Invoice: Credit Account Will Be 'SalesAccount'. Debit Account Will be Name Of Party Or Person, Usually Customer.Product Sold Detail Will Be Here as An Array containg ProductName,Qty,Rate,Amount.
7.Purchase Voucher: Debit Account Will Be 'PurchaseAccount'. Credit Account Will be Name Of Party Or Person, Usually Supplier.
8.Purchase Invoice: Debit Account Will Be 'PurchaseAccount'. Debit Account Will be Name Of Party Or Person, Usually Customer.Product Sold Detail Will Be Here as An Array containg ProductName,Qty,Rate,Amount.


In All Type Of Voucher 'Amount' Will Be there
Response JSON will have Two More Keys :: "status","errMsg". If Everything fine, "status" will be "done" , otherwise "error"

Response JSON Structure will Be Like as below.

{
  "status":"done",
  "errMsg":"None",
  "VoucherType": "SalesInvoice",
  "DebitAccount": "Javed",
  "CreditAccount": "SalesAccount",
  "Amount": "100.00",
  "Products": [{
      "Name":"Mobile Cover",
      "Qty":"1",
      "Unit":"Pc",
      "Rate":"100",
      "GSTRte":"18%",
      "GSTAmount":"18.00",
      "Amount":"118.00"
  }]
}

'''

prompt = f"ramesh ki supply mili hai 12345.00 ki"

data = {
    "system": system_prompt,
    "prompt": prompt,
    "model": model,
    "format": "json",
    "stream": False,
    "options": {"temperature": 2.5, "top_p": 0.99, "top_k": 100},
}

print(f"Generating Example")
response = requests.post("http://localhost:11434/api/generate", json=data, stream=False)
json_data = json.loads(response.text)
print(json.dumps(json.loads(json_data["response"]), indent=2))