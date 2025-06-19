from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# ---------------------
# ✅ Base URL Configuration
# ---------------------
BASE_URL = "http://localhost:3000"

# ---------------------
# ✅ Setup Chrome Options for Headless Ubuntu
# ---------------------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get(BASE_URL)
driver.maximize_window()

# ---------------------
# ✅ Summary Counters
# ---------------------
passed = 0
failed = 0
results = []

# ---------------------
# ✅ Helper Functions
# ---------------------
def print_result(name, success):
    global passed, failed
    if success:
        print(f"✅ {name}")
        passed += 1
        results.append(f"✅ {name}")
    else:
        print(f"❌ {name}")
        failed += 1
        results.append(f"❌ {name}")

def login(email, password):
    driver.get(f"{BASE_URL}/auth/login")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()

def signup(full_name, email, password):
    driver.get(f"{BASE_URL}/auth/signup")
    driver.find_element(By.ID, "fullName").send_keys(full_name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()

# ---------------------
# ✅ Test Case Functions
# ---------------------
def test_signup():
    try:
        signup("Test User", "testuser@example.com", "password123")
        time.sleep(2)
        print_result("Signup a new user", True)
    except Exception:
        print_result("Signup a new user", False)

def test_logout():
    try:
        driver.get(f"{BASE_URL}/auth/logout")
        time.sleep(1)
        print_result("Logout after signup", True)
    except:
        print_result("Logout after signup", False)

def test_login():
    try:
        login("testuser@example.com", "password123")
        time.sleep(2)
        print_result("Login with valid credentials", True)
    except:
        print_result("Login with valid credentials", False)

def test_new_article_page():
    try:
        driver.get(f"{BASE_URL}/articles/new")
        time.sleep(1)
        assert "New Article" in driver.page_source
        print_result("Navigate to New Article page", True)
    except:
        print_result("Navigate to New Article page", False)

def test_create_article():
    try:
        driver.find_element(By.ID, "title").send_keys("Test Article Title")
        driver.find_element(By.ID, "description").send_keys("This is a test article.")
        driver.find_element(By.ID, "markdown").send_keys("## Markdown content")
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(2)
        assert "Test Article Title" in driver.page_source
        print_result("Create a new article", True)
    except:
        print_result("Create a new article", False)

def test_article_show_page():
    try:
        assert "Test Article Title" in driver.page_source
        print_result("Show created article", True)
    except:
        print_result("Show created article", False)

def test_edit_article():
    try:
        driver.find_element(By.LINK_TEXT, "Edit").click()
        time.sleep(1)
        title = driver.find_element(By.ID, "title")
        title.clear()
        title.send_keys("Updated Article Title")
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(2)
        assert "Updated Article Title" in driver.page_source
        print_result("Edit article", True)
    except:
        print_result("Edit article", False)

def test_delete_article():
    try:
        driver.get(BASE_URL)
        time.sleep(1)
        driver.find_element(By.XPATH, "//form/button[contains(text(), 'Delete')]").click()
        time.sleep(2)
        assert "Updated Article Title" not in driver.page_source
        print_result("Delete article", True)
    except:
        print_result("Delete article", False)

def test_logout_again():
    try:
        driver.get(f"{BASE_URL}/auth/logout")
        time.sleep(1)
        print_result("Logout after editing", True)
    except:
        print_result("Logout after editing", False)

def test_protected_access():
    try:
        driver.get(f"{BASE_URL}/articles")
        time.sleep(1)
        assert "Login" in driver.page_source or "Sign Up" in driver.page_source
        print_result("Protected route access without login", True)
    except:
        print_result("Protected route access without login", False)

# ---------------------
# ✅ Run Test Cases
# ---------------------
print("🚀 Running Selenium Test Cases...\n")

test_signup()
test_logout()
test_login()
test_new_article_page()
test_create_article()
test_article_show_page()
test_edit_article()
test_delete_article()
test_logout_again()
test_protected_access()

# ---------------------
# ✅ Test Summary
# ---------------------
print("\n📋 Test Summary:")
for line in results:
    print(line)

print(f"\n✅ Passed: {passed}")
print(f"❌ Failed: {failed}")

driver.quit()
