import pytest
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        service_obj = Service("C:/Users/Mohan Sundar/Downloads/chromedriver_win32 (1).exe")
        driver = webdriver.Chrome(service=service_obj)

    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path="C:/Users/Mohan Sundar/Downloads/geckodriver-v0.32.2-win32")

    elif browser_name == "ie":
        print("IE")

    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.maximize_window()
    driver.implicitly_wait(5)
    request.cls.driver = driver
    # Now the driver is assigned to class level driver request parameter(request.cls.driver)
    yield
    driver.close()

#@pytest.mark.hookwrapper
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
        driver.get_screenshot_as_file(name)



