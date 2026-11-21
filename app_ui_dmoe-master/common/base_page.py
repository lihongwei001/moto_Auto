from common.log_util import logger
import allure
from io import BytesIO
import math
import time


class WaitTimeoutError(TimeoutError):
    """等待条件未在期限内满足，与设备通信异常区分。"""


def parse_selector(selector_str):
    """
    解析选择器字符串
    支持：resourceId:xxx , text:xxx , description:xxx , className:xxx
    特殊：xpath:xxx 单独处理，返回 ("xpath", xpath表达式)
    """
    if not isinstance(selector_str, str) or not selector_str.strip():
        raise ValueError("定位符必须是非空字符串")
    selector_str = selector_str.strip()
    if selector_str.startswith("xpath:"):
        expr = selector_str[len("xpath:"):].strip()
        if not expr:
            raise ValueError("XPath 表达式不能为空")
        return ("xpath", expr)
    # 多条件普通选择器

    res = {}
    for item in selector_str.split(","):
        item = item.strip()
        if ":" not in item:
            raise ValueError(f"定位条件缺少冒号：{item!r}")
        k, v = item.split(":", 1)
        k, v = k.strip(), v.strip()
        if not k or not v or k in res:
            raise ValueError(f"定位条件为空或重复：{item!r}")
        res[k] = v
    return ("selector", res)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_until(self, read, predicate, description, timeout=10, interval=0.2):
        if not math.isfinite(timeout) or timeout < 0:
            raise ValueError("timeout 必须是非负有限数值")
        if not math.isfinite(interval) or interval <= 0:
            raise ValueError("interval 必须是正有限数值")
        deadline = time.monotonic() + timeout
        while True:
            value = read()
            if predicate(value):
                return value
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise WaitTimeoutError(
                    f"设备 {self.driver.serial} 等待超时：{description}，"
                    f"timeout={timeout}s，最后结果={value!r}"
                )
            time.sleep(min(interval, remaining))

    # 基础向上滑动    """滑动查找元素"""
    def swipe_up(self, steps=40):
        """手指向上滑动，查看列表下方内容。"""
        w, h = self.driver.window_size()
        self.driver.swipe(w * 0.5, h * 0.7, w * 0.5, h * 0.3, steps=steps)

    def swipe_down(self, steps=40):
        """手指向下滑动，查看列表上方内容。"""
        w, h = self.driver.window_size()
        self.driver.swipe(w * 0.5, h * 0.3, w * 0.5, h * 0.7, steps=steps)

    def is_element_exist(self, selector, timeout=3):
        """
        判断元素是否在期限内出现，设备与定位异常直接传播。
        :param selector: 选择器，例如 "text:挂断" / "resourceId:xxx"
        :param timeout: 等待超时时间
        :return: True存在 / False不存在
        """
        try:
            self.wait_element(selector, timeout)
            return True
        except WaitTimeoutError:
            return False

    def wait_element(self, selector, timeout=10):
        if not math.isfinite(timeout) or timeout < 0:
            raise ValueError("timeout 必须是非负有限数值")
        type_, val = parse_selector(selector)
        print(f"等待元素: {selector}, type: {type_}, val: {val}")
        if type_ == "xpath":
            matches = self.wait_until(
                lambda: self.driver.xpath(val).all(),
                bool, f"元素 {selector}", timeout,
            )
            return matches[0]
        element = self.driver(**val)
        self.wait_until(
            lambda: bool(element.exists), bool,
            f"元素 {selector}", timeout,
        )
        return element

    def wait_element_gone(self, selector, timeout=10):
        self.wait_until(
            lambda: self.is_element_exist(selector, timeout=0),
            lambda exists: not exists,
            f"元素消失 {selector}", timeout,
        )

    def scroll_to_element(self, selector, max_swipes=5, timeout=1):
        if not isinstance(max_swipes, int) or max_swipes < 0:
            raise ValueError("max_swipes 必须是非负整数")
        for attempt in range(max_swipes + 1):
            try:
                return self.wait_element(selector, timeout)
            except WaitTimeoutError:
                if attempt == max_swipes:
                    raise WaitTimeoutError(
                        f"设备 {self.driver.serial} 滑动查找失败："
                        f"{selector}，最多滑动 {max_swipes} 次"
                    ) from None
                self.swipe_up()
    def scroll_to_element_down(self, selector, max_swipes=5, timeout=1):
        if not isinstance(max_swipes, int) or max_swipes < 0:
            raise ValueError("max_swipes 必须是非负整数")
        for attempt in range(max_swipes + 1):
            try:
                return self.wait_element(selector, timeout)
            except WaitTimeoutError:
                if attempt == max_swipes:
                    raise WaitTimeoutError(
                        f"设备 {self.driver.serial} 滑动查找失败："
                        f"{selector}，最多滑动 {max_swipes} 次"
                    ) from None
                self.swipe_down()
    def click_element(self, selector, timeout=10):
        type_, _ = parse_selector(selector)
        element = self.wait_element(selector, timeout)
        if type_ == "xpath":
            element.click()
        else:
            element.click(timeout=0)
        logger.info(f"点击元素: {selector}")

    def input_text(self, selector, text, timeout=10):
        type_, _ = parse_selector(selector)
        element = self.wait_element(selector, timeout)
        if type_ == "xpath":
            element.click()
            self.driver.clear_text()
            self.driver.send_keys(text)
        else:
            element.set_text(text, timeout=0)
        logger.info("文本输入完成，未记录输入内容")

    def get_element_text(self, selector, timeout=10):
        type_, _ = parse_selector(selector)
        element = self.wait_element(selector, timeout)
        if type_ == "xpath":
            return element.text
        else:
            return element.get_text(timeout=0)

    @allure.step("页面截图")
    def screenshot(self, name):
        img = self.driver.screenshot()
        buf = BytesIO()
        img.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        allure.attach(img_bytes, name=name, attachment_type=allure.attachment_type.PNG)
