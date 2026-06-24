from dataclasses import dataclass
import os

@dataclass(frozen=True)
class TestConfig:
    # 环境
    base_url: str = "https://www.saucedemo.com"
    browser_type: str = "chromium"
    headless: bool = os.getenv("CI", "false").lower() == "true"
    timeout: int = 30_000

    # 标准测试账号
    standard_user: str = "standard_user"
    locked_user: str = "locked_out_user"
    problem_user: str = "problem_user"
    password: str = "secret_sauce"