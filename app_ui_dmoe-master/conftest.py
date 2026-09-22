import pytest
import json
import os
from common.log_util import logger
from common.driver_util import DriverUtil

# conftest.py所在目录=项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger.info(f"项目根目录 BASE_DIR = {BASE_DIR}")

DEVICE_SERIAL = "N4AC220456"

# ========== 缺失的driver fixture ==========
@pytest.fixture(scope="session")
def driver():
    dr = DriverUtil.init_driver(DEVICE_SERIAL)
    yield dr
    DriverUtil.close_driver()

@pytest.fixture(scope="session")
def call_data():
    json_full_path = os.path.join(BASE_DIR, "data", "call_data.json")
    logger.info(f"读取call_data路径：{json_full_path}")
    assert os.path.exists(json_full_path), f"找不到文件: {json_full_path}"
    with open(json_full_path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def sms_data():
    json_full_path = os.path.join(BASE_DIR, "data", "sms_data.json")
    logger.info(f"读取sms_data路径：{json_full_path}")
    assert os.path.exists(json_full_path), f"找不到文件: {json_full_path}"
    with open(json_full_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 失败自动截图钩子
@pytest.fixture(autouse=True)
def failure_screenshot(request, driver):
    yield
    if request.node.rep_call.failed:
        import allure
        allure.attach(driver.screenshot(), name="fail_screenshot", attachment_type=allure.attachment_type.PNG)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
