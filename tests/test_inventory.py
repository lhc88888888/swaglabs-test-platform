import allure
from playwright.sync_api import Page

from config.settings import TestConfig
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("商品模块")
class TestInventory:
    def _login(self, page: Page, config: TestConfig):
        login_page = LoginPage(page)
        login_page.goto(config.base_url)
        return login_page.login(config.standard_user,config.password)

    @allure.story("商品列表展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_list_display(self, page: Page, config: TestConfig):
        inventory_page = self._login(page, config)
        count=inventory_page.get_product_count()
        assert count ==6,f"预期6个商品，实际{count}个"
        allure.attach(f"商品数量：{count}","统计",allure.attachment_type.TEXT)

    @allure.story("商品排序")
    @allure.severity(allure.severity_level.NORMAL)
    def test_display_sort(self,page: Page, config: TestConfig):
        inventory_page = self._login(page, config)
        inventory_page.sort_by("lohi")
        first_price=page.locator(".inventory_item_price").first.text_content()
        allure.attach(f"第一个商品价格：{first_price}","排序结果",allure.attachment_type.TEXT)
        inventory_page.sort_by("za")
        first_name=page.locator(".inventory_item_name").first.text_content()
        allure.attach(f"第一个商品名称：{first_name}","排序结果",allure.attachment_type.TEXT)

    @allure.story("商品详情页")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_detail(self, page: Page, config: TestConfig):
        inventory_page = self._login(page, config)
        page.locator(".inventory_item_name").first.click()
        assert page.get_by_text("Back to products").is_visible()