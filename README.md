# Turbo with Vision
## Introduction
Turbo with Vision is a Python script that integrates the OpenAI GPT (Generative Pre-trained Transformer) model with computer vision capabilities. It allows you to analyze food items captured from a camera, calculate calories, macros, ingredients, and weight for each dish using the GPT model, and save the analysis data to a CSV or JSON file.

## Prerequisites
Before running the script, ensure you have the following installed:

- Python 3.x
- Git (optional, if you're using version control)

## Installation
1. Clone the repository to your local machine:

```bash
git clone https://github.com/Cynthia-woo/NutritionMaster.git
```

2. Navigate to the project directory:
```bash
cd NutritionMaster
```
3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage
1. Ensure your webcam is connected and functional.

2. Run the script:

```bash
python turbo-with-vision.py
```

3. Follow the on-screen instructions to capture images from the webcam and analyze the food items.

## Run React app
1. Navigate to the folder
```bash
cd nutrition_master/src
```

2. Install requirements
```bash
pip install
```

3. Run the app
```hash
flask run
```




## Configuration
- Open the `turbo-with-vision.py` script and configure the api_key variable with your OpenAI API key.
- Customize the script behavior by modifying the functions or parameters as needed.
  
## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- This project utilizes the OpenAI GPT model for natural language processing and computer vision tasks.
- Special thanks to the contributors and maintainers of the libraries used in this project.