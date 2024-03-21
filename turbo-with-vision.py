import base64
import json
import cv2
import requests
import os
import csv
import time
import re
import glob

# OpenAI API Key
api_key = os.environ.get('OPENAI_API_KEY')

# Function to captsure image from camera and encode it
def capture_and_encode_image():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        raise Exception("Failed to open camera")
    
    # print("'s': save the image and proceed, 'q': quit, 'n': retake the image.")
    # while True:
    #     ret, frame = cap.read()
    #     cv2.imshow("Preview", frame)
    #     key = cv2.waitKey(1) & 0xFF

    #     if key == ord('q'):
    #         print("Quitting")
    #         break
    #     elif key == ord('n'):
    #         print("Retaking")
    #         continue
    #     elif key == ord('s'):
    #         print("Saving and Processing")
    #         cap.release()
    #         _, buffer = cv2.imencode('.jpg', frame)
    #         base64_image = base64.b64encode(buffer).decode('utf-8')
    #         cv2.destroyAllWindows()
    #         return base64_image
    print("Taking photo in 10 seconds...")
    # Preview the image during the 10-second delay
    for i in range(10, 0, -1):
        print(f"Previewing image in {i} seconds...")
        ret, frame = cap.read()
        if not ret:
            raise Exception("Failed to capture image")
        cv2.imshow("Preview", frame)
        cv2.waitKey(1000)  # Pause for 1 second
        cv2.destroyAllWindows()

    print("Capturing image...")
    
    ret, frame = cap.read()
    if not ret:
        raise Exception("Failed to capture image")

    _, buffer = cv2.imencode('.jpg', frame)
    base64_image = base64.b64encode(buffer).decode('utf-8')
    cap.release()
    return base64_image

def get_latest_file(folder, pattern):
    """Helper function to get the latest file from a given folder with a specific pattern."""
    list_of_files = glob.glob(os.path.join(folder, pattern))  # * means all if need specific format then *.csv
    if not list_of_files:  # No files found
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def get_total_weight_from_file():
    """Function to automatically get the total weight from the latest txt file."""
    latest_txt_file = get_latest_file('./txts', '*.txt')
    with open(latest_txt_file, 'r') as file:
        total_weight = file.read().strip()
    if not total_weight.isdigit():
        raise ValueError(f"Total weight in file {latest_txt_file} is not a valid number.")
    return total_weight

def capture_and_encode_image_from_file():
    """Function to automatically capture the latest image from the folder and encode it."""
    latest_image_file = get_latest_file('./images', '*.jpg')
    if latest_image_file is None:
        latest_image_file = get_latest_file('./images', '*.jpeg')
    if latest_image_file is None:
        latest_image_file = get_latest_file('./images', '*.png')
    with open(latest_image_file, 'rb') as image_file:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
    return base64_image

# Function to ask for total weight
def get_total_weight():
    while True:
        total_weight = input("Enter the total weight (in grams): ")
        if total_weight.isdigit():
            return total_weight
        else:
            print("Please enter a valid number.")

# Function to save table data to a CSV file
def save_to_csv(meal_data):
    csv_file_path = os.path.join(os.getcwd(), 'meal_data.csv')
    file_exists = os.path.exists(csv_file_path)

    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['Meal', 'Calories', 'Macros', 'Ingredients', 'Weight']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(meal_data)

    print("Data appended to CSV file successfully.")

# Function to parse JSON content and save to table
def save_to_csv(meal_data):
    csv_file_path = os.path.join(os.getcwd(), 'meal_data.csv')
    file_exists = os.path.exists(csv_file_path)

    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['Time', 'Meal', 'Dish', 'Calories', 'Macros', 'Ingredients', 'Weight']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        for meal_name, meal_content in meal_data['Meal'].items():
            for dish_name, dish_info in meal_content.items():
                if isinstance(dish_info, dict):
                    writer.writerow({
                        'Time': meal_data['Time'],
                        'Meal': meal_name,
                        'Dish': dish_name,
                        'Calories': dish_info.get('Calories', ''),
                        'Macros': dish_info.get('Macros (Protein/Carbs/Fats)', ''),
                        'Ingredients': dish_info.get('Ingredients', ''),
                        'Weight': dish_info.get('Weight', '')
                    })
                else:
                    print(f"Skipping dish '{dish_name}' in meal '{meal_name}' due to invalid format.")

    print("Data appended to CSV file successfully.")

