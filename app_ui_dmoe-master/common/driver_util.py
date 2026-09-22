import uiautomator2 as u2
import subprocess
from common.log_util import (logger)

class DriverUtil:
    driver = None

    @classmethod
    def init_driver(cls, serial):
        """初始化uia2驱动，adb connect设备"""
        cls.driver = u2.connect(serial)
        logger.info(f"✅ 设备 {serial} 连接成功")
        return cls.driver

    @classmethod
    def adb_shell(cls, cmd, serial):
        """adb命令封装，替代 d.info / d.window_size()"""
        res = subprocess.run(["adb", "-s", serial, "shell", cmd], capture_output=True, text=True, encoding="utf-8")
        return res.stdout.strip()

    @classmethod
    def get_screen_size(cls, serial):
        """adb获取屏幕尺寸，替代d.window_size()"""
        out = cls.adb_shell("wm size", serial)
        size_str = out.split(":")[-1].strip()
        w, h = size_str.split("x")
        return int(w), int(h)

    @classmethod
    def close_driver(cls):
        if cls.driver:
            cls.driver.app_stop_all()
            cls.driver = None
            logger.info("🔌 驱动释放完成")
