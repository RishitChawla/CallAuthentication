from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_NUMBERS_FILE = 'valid_numbers.txt'  # Name of your local text file

def is_valid_number(number):
    try:
        with open(VALID_NUMBERS_FILE, 'r') as f:
            valid_numbers = [line.strip().lower() for line in f]
        return str(number).strip().lower() in valid_numbers
    except FileNotFoundError:
        print(f"Error: File '{VALID_NUMBERS_FILE}' not found.")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

@app.route('/', methods=['GET'])
def exotel_webhook():
    caller_input = request.args.get('digits')
    print(f"Received digits: '{caller_input}'")

    if caller_input:
        cleaned_input = caller_input.strip('"')  # Remove double quotes
        is_valid = is_valid_number(cleaned_input)
        print(f"is_valid_number('{cleaned_input}') returned: {is_valid}")
        if is_valid:
            response = {"status": "valid", "message": "Number found"}
            print(f"Returning response: {response}, status: 200")
            return jsonify(response), 200
        else:
            response = {"status": "invalid", "message": "Number not found"}
            print(f"Returning response: {response}, status: 400")
            return jsonify(response), 400
    else:
        response = {"status": "error", "message": "No input received"}
        print(f"Returning response: {response}, status: 400")
        return jsonify(response), 400

@app.route('/test', methods=['GET'])
def test_endpoint():
    print("Test endpoint was hit!")
    return jsonify({"message": "Test endpoint reached"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')