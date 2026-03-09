from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.google.com")

print("Chrome opened successfully!")

driver.quit()