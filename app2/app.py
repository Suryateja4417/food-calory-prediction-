from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
import json
import os
from werkzeug.utils import secure_filename
from PIL import Image
import base64
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fallback nutrition database for common fruits and vegetables
FALLBACK_NUTRITION = {
    "apple": {"name": "Apple", "calories": 52, "fat": 0.2, "saturated_fat": 0.1, "protein": 0.3, "sodium": 1, "potassium": 107, "cholesterol": 0, "carbohydrates": 14, "fiber": 2.4, "sugar": 10},
    "banana": {"name": "Banana", "calories": 89, "fat": 0.3, "saturated_fat": 0.1, "protein": 1.1, "sodium": 1, "potassium": 358, "cholesterol": 0, "carbohydrates": 23, "fiber": 2.6, "sugar": 12},
    "orange": {"name": "Orange", "calories": 47, "fat": 0.1, "saturated_fat": 0.0, "protein": 0.9, "sodium": 0, "potassium": 181, "cholesterol": 0, "carbohydrates": 12, "fiber": 2.4, "sugar": 9},
    "carrot": {"name": "Carrot", "calories": 41, "fat": 0.2, "saturated_fat": 0.0, "protein": 0.9, "sodium": 69, "potassium": 320, "cholesterol": 0, "carbohydrates": 10, "fiber": 2.8, "sugar": 4.7},
    "tomato": {"name": "Tomato", "calories": 18, "fat": 0.2, "saturated_fat": 0.0, "protein": 0.9, "sodium": 5, "potassium": 237, "cholesterol": 0, "carbohydrates": 3.9, "fiber": 1.2, "sugar": 2.6},
    "broccoli": {"name": "Broccoli", "calories": 34, "fat": 0.4, "saturated_fat": 0.1, "protein": 2.8, "sodium": 33, "potassium": 316, "cholesterol": 0, "carbohydrates": 7, "fiber": 2.6, "sugar": 1.5},
    "strawberry": {"name": "Strawberry", "calories": 32, "fat": 0.3, "saturated_fat": 0.0, "protein": 0.7, "sodium": 1, "potassium": 153, "cholesterol": 0, "carbohydrates": 8, "fiber": 2.0, "sugar": 4.9},
    "grape": {"name": "Grape", "calories": 62, "fat": 0.2, "saturated_fat": 0.1, "protein": 0.6, "sodium": 2, "potassium": 191, "cholesterol": 0, "carbohydrates": 16, "fiber": 0.9, "sugar": 16},
    "lemon": {"name": "Lemon", "calories": 29, "fat": 0.3, "saturated_fat": 0.0, "protein": 1.1, "sodium": 2, "potassium": 138, "cholesterol": 0, "carbohydrates": 9, "fiber": 2.8, "sugar": 2.5},
    "corn": {"name": "Corn", "calories": 86, "fat": 1.2, "saturated_fat": 0.2, "protein": 3.2, "sodium": 15, "potassium": 270, "cholesterol": 0, "carbohydrates": 19, "fiber": 2.7, "sugar": 3.2}
}

def get_nutrition_info(label):
    """Get nutrition information from OpenFoodFacts API with fallback"""
    try:
        print(f"Searching for nutrition info for: {label}")
        
        # First try the fallback database
        label_lower = label.lower().strip()
        if label_lower in FALLBACK_NUTRITION:
            print(f"Found in fallback database: {label_lower}")
            return FALLBACK_NUTRITION[label_lower]
        
        # Try API
        response = requests.get(
            "https://world.openfoodfacts.org/cgi/search.pl",
            params={
                "search_terms": label,
                "search_simple": 1,
                "action": "process",
                "json": 1
            }
        )
        
        print(f"API Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API Response data: {data}")
            
            if data.get("products") and len(data["products"]) > 0:
                product = data["products"][0]
                nutriments = product.get("nutriments", {})
                
                print(f"Found product: {product.get('product_name', label)}")
                print(f"Nutriments: {nutriments}")
                
                return {
                    "name": product.get("product_name", label),
                    "calories": nutriments.get("energy-kcal_100g", "N/A"),
                    "fat": nutriments.get("fat_100g", "N/A"),
                    "saturated_fat": nutriments.get("saturated-fat_100g", "N/A"),
                    "protein": nutriments.get("proteins_100g", "N/A"),
                    "sodium": nutriments.get("sodium_100g", "N/A"),
                    "potassium": nutriments.get("potassium_100g", "N/A"),
                    "cholesterol": nutriments.get("cholesterol_100g", "N/A"),
                    "carbohydrates": nutriments.get("carbohydrates_100g", "N/A"),
                    "fiber": nutriments.get("fiber_100g", "N/A"),
                    "sugar": nutriments.get("sugars_100g", "N/A"),
                }
            else:
                print("No products found in API response")
        else:
            print(f"API request failed with status: {response.status_code}")
            
        return None
    except Exception as e:
        print(f"Error fetching nutrition info: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print("Upload request received")
        
        if 'file' not in request.files:
            print("No file in request")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            print("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"File received: {file.filename}")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract label from filename
            label = os.path.splitext(filename)[0].split('_')[0].split('.')[0]
            print(f"Extracted label: {label}")
            
            # Get nutrition information
            nutrition_info = get_nutrition_info(label)
            print(f"Nutrition info result: {nutrition_info}")
            
            # Convert image to base64 for display
            with open(filepath, 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            response_data = {
                'success': True,
                'image': img_base64,
                'label': label,
                'nutrition': nutrition_info
            }
            
            print(f"Sending response: {response_data}")
            return jsonify(response_data)
        else:
            print("Invalid file type")
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        print(f"Error in upload_file: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/nutrition/<label>')
def get_nutrition(label):
    nutrition_info = get_nutrition_info(label)
    if nutrition_info:
        return jsonify(nutrition_info)
    return jsonify({'error': 'Nutrition information not found'}), 404

@app.route('/test')
def test_nutrition():
    """Test route to verify nutrition function works"""
    test_label = "apple"
    nutrition_info = get_nutrition_info(test_label)
    return jsonify({
        'test_label': test_label,
        'nutrition_info': nutrition_info,
        'fallback_keys': list(FALLBACK_NUTRITION.keys())
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
