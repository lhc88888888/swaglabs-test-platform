import allure
from playwright.sync_api import Page

class CartPage:
    def __init__(self,page:Page):
        self.page = page
        self.cart_items=page.locator(".cart_item")
        self.checkout_button=page.get_by_role("button",name="Checkout")

    def get_cart_item_count(self)->int:
        return self.cart_items.count()

    def remove_item(self,index:int=0):
        with allure.step(f"移除第{index+1}个商品"):
            self.cart_items.nth(index).get_by_text("Remove").click()

    def go_to_checkout(self):
        with allure.step("点击结算"):
            self.checkout_button.click()
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.page)