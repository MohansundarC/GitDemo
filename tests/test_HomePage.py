import pytest

from TestData.HomePageData import HomePageData
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class TestHomePage(BaseClass):

    def test_formSubmission(self, getData):
        log = self.getLogger()
        homepage = HomePage(self.driver)
        log.info("First name is "+getData["firstname"])
        homepage.getName().send_keys(getData["firstname"])
        homepage.getEmail().send_keys(getData["emailID"])
        homepage.getPassword().send_keys(getData["password"])
        homepage.getCheckBox().click()
        self.selectOptionsByText(homepage.getGender(), getData ["gender"])

        homepage.submitForm().click()

        alertText = homepage.getSuccessMessage().text

        assert ("Success" in alertText)
        self.driver.refresh()

    @pytest.fixture(params=HomePageData.getTestData("Testcase2"))
    def getData(self, request):
        return request.param


