import allure
from playwright.sync_api import Page
from config.settings import TestConfig
from pages.login_page import LoginPage


@allure.feature("购物车模块")
class TestCart:

    def _login(self, page: Page, config: TestConfig):
        login_page = LoginPage(page)
        login_page.goto(config.base_url)
        return login_page.login(config.standard_user, config.password)

    @allure.story("添加商品到购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_to_cart(self, page: Page, config: TestConfig):
        inventory_page = self._login(page, config)
        # 添加第一个商品
        inventory_page.add_item_to_cart(0)
        # 验证购物车徽标数量
        assert inventory_page.get_cart_count() == 1
        # 进入购物车验证
        cart_page = inventory_page.go_to_cart()
        assert cart_page.get_cart_item_count() == 1

    @allure.story("移除购物车商品")
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_from_cart(self, page: Page, config: TestConfig):
        inventory_page = self._login(page, config)
        inventory_page.add_item_to_cart(0)
        inventory_page.add_item_to_cart(1)
        assert inventory_page.get_cart_count() == 2

        # 进入购物车，移除第一个商品
        cart_page = inventory_page.go_to_cart()
        cart_page.remove_item(0)
        assert cart_page.get_cart_item_count() == 1