# Function to make request to OpenAI API
def make_openai_request(base64_image, total_weight):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "You are a nutritionist and you always give accurate analyses of food items. Analyze the food in the picture. If the food has dessert, berverage, appetizer, main dish, soup, salad, calculate according to your estimates. Calculate the calories, macros, ingredients, and weight for each dish and list them from Dish1 to Dish2, Dish3,....but no more than three dishes. The total weight of the food is " + total_weight + " grams. Response in a pure JSON format: \n"
                    "{\n"
                    "    \"Time\": \"\",\n"
                    "    \"Meal\": {\n"
                    "        \"Dish1\": {\n"
                    "            \"Dishname\": \"\",\n"
                    "            \"Weight\": \"\",\n"
                    "            \"Calories\": \"\",\n"
                    "            \"Macros (Protein/Carbs/Fats)\": \"\",\n"
                    "            \"Ingredients\": \"\"\n"
                    "        }\n"
                    "        // More dishes can be added here, same as the dish1 above: dish2, dish3 ....\n"
                    "    }\n"
                    "}\n"
                "Ensure each dish has a unique index name and value of time is the current time when user posts this request. Standardize the response format as shown above, excluding any additional notes or explanations. If the analysis cannot be provided, refrain from responding."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    print("Making request to OpenAI API")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    print("Getting response from OpenAI API")
    if response.status_code == 200:
        print("Success")
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        print("Response message:")
        print(content)
        print("--------------------")
        return content if content.strip() else None
    else:
        print('Failed to get response from OpenAI API')
        return None

def extract_json_content(json_content_str):
    # Find the first occurrence of "```json"
    start_match = re.search(r'```json', json_content_str)
    
    # Find the last occurrence of "```"
    end_match = re.search(r'```', json_content_str[::-1])
    if end_match:
        end_index = len(json_content_str) - end_match.start()
    else:
        end_index = None
    
    if start_match and end_index:
        # Extract the substring between the first "```json" and the last "```"
        json_content = json_content_str[start_match.end():end_index].strip()
        return json_content
    else:
        return None

def save_to_json(json_content_str):
    # Check if meal_data.json exists   
    json_url = "./nutrition_master/src/meal_data.json"
    if not os.path.exists(json_url):
        with open(json_url, 'w') as json_file:
            json_file.write('[\n')
            json_file.write(json_content_str + '\n')
            json_file.write(']\n')
    else:
        try:
            with open(json_url, 'r+') as json_file:
                content = json_file.read()
                json_file.seek(0)
                json_file.write(content[:-2])  # Remove the last comma and newline
                json_file.write(',\n')
                json_file.write(json_content_str + '\n')
                json_file.write(']\n')
        except Exception as e:
            print(f"Error saving JSON to file: {e}")

    #  # Check if meal_data.txt exists
    # if not os.path.exists('meal_data.txt'):
    #     try:
    #         # Load JSON data from meal_data.json
    #         with open('meal_data.json', 'r') as json_file:
    #             data = json.load(json_file)
            
    #         # Write JSON data to meal_data.txt
    #         with open('meal_data.txt', 'w') as txt_file:
    #             txt_file.write(json.dumps(data, indent=4))
                
    #     except Exception as e:
    #         print(f"Error creating meal_data.txt: {e}")


# Main function
def main():
    total_weight = get_total_weight()
    base64_image = capture_and_encode_image()
    # total_weight = get_total_weight_from_file()
    # base64_image = capture_and_encode_image_from_file()
    json_content = make_openai_request(base64_image, total_weight)
    print("json_content", json_content)
    json_content_str = extract_json_content(json_content)
    print("json_content_str", json_content_str)

    # json_content_str = '''```json
    #     {
    #         "Dish1": {
    #             "Dishname": "Kung Pao Chicken",
    #             "Weight": "100g",
    #             "Calories": "179",
    #             "Macros (Protein/Carbs/Fats)": "14g/11g/9g",
    #             "Ingredients": "Chicken, peanuts, vegetables (bell peppers, zucchini, onions), Szechuan peppers, soy sauce, garlic, ginger, sugar, sesame oil, chili peppers",
    #             "Timestamp": "2023-04-12T14:32:12Z"
    #         }
    #     },
    #     ```
    #     ```json
    #     {
    #         "Dish1": {
    #             "Dishname": "Kung Pao Chicken",
    #             "Weight": "100g",
    #             "Calories": "179",
    #             "Macros (Protein/Carbs/Fats)": "14g/11g/9g",
    #             "Ingredients": "Chicken, peanuts, vegetables (bell peppers, zucchini, onions), Szechuan peppers, soy sauce, garlic, ginger, sugar, sesame oil, chili peppers",
    #             "Timestamp": "2023-04-12T14:32:12Z"
    #         }
    #     }
    #     ```'''
    if json_content_str:
        print("Saving JSON to file")
        save_to_json(json_content_str.replace('```json\n', '').replace('```\n', '').replace('```', ''))


    # if json_content_str:
    #     print("Loading the JSON content string")
    #     json_content = json.loads(json_content_str)
    #     print("Saving JSON to CSV")
    #     save_to_csv(json_content)

if __name__ == "__main__":
    main()
