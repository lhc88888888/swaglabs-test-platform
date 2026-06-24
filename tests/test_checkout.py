import allure
from playwright.sync_api import Page
from config.settings import TestConfig
from pages.login_page import LoginPage


@allure.feature("结算模块")
class TestCheckout:

    def _login_and_add_item(self, page: Page, config: TestConfig):
        """登录并添加一个商品到购物车，进入结算页"""
        login_page = LoginPage(page)
        login_page.goto(config.base_url)
        inventory_page = login_page.login(config.standard_user, config.password)
        inventory_page.add_item_to_cart(0)
        cart_page = inventory_page.go_to_cart()
        return cart_page.go_to_checkout()

    @allure.story("完整结算流程")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_checkout(self, page: Page, config: TestConfig):
        checkout_page = self._login_and_add_item(page, config)
        checkout_page.fill_info("Test", "User", "12345")
        checkout_page.continue_checkout()
        checkout_page.finish_order()
        assert checkout_page.is_order_complete(), "订单完成页面未显示"

    @allure.story("结算 - 数据驱动")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_data_driven(self, page: Page, config: TestConfig, checkout_data: dict):
        allure.dynamic.title(f"结算测试: {checkout_data['description']}")
        checkout_page = self._login_and_add_item(page, config)
        checkout_page.fill_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.continue_checkout()

        if "expected_error" in checkout_data:
            # 预期出现错误
            error_msg = checkout_page.get_error_message()
            assert checkout_data["expected_error"] in error_msg, \
                f"错误信息不匹配。预期包含: {checkout_data['expected_error']}, 实际: {error_msg}"
        else:
            # 正常结算
            checkout_page.finish_order()
            assert checkout_page.is_order_complete()