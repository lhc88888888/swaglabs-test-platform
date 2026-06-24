import allure
from playwright.sync_api import Page
from pages.inventory_page import InventoryPage

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator("[data-test='error']")

    def goto(self, base_url: str):
        """打开登录页"""
        with allure.step("打开登录页"):
            self.page.goto(base_url)

    def login(self, username: str, password: str) -> InventoryPage | None:
        """登录操作，成功返回 InventoryPage，失败返回 None"""
        with allure.step(f"输入用户名: {username}"):
            self.username_input.fill(username)
        with allure.step(f"输入密码: {password}"):
            self.password_input.fill(password)
        with allure.step("点击登录按钮"):
            self.login_button.click()

        # 判断是否登录成功
        if self.page.url.endswith("/inventory.html"):
            allure.attach("登录成功", "结果", allure.attachment_type.TEXT)
            return InventoryPage(self.page)
        else:
            error_text = self.error_message.text_content() if self.error_message.is_visible() else "未知错误"
            allure.attach(error_text, "登录失败", allure.attachment_type.TEXT)
            return None

    def get_error_message(self) -> str:
        """获取错误提示文字"""
        return self.error_message.text_content() if self.error_message.is_visible() else ""