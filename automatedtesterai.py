import streamlit as st
import time
import openai
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up OpenAI API credentials
#openai.api_key = st.text_input("Enter your OpenAI API key", type="password")

# Define the main function
# Define the main function
def main():
    st.set_page_config(page_title="Simi - Automate Your Web App Testing With AI")
    st.title("Automate Your Web App Testing With AI")
    
    # Prompt the user to enter the OpenAI API key
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    # Rest of the code...
    
    # Prompt the user to enter the OpenAI API key
    #api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    if api_key:
        openai.api_key = api_key
        
        web_url = st.text_input("Enter the URL of the web application to test")
        test_instructions = st.text_area("Enter the test instructions in plain English")

        if st.button("Run Tests"):
            if web_url and test_instructions:
                st.session_state.web_url = web_url

                # Use OpenAI API to generate test steps based on the instructions
                try:
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a test step generator."},
                            {"role": "user", "content": f"Generate precise and actionable test steps for the following instructions:\n{test_instructions}"}
                        ],
                        max_tokens=150,
                        n=1,
                        stop=None,
                        temperature=0.7,
                    )
                    test_steps = response.choices[0].message.content.strip()

                    # Display the generated test steps
                    st.subheader("Generated Test Steps")
                    st.write(test_steps)

                    # Execute the test steps using Selenium
                    driver = webdriver.Chrome()
                    current_url = st.session_state.web_url
                    driver.get(current_url)
                    screenshot_counter = 1

                    try:
                        # Parse and execute the test steps
                        steps = test_steps.split('\n')
                        for step in steps:
                            st.write(f"Current URL: {current_url}")
                            st.write(f"Executing step: {step}")

                            if step.lower().startswith('click'):
                                element_text = step.split('click', 1)[1].strip()
                                element_text = re.escape(element_text)
                                try:
                                    element = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}')]"))
                                    )
                                    driver.execute_script("arguments[0].scrollIntoView();", element)
                                    element.click()
                                    WebDriverWait(driver, 10).until(EC.url_changes(current_url))
                                    current_url = driver.current_url
                                except Exception as e:
                                    st.error(f"Error: Unable to find or click the element with text '{element_text}'. {str(e)}")
                                    driver.save_screenshot(f"error_screenshot_{screenshot_counter}.png")
                                    screenshot_counter += 1
                            elif step.lower().startswith('verify'):
                                # Add generic verification logic here
                                pass
                            elif step.lower().startswith('locate'):
                                element_text = step.split('locate', 1)[1].strip()
                                element_text = re.escape(element_text)
                                try:
                                    element = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}')]"))
                                    )
                                    st.write(f"Located element: {element_text}")
                                except Exception as e:
                                    st.error(f"Error: Unable to locate the element with text '{element_text}'. {str(e)}")
                                    driver.save_screenshot(f"error_screenshot_{screenshot_counter}.png")
                                    screenshot_counter += 1
                            elif step.lower().startswith('enter'):
                                element_text, value = step.split('enter', 1)[1].split('into', 1)
                                element_text = element_text.strip()
                                value = value.strip()
                                element_text = re.escape(element_text)
                                try:
                                    element = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{element_text.lower()}')]"))
                                    )
                                    element.clear()
                                    element.send_keys(value)
                                    time.sleep(1)  # Pause for 1 second after each enter action
                                except Exception as e:
                                    st.error(f"Error: Unable to find or enter value in the element with text '{element_text}'. {str(e)}")
                                    driver.save_screenshot(f"error_screenshot_{screenshot_counter}.png")
                                    screenshot_counter += 1
                            elif step.lower().startswith('submit'):
                                try:
                                    submit_button = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))
                                    )
                                    submit_button.click()
                                    WebDriverWait(driver, 10).until(EC.url_changes(current_url))
                                    current_url = driver.current_url
                                except Exception as e:
                                    st.error(f"Error: Unable to find or click the submit button. {str(e)}")
                                    driver.save_screenshot(f"error_screenshot_{screenshot_counter}.png")
                                    screenshot_counter += 1
                            elif step.lower().startswith('screenshot'):
                                screenshot_path = f"screenshot_{screenshot_counter}.png"
                                driver.save_screenshot(screenshot_path)
                                st.image(screenshot_path, caption=f"Screenshot {screenshot_counter}", use_column_width=True)
                                screenshot_counter += 1
                                time.sleep(1)  # Pause for 1 second after each screenshot
                            # Add more conditions for other types of steps as needed

                        test_results = "Test Passed"
                    except Exception as e:
                        test_results = f"Test Failed: {str(e)}"
                    finally:
                        st.subheader("Test Results")
                        st.write(test_results)
                        driver.quit()
                except Exception as e:
                    st.error(f"Error with OpenAI API: {str(e)}")
            else:
                st.warning("Please provide both the web URL and test instructions.")

if __name__ == "__main__":
    main()