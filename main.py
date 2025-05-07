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
    assert "Dashboard" in dashboard_page.get_header_text()

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