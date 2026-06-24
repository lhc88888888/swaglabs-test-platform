import allure
from playwright.sync_api import Page


class InventoryPage():
    def __init__(self, page:Page):
        self.page = page
        self.product_items = page.locator(".inventory_item")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.cart_badge=page.locator(".shopping_cart_badge")
        self.cart_link=page.locator(".shopping_cart_link")

    def get_product_count(self)->int:
        return self.product_items.count()

    def sort_by(self,option:str):
        with allure.step(f"选择排序：{option}"):
            self.sort_dropdown.select_option(option)

    def add_item_to_cart(self,index:int=0)->None:
        with allure.step(f"添加第{index+1}个商品到购物车"):
            self.product_items.nth(index).get_by_text("Add to cart").click()

    def get_cart_count(self)->int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())

    def go_to_cart(self):
        with allure.step("进入购物车"):
            self.cart_link.click()
        from pages.cart_page import CartPage
        return CartPage(self.page)