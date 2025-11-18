🧾 Accounting Data Extractor (AI-Powered)

This project is a command-line AI tool that extracts structured accounting information from natural-language sentences.
It uses an Ollama LLM to convert messy, human-written accounting text into clean JSON data for further processing.

⸻

🚀 Features
	•	Convert human accounting sentences into structured JSON
	•	Automatically extracts:
	•	Transaction type (sale / purchase / refund)
	•	Product name
	•	Quantity
	•	Price per unit
	•	Total amount
	•	Date
	•	Cleans the LLM output, fixes formatting issues, and returns proper JSON
	•	Runs directly in the terminal
	•	Uses Ollama (local LLM) — no cloud required

⸻

📦 Requirements

Make sure you have the following installed:
	•	Python 3.8+
	•	Ollama installed on your system
👉 https://ollama.com/download
	•	Any Ollama model (e.g., llama3, mistral, etc.)
🛠️ How It Works

The script:
	1.	Sends the user’s sentence to the Ollama model with a structured prompt.
	2.	Receives a JSON-like output.
	3.	Cleans it using:
	•	Regex
	•	JSON fixing
	4.	Prints valid, formatted JSON to the terminal.



⸻

🧙‍♂️ Behind the Scenes

The script includes:
	•	A detailed prompt for accurate extraction
	•	Cleaning pipelines to fix malformed LLM JSON
	•	Regex operations to remove unwanted characters
	•	Debug prints to help developers inspect raw vs cleaned output

⸻

🤝 Contributing

Pull requests are welcome!
If you want to enhance parsing accuracy, integrate external accounting APIs, or add UI support, feel free to contribute.
