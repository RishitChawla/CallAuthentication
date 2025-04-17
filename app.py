from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Path to your downloaded service account key file
CREDENTIALS_FILE = 'C:/Users/rishi/Downloads/voice-assistant-456619-723bf8781d9e.json'

# Name of your Google Sheet
SPREADSHEET_NAME = 'SerialNumbers'

# Name of the worksheet (tab) you are using
WORKSHEET_NAME = 'Sheet1'

def is_valid_number(number):
    try:
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
        gc = gspread.authorize(creds)
        spreadsheet = gc.open(SPREADSHEET_NAME)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        column_a = worksheet.col_values(1)  # Get all values from the first column (A)
        return number in column_a
    except Exception as e:
        print(f"Error accessing Google Sheet: {e}")
        return False

@app.route('/', methods=['POST'])
def exotel_webhook():
    caller_input = request.form.get('caller_input')
    if caller_input:
        if is_valid_number(caller_input):
            response = {"status": "valid", "message": "Number found"}
        else:
            response = {"status": "invalid", "message": "Number not found"}
        return jsonify(response)
    else:
        return jsonify({"status": "error", "message": "No input received"}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)