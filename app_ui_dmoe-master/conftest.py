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


@pytest.fixture(scope="session")
def test_data():
    json_full_path = os.path.join(BASE_DIR, "data", "data.json")
    logger.info(f"读取测试配置：{json_full_path}")
    with open(json_full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("data.json 顶层必须是 JSON 对象")
    return data
@pytest.fixture(scope="session")
def device_serials(request, test_data):
    serials = {}
    for role, key in (("main", "DUT_SN"), ("sup", "SUP_SN"), ("sup2", "SUP2_SN")):
        value = test_data.get(key, "")
        if role == "main":
            override = request.config.getoption("--serial")
            if override != "":
                value = override
        if not isinstance(value, str):
            raise ValueError(f"{key} 必须是字符串")
        serials[role] = value.strip()

    configured = [serial for serial in serials.values() if serial]
    if len(configured) != len(set(configured)):
        raise ValueError("main、sup、sup2 必须使用不同的设备序列号")
    return serials


@pytest.fixture(scope="session")
def device_serial(device_serials):
    return device_serials["main"]


@pytest.fixture(scope="session")
def sup_serial(device_serials):
    return device_serials["sup"]


@pytest.fixture(scope="session")
def sup2_serial(device_serials):
    return device_serials["sup2"]


@pytest.fixture(scope="session")
def connected_devices():
    devices = {}
    yield devices
    devices.clear()
    logger.info("已释放框架持有的设备引用，未停止应用或断开 ADB")


def _connect_device(role, key, serial, connected_devices):
    if not serial:
        raise ValueError(f"{role} 用例需要设备，请配置 {key}")
    logger.info(f"正在连接 {role} 设备 {serial}")
    device = DriverUtil.init_driver(serial)
    connected_devices[role] = device
    return device


@pytest.fixture(scope="session")
def main_driver(device_serial, connected_devices):
    return _connect_device("main", "DUT_SN", device_serial, connected_devices)


@pytest.fixture(scope="session")
def sup_driver(sup_serial, connected_devices):
    return _connect_device("sup", "SUP_SN", sup_serial, connected_devices)


@pytest.fixture(scope="session")
def sup2_driver(sup2_serial, connected_devices):
    return _connect_device("sup2", "SUP2_SN", sup2_serial, connected_devices)


@pytest.fixture(scope="session")
def driver(request, main_driver, device_serials):
    """兼容入口：连接主机及已配置的辅助机，固定返回三个位置。"""
    sup = request.getfixturevalue("sup_driver") if device_serials["sup"] else None
    sup2 = request.getfixturevalue("sup2_driver") if device_serials["sup2"] else None
    return main_driver, sup, sup2


@pytest.fixture(scope="session")
def call_data(test_data):
    return test_data


@pytest.fixture(scope="session")
def sms_data(test_data):
    return test_data


@pytest.fixture(scope="session")
def pin1_data(test_data):
    return test_data


# 失败自动截图钩子
@pytest.fixture(autouse=True)
def failure_screenshot(request, connected_devices):
    yield
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        from common.base_page import BasePage

        for role, device in connected_devices.items():
            if f"{role}_driver" in request.fixturenames or "driver" in request.fixturenames:
                try:
                    BasePage(device).screenshot(f"fail_screenshot_{role}")
                except Exception:
                    logger.exception(f"{role} 设备失败截图采集异常")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
