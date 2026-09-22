from common.log_util import logger
import allure
from io import BytesIO

def parse_selector(selector_str):
    """
    解析选择器字符串
    支持：resourceId:xxx , text:xxx , description:xxx , className:xxx
    特殊：xpath:xxx 单独处理，返回 ("xpath", xpath表达式)
    """
    if selector_str.startswith("xpath:"):
        expr = selector_str.replace("xpath:", "", 1)
        return ("xpath", expr)
    # 多条件普通选择器
    res = {}
    for item in selector_str.split(","):
        item = item.strip()
        k, v = item.split(":", 1)
        res[k] = v
    return ("selector", res)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_element(self, selector, timeout=10):
        logger.info(f"等待元素: {selector}")
        type_, val = parse_selector(selector)
        if type_ == "xpath":
            # xpath 单独走 xpath api
            return self.driver.xpath(val).wait(timeout=timeout)
        else:
            # resourceId / text / className 原生selector
            return self.driver(**val).wait(timeout=timeout)

    def click_element(self, selector, timeout=10):
        self.wait_element(selector, timeout)
        type_, val = parse_selector(selector)
        if type_ == "xpath":
            self.driver.xpath(val).click()
        else:
            self.driver(**val).click()
        logger.info(f"点击元素: {selector}")

    def input_text(self, selector, text, timeout=10):
        self.wait_element(selector, timeout)
        type_, val = parse_selector(selector)
        if type_ == "xpath":
            self.driver.xpath(val).set_text(text)
        else:
            self.driver(**val).set_text(text)
        logger.info(f"输入内容: {text}")

    @allure.step("页面截图")
    def screenshot(self, name):
        img = self.driver.screenshot()
        buf = BytesIO()
        img.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        allure.attach(img_bytes, name=name, attachment_type=allure.attachment_type.PNG)
