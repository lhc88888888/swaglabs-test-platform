import allure
from playwright.sync_api import Page
from config.settings import TestConfig
from pages.login_page import LoginPage


@allure.feature("登录模块")
class TestLogin:

    @allure.story("登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, page: Page, config: TestConfig):
        login_page = LoginPage(page)
        login_page.goto(config.base_url)                                    # ✅ 修正
        inventory_page = login_page.login(config.standard_user, config.password)  # ✅ 实例调用
        assert inventory_page is not None, "登录失败，未跳转到商品页"
        assert inventory_page.get_product_count() == 6

    @allure.story("登录失败-密码错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self, page: Page, config: TestConfig):
        login_page = LoginPage(page)
        login_page.goto(config.base_url)                                    # ✅ 修正
        result = login_page.login(config.standard_user, "wrong_password")   # ✅ 实例调用
        assert result is None
        assert "do not match" in login_page.get_error_message()

    @allure.story("登录失败-锁定用户")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_locked_user(self, page: Page, config: TestConfig):
        login_page = LoginPage(page)
        login_page.goto(config.base_url)
        result = login_page.login(config.locked_user, config.password)
        assert result is None
        assert "locked out" in login_page.get_error_message()               # ✅ 用子串匹配

    @allure.story("登录-数据驱动")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_data_driven(self, page: Page, config: TestConfig, login_data: dict):
        allure.dynamic.title(f"登录测试：{login_data['description']}")
        login_page = LoginPage(page)
        login_page.goto(config.base_url)
        result = login_page.login(login_data["username"], login_data["password"])
        expected = login_data["expected_result"]
        if expected == "success":
            assert result is not None, f"预期登录成功，但失败了"
        elif expected == "locked":
            assert result is None
            assert "locked out" in login_page.get_error_message()