from common.log_util import logger
import allure
from io import BytesIO
import uiautomator2
from uiautomator2.exceptions import UiObjectNotFoundError
import time


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

    # 基础向上滑动    """滑动查找元素"""
    def swipe_up(self, steps=40):
        """从屏幕上半部分往下滑"""
        w, h = self.driver.window_size()
        self.driver.swipe(w * 0.5, h * 0.7, w * 0.5, h * 0.3, steps=steps)

    def swipe_down(self, steps=40):
        """从屏幕下半部分往上滑"""
        w, h = self.driver.window_size()
        self.driver.swipe(w * 0.5, h * 0.3, w * 0.5, h * 0.7, steps=steps)

    def is_element_exist(self, selector, timeout=3):
        """
        判断元素是否存在，捕获异常，返回布尔值
        :param selector: 选择器，例如 "text=挂断" / "resourceId=xxx"
        :param timeout: 等待超时时间
        :return: True存在 / False不存在
        """
        logger.info(f"【判断元素存在】selector={selector}, timeout={timeout}")
        type_, val = parse_selector(selector)
        try:
            if type_ == "xpath":
                ele = self.driver.xpath(val).wait(timeout=timeout)
            else:
                ele = self.driver(**val).wait(timeout=timeout)
            return True
        except uiautomator2.exceptions.UiObjectNotFoundError:
            return False
        except Exception as e:
            logger.warning(f"查找元素异常: {selector}, err:{str(e)}")
            return False

    def wait_element(self, selector, timeout=10):
        logger.info(f"等待元素: {selector}")
        type_, val = parse_selector(selector)
        print(f"等待元素: {selector}, type: {type_}, val: {val}")
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

    def get_element_text(self, selector, timeout=10):
        self.wait_element(selector, timeout)
        type_, val = parse_selector(selector)
        if type_ == "xpath":
            return self.driver.xpath(val).get_text()
        else:
            return self.driver(**val).get_text()

    @allure.step("页面截图")
    def screenshot(self, name):
        img = self.driver.screenshot()
        buf = BytesIO()
        img.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        allure.attach(img_bytes, name=name, attachment_type=allure.attachment_type.PNG)
