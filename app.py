from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os

app = Flask(__name__)
CORS(app)

USER_DETAILS = {
    "full_name": "farhaan_khan",  
    "birth_date": "05032004",  
    "email": "farhaan.khan2022@vitstudent.ac.in", 
    "roll_number": "22BKT0054"  
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
        "all_alphabets": []  
    }
    
    for item in data:
        if item.isdigit() or (item.startswith('-') and item[1:].isdigit()):
            num = int(item)
            result["sum"] += num
            
            if num % 2 == 0:
                result["even_numbers"].append(str(item))
            else:
                result["odd_numbers"].append(str(item))
                
        elif re.match(r'^[a-zA-Z]+$', item):
            result["alphabets"].append(item.upper())
            for char in item:
                result["all_alphabets"].append(char)
                
        else:
            result["special_characters"].append(item)
    
    return result

def create_concat_string(all_alphabets):
    """
    Create concatenated string in reverse order with alternating caps
    """
    if not all_alphabets:
        return ""
    
    reversed_chars = all_alphabets[::-1]
    
    concat_result = ""
    for i, char in enumerate(reversed_chars):
        if i % 2 == 0:  
            concat_result += char.upper()
        else:  
            concat_result += char.lower()
    
    return concat_result

@app.route('/bfhl', methods=['POST'])
def process_bfhl():
    """
    Main POST endpoint that processes the data array
    """
    try:
        request_data = request.get_json()
        
        if not request_data or 'data' not in request_data:
            return jsonify({
                "is_success": False,
                "error": "Invalid input. 'data' field is required."
            }), 400
        
        data = request_data['data']
        
        if not isinstance(data, list):
            return jsonify({
                "is_success": False,
                "error": "'data' must be an array."
            }), 400
        
        processed = process_data(data)
        
        concat_string = create_concat_string(processed["all_alphabets"])
        
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