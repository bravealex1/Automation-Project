# from flask import Flask, request, render_template_string, jsonify
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from threading import Thread
# from urllib.parse import urlparse, parse_qs

# app = Flask(__name__)

# @app.route('/')
# def index():
#     # Serve the HTML content of the main interface
#     return render_template_string(open('interface.html', 'r').read())

# @app.route('/start_clicks', methods=['POST'])
# def start_clicks():
#     data = request.json
#     web_link = data['web_link']
#     search_keyword = data['search_keyword']

#     # Both search_keyword and web_link are required for the operation
#     if not web_link or not search_keyword:
#         return jsonify({'error': "Please provide both the Search Keyword and Targeted Web Page."}), 400

#     # Start the click_website function in a separate thread to handle the operation without blocking
#     thread = Thread(target=click_website, args=(web_link, search_keyword), daemon=True)
#     thread.start()

#     # The response to the AJAX request
#     return jsonify({'message': "Processing started. Please wait for the result."}), 202

# def click_website(web_link, search_keyword):
#     service = Service(executable_path="chromedriver.exe")
#     driver = webdriver.Chrome(service=service)
#     ad_found = None  # This will be a boolean after checking the URL, but starts as None

#     try:
#         # Go to the targeted web page using Selenium WebDriver
#         driver.get(web_link)
#         parsed_url = urlparse(web_link)
#         query_params = parse_qs(parsed_url.query)

#         # Check if the URL contains ad parameters
#         ad_found = 'gad_source' in query_params and 'gclid' in query_params

#         # Additional steps such as clicking could be performed here if ad_found is True

#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         driver.quit()

#     # Log the outcome for debugging - In a real app, consider updating the client-side dynamically or storing the result
#     print(f"Ad found: {ad_found}")

# # Run the Flask app when executed directly
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse, parse_qs
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    # Serve the HTML content directly from a file called 'interface.html'
    # This function returns the HTML interface to the user's browser
    return render_template_string(open('interface.html', 'r').read())

@app.route('/check_ad', methods=['POST'])
def check_ad():
    # Extract data from the JSON sent to this route
    data = request.get_json()
    web_link = data['web_link']
    
    # Initialize the Selenium WebDriver
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    ad_found = False  # Flag to check if an ad was found

    try:
        # Navigate to the specified URL
        driver.get(web_link)
        # Parse the URL to extract query parameters
        parsed_url = urlparse(web_link)
        query_params = parse_qs(parsed_url.query)
        # Check specific query parameters to identify if it's an ad
        ad_found = 'gclid' in query_params
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    # Send a response back to the client with the result of the ad check
    return jsonify({'ad_found': ad_found})

@app.route('/run_autoclick', methods=['POST'])
def run_autoclick():
    # Extract data from the JSON sent to this route
    data = request.get_json()
    web_link = data['web_link']
    number_of_clicks = int(data['number_of_clicks'])
    
    # Start the auto-click process in a new thread so it doesn't block other requests
    thread = Thread(target=autoclick_website, args=(web_link, number_of_clicks), daemon=True)
    thread.start()
    
    # Notify the client that the auto-clicking has started
    return jsonify({'message': "Auto-clicking has started."})

def autoclick_website(web_link, number_of_clicks):
    # Initialize the Selenium WebDriver
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    try:
        for _ in range(number_of_clicks):
            # Navigate to the URL for each click
            driver.get(web_link)
    except Exception as e:
        print(f"An error occurred during auto-click: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)