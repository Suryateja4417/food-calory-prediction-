# 🍌 Fruit & Vegetable Nutrition Finder

A beautiful Flask web application that analyzes images of fruits and vegetables to provide detailed nutritional information using the OpenFoodFacts API.

## Features

- **Image Upload**: Drag and drop or click to upload images
- **Nutrition Analysis**: Get detailed nutritional information for fruits and vegetables
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Real-time Processing**: Fast image analysis and nutrition lookup
- **Mobile Friendly**: Responsive design that works on all devices

## Installation

1. **Clone or download the project**
   ```bash
   git clone <your-repo-url>
   cd app2
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Upload an Image**: 
   - Drag and drop an image onto the upload area, or
   - Click the upload area to browse and select a file
   - Supported formats: JPG, PNG, JPEG, GIF

2. **View Results**:
   - The app will analyze the image filename to identify the food item
   - Nutritional information will be displayed in a beautiful card format
   - Information includes calories, fat, protein, vitamins, and more

## File Structure

```
app2/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # CSS styles
│   └── uploads/          # Uploaded images (auto-created)
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## API Endpoints

- `GET /` - Main page
- `POST /upload` - Upload and analyze image
- `GET /nutrition/<label>` - Get nutrition info for a specific food

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **API**: OpenFoodFacts API
- **Image Processing**: PIL (Pillow)
- **Styling**: Custom CSS with modern design principles

## Customization

### Changing the Secret Key
In `app.py`, change the secret key:
```python
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key
```

### Modifying the UI
- Edit `templates/index.html` for HTML structure
- Edit `static/style.css` for styling and colors
- The design uses CSS Grid and Flexbox for responsive layout

### Adding New Features
- Add new routes in `app.py`
- Extend the nutrition analysis in the `get_nutrition_info()` function
- Add new API endpoints for additional functionality

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

2. **File upload errors**:
   - Check file size (max 16MB)
   - Ensure file format is supported (JPG, PNG, JPEG, GIF)

3. **Nutrition data not found**:
   - The app uses filename-based detection
   - Try renaming your image file to include the food name (e.g., `apple_1.jpg`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- OpenFoodFacts API for nutritional data
- Font Awesome for icons
- Flask community for excellent documentation



