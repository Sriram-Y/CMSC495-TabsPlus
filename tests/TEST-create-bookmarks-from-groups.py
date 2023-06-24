import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from unique import extensionId
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains

# Set the path to your ChromeDriver executable
webdriver_service = Service('/usr/local/bin/chromedriver')

extensionPath = "./"
# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--load-extension=' + extensionPath)
chrome_options.add_argument('--disable-extensions-except=./')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--headless')  

# Create a new instance of Chrome WebDriver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

print("Opening Extension")

# navigate to extension 
driver.get('chrome-extension://kjdkhbloaajgmkmcppnfnhjoedkddhpb/index.html')

print("Opening Tabs")
## Input URLs ##
urls = ["https://github.com/", "https://www.youtube.com/", 
        "https://www.google.com/", "https://www.wikipedia.org/", 
        "https://www.etsy.com/", "https://www.dictionary.com/"]

for url in urls: 
    # Open tabs 
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    print(f"Tab: {url} opened")
print("Switching back to Extension Tab")
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
print("Creating Groups")
group_script = """
      chrome.tabs.query({ url: ["https://github.com/", "https://www.youtube.com/"] }, (tabs) => {
         const tabIds = tabs.map(tab => tab.id);
         chrome.tabs.group({ tabIds: tabIds }, (group) => {
         });
      });
      chrome.tabs.query({ url: ["https://www.google.com/", "https://www.wikipedia.org/"] }, (tabs) => {
         const tabIds = tabs.map(tab => tab.id);
         chrome.tabs.group({ tabIds: tabIds }, (group) => {
         });
      });
      chrome.tabs.query({ url: ["https://www.etsy.com/", "https://www.dictionary.com/"] }, (tabs) => {
         const tabIds = tabs.map(tab => tab.id);
         chrome.tabs.group({ tabIds: tabIds }, (group) => {
         });
      });
"""

x = driver.execute_script(group_script)
time.sleep(1)

# Find and click feature button
button = driver.find_element(By.ID, "groupsToBookmarksFolder")
print("Hovering over feature button")
actions = ActionChains(driver)
actions.move_to_element(button).perform()

time.sleep(1)

print("making tab groups")
# loop through 3 group colors and create bookmark folders 
colors = ["blue", "grey", "red"]
for color in colors:
   # Find all list items on the page
   list_items = driver.find_elements(By.TAG_NAME, "li")

   # Iterate through each list item
   for item in list_items:
      
      # Check if the item's text content contains the word "blue"
      if color in item.text:
         # Perform the desired action on the list item (e.g., click on it)
         item.click()
         break  # Optionally, break the loop if you only want to select the first matching item

   # Switch the driver's focus to the confirmation dialog
   time.sleep(1)
   alert = Alert(driver)

   # Accept the confirmation dialog by clicking "OK"
   alert.accept()
   time.sleep(1)

confirmBookmarks = """ 
   const getBookmarkBarBookmarks = () => {
    return new Promise((resolve) => {
      chrome.bookmarks.getTree(function(bookmarkTreeNodes) {
        const bookmarkBar = bookmarkTreeNodes[0].children[0]; 
        const bookmarkBarBookmarks = bookmarkBar.children;
        const urls = [];
        bookmarkBarBookmarks.forEach(item => {
          if (item.children) {
            item.children.forEach(child => {
              urls.push(child.url);
            });
          }
        });
         resolve(urls);
      });
    });
  }
  return getBookmarkBarBookmarks();
"""

testResult = driver.execute_script(confirmBookmarks)

testResultSet = set(testResult)
urlsSet = set(urls)

print(f"results: {testResultSet}")
print(f"expected urls: {urlsSet}\n")
assert testResultSet == urlsSet, "TESTFAIL"
print("TEST RESULT: PASS - urls match test results")

driver.get("chrome://bookmarks")

# Close the browser
driver.quit()
