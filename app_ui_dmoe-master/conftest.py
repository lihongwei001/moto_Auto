import pytest
import json
import os
from common.log_util import logger
from common.driver_util import DriverUtil

# conftest.py所在目录=项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger.info(f"项目根目录 BASE_DIR = {BASE_DIR}")


# 增加自定义命令行参数 --serial
def pytest_addoption(parser):
    parser.addoption(
        "--serial",
        action="store",
        default="",
        help="adb设备序列号，adb devices查看"
    )


# fixture 获取命令行传入的serial
@pytest.fixture(scope="session")
def device_serial():
    json_full_path = os.path.join(BASE_DIR, "data", "data.json")
    logger.info(f"读取device_serial路径：{json_full_path}")
    assert os.path.exists(json_full_path), f"找不到文件: {json_full_path}"

    with open(json_full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    serial = data.get("DUT_SN", "")
    if not serial:
        raise ValueError("DUT_SN not found in data.json or is empty!")

    logger.info(f"当前使用设备serial: {serial}")
    return serial

@pytest.fixture(scope="session")
def sup_serial():
    json_full_path = os.path.join(BASE_DIR, "data", "data.json")
    logger.info(f"读取sup_serial路径：{json_full_path}")
    assert os.path.exists(json_full_path), f"找不到文件: {json_full_path}"

    with open(json_full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    serial = data.get("SUP_SN", "")
    if not serial:
        raise ValueError("SUP_SN not found in data.json or is empty!")

    logger.info(f"当前使用SUP设备serial: {serial}")
    return serial


# ========== driver fixture 改成依赖device_serial，不再硬编码 ==========
@pytest.fixture(scope="session")
def driver(device_serial, sup_serial):
    """
    初始化 driver，连接指定设备
    :param device_serial: 主设备序列号
    :param sup_serial: 辅助设备序列号（可选）
    """
    if not device_serial:
        raise ValueError("主设备序列号未提供！")

    # 初始化主设备 driver
    main_driver = DriverUtil.init_driver(device_serial)
    logger.info(f"主设备 {device_serial} 已连接")

    # 初始化辅助设备 driver（如果提供了序列号）
    sup_driver = None
    if sup_serial:
        try:
            sup_driver = DriverUtil.init_driver(sup_serial)
            logger.info(f"辅助设备 {sup_serial} 已连接")
        except Exception as e:
            logger.warning(f"辅助设备 {sup_serial} 连接失败，原因: {e}")

    # 返回主设备和辅助设备的 driver
    yield main_driver, sup_driver

@pytest.fixture(scope="session")
def call_data():
    json_full_path = os.path.join(BASE_DIR, "data", "data.json")
    logger.info(f"读取call_data路径：{json_full_path}")
    assert os.path.exists(json_full_path), f"找不到文件: {json_full_path}"
    with open(json_full_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def sms_data():
    json_full_path = os.path.join(BASE_DIR, "data", "data.json")
    logger.info(f"读取sms_data路径：{json_full_path}")
    assert os.path.exists(json_full_path), f"找不到文件: {json_full_path}"
    with open(json_full_path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def pin1_data():
    json_full_path = os.path.join(BASE_DIR, "data", "data.json")
    logger.info(f"读取Pin1_data路径：{json_full_path}")
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
