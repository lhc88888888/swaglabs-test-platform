import allure
from playwright.sync_api import Page

def attach_screenshot(page: Page, name: str = "screenshot"):
    """失败时自动截图并附加到 Allure 报告"""
    screenshot = page.screenshot()
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)

def attach_text(content: str, name: str = "info"):
    """附加文本信息到报告"""
    allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)