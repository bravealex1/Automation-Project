import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlparse, parse_qs
from threading import Thread

# Function to check for ads on a website using Selenium WebDriver
def check_ad(web_link, keyword):
    # Set path to your WebDriver executable
    service = Service(executable_path="chromedriver.exe")
    # Initialize the Selenium WebDriver with Chrome
    driver = webdriver.Chrome(service=service)
    ad_found = False  # Default ad_found status is False

    try:
        # Navigate to the specified URL
        driver.get(web_link)
        # Check if the keyword is present in the page source, implying an ad might be present
        ad_found = keyword.lower() in driver.page_source.lower()
    except WebDriverException as e:
        st.error(f"WebDriver error occurred: {e}")  # Display error if WebDriver fails
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")  # Display error for any other exceptions
    finally:
        driver.quit()  # Ensure the driver is quit properly

    return ad_found

# Function to perform automated clicks on a website
def autoclick_website(web_link, number_of_clicks):
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    try:
        # Execute the number of clicks specified by navigating to the URL repeatedly
        for _ in range(number_of_clicks):
            driver.get(web_link)
    except WebDriverException as e:
        st.error(f"WebDriver error during auto-click: {e}")  # Handle WebDriver exceptions
    except Exception as e:
        st.error(f"An error occurred during auto-click: {e}")  # Handle general exceptions
    finally:
        driver.quit()  # Ensure the driver is quit properly

# Session state initialization for maintaining state across interactions
if 'ad_detected' not in st.session_state:
    st.session_state['ad_detected'] = False
if 'number_of_clicks' not in st.session_state:
    st.session_state['number_of_clicks'] = 0

# UI setup in Streamlit
st.title('Web Automation Tool')
st.markdown("""
Follow these steps to automate your web interactions:
1. Enter a keyword and the targeted web page URL to check if it contains a sponsored ad.
2. Click 'Check Ad' to verify. If an ad is detected, you will be prompted to enter the number of clicks.
3. Enter the number of times you want to auto-click the ad and click 'Run Auto-click'.
""", unsafe_allow_html=True)

# UI for keyword input
keyword = st.text_input("Search Keyword", placeholder="Enter the keyword here")

# UI for web link input
web_link = st.text_input("Targeted Web Page URL", placeholder="Enter the URL here")

# Button to check for ads
if st.button('Check Ad'):
    with st.spinner('Checking for ads, please wait...'):
        # Execute ad checking function with entered keyword and URL
        st.session_state['ad_detected'] = check_ad(web_link, keyword)
        if st.session_state['ad_detected']:
            st.success('Ad detected. Please enter the number of clicks.')
        else:
            st.info('No ad detected.')

# Input for specifying the number of clicks, shown only if an ad is detected
if st.session_state['ad_detected']:
    st.session_state['number_of_clicks'] = st.number_input('Number of Clicks:', min_value=1, step=1, key='num_clicks')

# Button to start auto-clicking, shown only if an ad is detected and number of clicks is set
if st.session_state['ad_detected'] and st.session_state['number_of_clicks'] > 0:
    if st.button('Run Auto-click'):
        # Start a new thread for auto-clicking to prevent blocking of other operations
        thread = Thread(target=autoclick_website, args=(web_link, st.session_state['number_of_clicks']), daemon=True)
        thread.start()
        st.success("Auto-clicking has started.")

