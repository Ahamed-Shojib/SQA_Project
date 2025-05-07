from playwright.sync_api import sync_playwright
import pytest

# Page Object Model Classes
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("button[type='submit']")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

class DashboardPage:
    def __init__(self, page):
        self.page = page
        self.dashboard_header = page.locator("h6.oxd-text--h6.oxd-topbar-header-breadcrumb-module")
    def get_dashboard_header_text(self):
        return self.dashboard_header.text_content()
    def is_dashboard_header_visible(self):
        return self.dashboard_header.is_visible()


class AdminPage:
    def __init__(self, page):
        self.page = page
        self.admin_tab = page.locator("a[href='/web/index.php/admin/viewAdminModule']")
        self.search_box = page.locator("input[placeholder='Type for hints...']")
        self.search_button = page.locator("button[type='submit']")

    def go_to_admin(self):
        self.admin_tab.click()

    def search_user(self, username):
        self.search_box.fill(username)
        self.search_button.click()

# Test Fixtures
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/")
    yield page
    context.close()

# Test Cases
def test_01_login_valid_credentials(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    login_page.login("Admin", "admin123")
    assert "Dashboard" in dashboard_page.get_dashboard_header_text()
    print("Login successful: Dashboard page is displayed.")

def test_02_login_invalid_credentials(page):
    login_page = LoginPage(page)
    login_page.login("Invalid", "invalid")
    error = page.locator(".oxd-alert-content-text").text_content()
    assert "Invalid credentials" in error

def test_03_dashboard_header_exists(page):
    LoginPage(page).login("Admin", "admin123")
    dashboard_page = DashboardPage(page)
    page.wait_for_selector("h6.oxd-text--h6.oxd-topbar-header-breadcrumb-module")
    assert dashboard_page.is_dashboard_header_visible(), "Dashboard header is not visible"
    assert dashboard_page.get_dashboard_header_text() == "Dashboard", "Dashboard header text is incorrect"

def test_04_directory_navigates_correctly(page):
    base_url = "https://opensource-demo.orangehrmlive.com/"
    page.goto(base_url)

    LoginPage(page).login("Admin", "admin123")
    page.wait_for_url("**/dashboard/index")
    page.locator('a:has-text("Directory")').click()
    page.wait_for_url("**/web/index.php/directory/viewDirectory", timeout=5000)
    assert "/web/index.php/directory/viewDirectory" in page.url, \
        f"Expected to be on directory view, but current URL is {page.url}"
    
def test_05_my_info_navigates_correctly(page):
    base_url = "https://opensource-demo.orangehrmlive.com/"
    page.goto(base_url)

    LoginPage(page).login("Admin", "admin123")
    page.wait_for_url("**/dashboard/index")
    page.locator('a:has-text("My Info")').click()
    page.wait_for_url("**/web/index.php/pim/viewPersonalDetails/**", timeout=5000)
    assert "/web/index.php/pim/viewPersonalDetails/" in page.url, \
        f"Expected to be on My Info page, but current URL is {page.url}"

def test_06_navigate_to_job_details(page):
    base_url = "https://opensource-demo.orangehrmlive.com/"
    page.goto(base_url)
    LoginPage(page).login("Admin", "admin123")
    page.wait_for_url("**/dashboard/index")
    page.locator('a:has-text("My Info")').click()
    page.wait_for_url("**/web/index.php/pim/viewPersonalDetails/**", timeout=5000)
    page.locator('a:has-text("Job")').click()
    page.wait_for_url("**/web/index.php/pim/viewJobDetails/**", timeout=5000)
    assert "/web/index.php/pim/viewJobDetails/" in page.url, \
        f"Expected to be on Job Details page, but current URL is {page.url}"

def test_07_navigate_to_contact_details(page):
    base_url = "https://opensource-demo.orangehrmlive.com/"
    page.goto(base_url)

    LoginPage(page).login("Admin", "admin123")
    page.wait_for_url("**/dashboard/index")
    page.locator('a:has-text("My Info")').click()
    page.wait_for_url("**/viewPersonalDetails/**", timeout=5000)
    page.locator('a:has-text("Contact Details")').click()
    page.wait_for_url("**/contactDetails/**", timeout=5000)
    assert "/web/index.php/pim/contactDetails/" in page.url, \
        f"Expected to be on Contact Details page, but got {page.url}"

def test_05_search_admin_user(page):
    LoginPage(page).login("Admin", "admin123")
    admin_page = AdminPage(page)
    admin_page.go_to_admin()
    admin_page.search_user("Admin")
    assert page.locator(".oxd-table-cell").first.is_visible()


def test_05_buzz_navigates_correctly(page):
    base_url = "https://opensource-demo.orangehrmlive.com/"
    page.goto(base_url)
    LoginPage(page).login("Admin", "admin123")
    page.wait_for_url("**/dashboard/index")
    page.locator('a:has-text("Buzz")').click()
    page.wait_for_url("**/web/index.php/buzz/viewBuzz", timeout=5000)
    assert "/web/index.php/buzz/viewBuzz" in page.url, \
        f"Expected to be on Buzz page, but current URL is {page.url}"

def test_06_buzz_navigates_Post_Button(page):
    base_url = "https://opensource-demo.orangehrmlive.com/"
    page.goto(base_url)
    LoginPage(page).login("Admin", "admin123")
    page.wait_for_url("**/dashboard/index")
    page.locator('a:has-text("Buzz")').click()
    page.wait_for_url("**/web/index.php/buzz/viewBuzz", timeout=5000)
    assert "/web/index.php/buzz/viewBuzz" in page.url, \
        f"Expected to be on Buzz page, but current URL is {page.url}"
    page.locator("button.oxd-button.oxd-button--medium.oxd-button--main").click()


def test_07_buzz_navigates_Share_Button(page):
    base_url = "https://opensource-demo.orangehrmlive.com/"
    page.goto(base_url)
    LoginPage(page).login("Admin", "admin123")
    page.wait_for_url("**/dashboard/index")
    page.locator('a:has-text("Buzz")').click()
    page.wait_for_url("**/web/index.php/buzz/viewBuzz", timeout=5000)
    assert "/web/index.php/buzz/viewBuzz" in page.url, \
        f"Expected to be on Buzz page, but current URL is {page.url}"
    page.locator("button.oxd-icon-button").first.click()



def test_07_navigate_to_my_info(page):
    LoginPage(page).login("Admin", "admin123")
    page.locator("a[href='/web/index.php/pim/viewMyDetails']").click()
    assert "Personal Details" in page.content()

def test_08_logout_button_works(page):
    LoginPage(page).login("Admin", "admin123")
    page.locator(".oxd-userdropdown-name").click()
    page.locator("a[href='/web/index.php/auth/logout']").click()
    assert page.url.endswith("/auth/login")

def test_09_remember_me_option_not_present(page):
    assert not page.is_visible("input[name='rememberMe']")


def test_11_cannot_login_with_blank_credentials(page):
    LoginPage(page).login("", "")
    error = page.locator("#app").text_content()
    assert "Required" in error

#====================================================


