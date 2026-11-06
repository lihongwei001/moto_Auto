import uiautomator2 as u2
import subprocess
import re
from common.log_util import (logger)

class DriverUtil:
    @staticmethod
    def init_driver(serial):
        """连接指定设备，设备对象由调用方持有。"""
        driver = u2.connect(serial)
        logger.info(f"✅ 设备 {serial} 连接成功")
        return driver

    @classmethod
    def adb_shell(cls, cmd, serial, timeout=10):
        """adb命令封装，替代 d.info / d.window_size()"""
        try:
            res = subprocess.run(
                ["adb", "-s", serial, "shell", cmd],
                capture_output=True, text=True, encoding="utf-8", timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError(
                f"设备 {serial} ADB 命令超时：{cmd!r}，timeout={timeout}s"
            ) from exc
        if res.returncode != 0:
            raise RuntimeError(
                f"设备 {serial} ADB 命令失败：{cmd!r}，"
                f"退出码={res.returncode}，stderr={res.stderr.strip()}，"
                f"stdout={res.stdout.strip()}"
            )
        return res.stdout.strip()

    @staticmethod
    def device_shell(driver, cmd, timeout=10):
        result = driver.shell(cmd, timeout=timeout)
        if result.exit_code != 0:
            raise RuntimeError(
                f"设备 {driver.serial} Shell 命令失败：{cmd!r}，"
                f"退出码={result.exit_code}，输出={result.output}"
            )
        return result.output.strip()

    @classmethod
    def get_screen_size(cls, serial, timeout=10):
        """adb获取屏幕尺寸，替代d.window_size()"""
        out = cls.adb_shell("wm size", serial, timeout=timeout)
        matches = re.findall(
            r"^(?:Physical|Override) size:\s*(\d+)x(\d+)\s*$",
            out, re.MULTILINE,
        )
        if not matches:
            raise RuntimeError(f"设备 {serial} 屏幕尺寸输出无法解析：{out!r}")
        w, h = map(int, matches[-1])
        if w <= 0 or h <= 0:
            raise RuntimeError(f"设备 {serial} 屏幕尺寸无效：{out!r}")
        return w, h
