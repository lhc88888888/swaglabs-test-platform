from pathlib import Path

import pytest
import yaml
from playwright.sync_api import Browser, sync_playwright, BrowserContext, Page

from config.settings import TestConfig
from utils.allure_helpers import attach_screenshot
from utils.logger import get_logger

logger=get_logger(__name__)

@pytest.fixture(scope='session')
def config()->TestConfig:
    return TestConfig()

@pytest.fixture(scope='session')
def browser(config:TestConfig)->Browser:
    with sync_playwright() as p:
        browser_instance = p.chromium.launch(headless=config.headless)
        yield browser_instance

@pytest.fixture
def context(browser:Browser,request:pytest.FixtureRequest)->BrowserContext:
    context=browser.new_context()
    context.tracing.start(screenshots=True,snapshots=True)
    yield context
    trace_dir=Path("traces")
    trace_dir.mkdir(exist_ok=True)
    context.tracing.stop(path=trace_dir/f"{request.node.name}.zip")

@pytest.fixture
def page(context:BrowserContext,config:TestConfig)->Page:
    page=context.new_page()
    page.set_default_timeout(config.timeout)
    yield page
    page.close()

def pytest_generate_tests(metafunc):
    if "login_data" in metafunc.fixturenames:
        file = Path(__file__).parent / "test_data" / "users.yaml"
        with open(file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        users = data["login_users"]   # 这是一个列表
        # 关键：用 ids 参数给每组数据起个描述名
        ids = [u["description"] for u in users]
        metafunc.parametrize("login_data", users, ids=ids)

    if "checkout_data" in metafunc.fixturenames:
        file = Path(__file__).parent / "test_data" / "checkout.yaml"
        with open(file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        checkout_list = data["checkout_info"]
        ids = [c.get("description", "") for c in checkout_list]
        metafunc.parametrize("checkout_data", checkout_list, ids=ids)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page=item.funcargs.get("page")
        if page:
            attach_screenshot(page,f"失败截图-{item.nodeid}")

