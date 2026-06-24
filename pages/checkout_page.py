import allure
from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.get_by_placeholder("First Name")
        self.last_name = page.get_by_placeholder("Last Name")
        self.postal_code = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.error_message = page.locator("[data-test='error']")
        self.complete_header = page.locator(".complete-header")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        """填写结算信息"""
        with allure.step(f"填写收货信息: {first_name}, {last_name}, {postal_code}"):
            self.first_name.fill(first_name)
            self.last_name.fill(last_name)
            self.postal_code.fill(postal_code)

    def continue_checkout(self):
        """点击继续"""
        with allure.step("点击继续"):
            self.continue_button.click()

    def finish_order(self):
        """完成订单"""
        with allure.step("点击完成"):
            self.finish_button.click()

    def get_error_message(self) -> str:
        """获取错误信息"""
        return self.error_message.text_content() if self.error_message.is_visible() else ""

    def is_order_complete(self) -> bool:
        """判断订单是否完成"""
        return self.complete_header.is_visible() and "Thank you" in self.complete_header.text_content()