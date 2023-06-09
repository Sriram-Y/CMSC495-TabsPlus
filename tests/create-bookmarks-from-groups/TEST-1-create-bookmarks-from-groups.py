import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from unique import extensionId
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from inputUrls import urls

# Set the path to your ChromeDriver executable
webdriver_service = Service('/usr/local/bin/chromedriver')

extensionPath = "./"
# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--load-extension=' + extensionPath)
chrome_options.add_argument('--disable-extensions-except=./')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--headless=new')  

# Create a new instance of Chrome WebDriver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# navigate to extension 
driver.get('chrome-extension://kjdkhbloaajgmkmcppnfnhjoedkddhpb/index.html')
print("Opening Tabs")

for url in urls: 
    # Open tabs 
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    print(f"Tab: {url} opened")
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
print("Making Tab Groups")
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

driver.execute_script(group_script)
time.sleep(1)

print("Pressing Feature Button")
# Find and click feature button
button = driver.find_element(By.ID, "groupsToBookmarksFolder")
actions = ActionChains(driver)
actions.move_to_element(button).perform()
driver.save_screenshot("./tests/create-bookmarks-from-groups/test1results/TEST1tab_groups_list.png")
time.sleep(1)
print("Making Bookmark Folder(s)")
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
         prompt = Alert(driver)
         prompt.send_keys(color)
         prompt.accept()
   time.sleep(1)
   
print("Bookmark Groups Created Successfully")
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
              urls.push({url: child.url, parentId: child.parentId});
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

for result in testResult:
   print(result)

driver.get("chrome://bookmarks")
driver.save_screenshot("./tests/create-bookmarks-from-groups/test1results/TEST1bookmark_bar_folders_created.png")
# Close the browser
driver.quit()

file = open("./tests/create-bookmarks-from-groups/test1results/test1output", "w")
file.write((str(list(urls))) + "\n")
file.write(str(list(testResult)))
file.close()
