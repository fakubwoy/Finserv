from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os

app = Flask(__name__)
CORS(app)

# User details - Replace with your actual details
USER_DETAILS = {
    "full_name": "john_doe",  # Replace with your actual name in lowercase
    "birth_date": "17091999",  # Replace with your actual birth date (ddmmyyyy)
    "email": "john@xyz.com",  # Replace with your actual email
    "roll_number": "ABCD123"  # Replace with your actual roll number
}

def process_data(data):
    """
    Process the input data array and categorize items
    """
    result = {
        "odd_numbers": [],
        "even_numbers": [],
        "alphabets": [],
        "special_characters": [],
        "sum": 0,
        "all_alphabets": []  # For concat_string processing
    }
    
    for item in data:
        # Check if item is a number
        if item.isdigit() or (item.startswith('-') and item[1:].isdigit()):
            num = int(item)
            result["sum"] += num
            
            if num % 2 == 0:
                result["even_numbers"].append(str(item))
            else:
                result["odd_numbers"].append(str(item))
                
        # Check if item contains only alphabetic characters
        elif re.match(r'^[a-zA-Z]+$', item):
            result["alphabets"].append(item.upper())
            # Store individual characters for concat_string
            for char in item:
                result["all_alphabets"].append(char)
                
        # Everything else is a special character
        else:
            result["special_characters"].append(item)
    
    return result

def create_concat_string(all_alphabets):
    """
    Create concatenated string in reverse order with alternating caps
    """
    if not all_alphabets:
        return ""
    
    # Reverse the order
    reversed_chars = all_alphabets[::-1]
    
    # Apply alternating caps (starting with uppercase)
    concat_result = ""
    for i, char in enumerate(reversed_chars):
        if i % 2 == 0:  # Even index -> uppercase
            concat_result += char.upper()
        else:  # Odd index -> lowercase
            concat_result += char.lower()
    
    return concat_result

@app.route('/bfhl', methods=['POST'])
def process_bfhl():
    """
    Main POST endpoint that processes the data array
    """
    try:
        # Get JSON data from request
        request_data = request.get_json()
        
        # Validate input
        if not request_data or 'data' not in request_data:
            return jsonify({
                "is_success": False,
                "error": "Invalid input. 'data' field is required."
            }), 400
        
        data = request_data['data']
        
        # Validate that data is a list
        if not isinstance(data, list):
            return jsonify({
                "is_success": False,
                "error": "'data' must be an array."
            }), 400
        
        # Process the data
        processed = process_data(data)
        
        # Create concatenated string
        concat_string = create_concat_string(processed["all_alphabets"])
        
        # Build response
        response = {
            "is_success": True,
            "user_id": f"{USER_DETAILS['full_name']}_{USER_DETAILS['birth_date']}",
            "email": USER_DETAILS["email"],
            "roll_number": USER_DETAILS["roll_number"],
            "odd_numbers": processed["odd_numbers"],
            "even_numbers": processed["even_numbers"],
            "alphabets": processed["alphabets"],
            "special_characters": processed["special_characters"],
            "sum": str(processed["sum"]),  # Return sum as string
            "concat_string": concat_string
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/bfhl', methods=['GET'])
def get_bfhl():
    """
    GET endpoint for testing/status
    """
    return jsonify({
        "operation_code": 1,
        "message": "BFHL API is running",
        "user_id": f"{USER_DETAILS['full_name']}_{USER_DETAILS['birth_date']}"
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    Root endpoint
    """
    return jsonify({
        "message": "BFHL REST API",
        "endpoints": {
            "POST /bfhl": "Process data array",
            "GET /bfhl": "API status"
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))