# -*- coding: utf-8 -*-
import uiautomator2 as u2
import time
import subprocess
from datetime import datetime

# 彩色打印常量
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
END = '\033[0m'

def adb_run(sn, cmd):
    """执行adb命令，返回输出、错误、执行码"""
    p = subprocess.run(
        ["adb", "-s", sn, "shell", cmd],
        capture_output=True,
        text=True
    )
    return p.stdout, p.stderr, p.returncode

def send_sms_by_adb(sn, receiver, msg, tap_x, tap_y):
    """纯adb完成发送，不使用uiautomator2点击"""
    # 1. adb拉起短信编辑页面
    launch_cmd = f'am start -a android.intent.action.SENDTO -d sms:{receiver} --es sms_body "{msg}"'
    out, err, code = adb_run(sn, launch_cmd)
    if code != 0:
        print(f"{RED}[{sn}] 拉起短信页面失败{END}")
        return False
    time.sleep(2.5)

    # 2. adb input tap 坐标点击发送（纯adb，不依赖u2）
    tap_cmd = f"input tap {tap_x} {tap_y}"
    tap_out, tap_err, tap_code = adb_run(sn, tap_cmd)
    time.sleep(2)

    if tap_code == 0:
        print(f"{GREEN}[{sn}] adb坐标点击执行完成{END}")
        return True
    else:
        print(f"{RED}[{sn}] adb点击执行异常{END}")
        return False

def check_receive_sms(assist_dev, send_phone, target_text):
    print("\n===== 辅助机开始校验短信 =====")
    assist_dev.press("home")
    time.sleep(1)
    assist_dev.app_start("com.android.messaging", stop=True)
    time.sleep(2)

    # 会话摘要文本匹配目标短信
    snippet_node = assist_dev(resourceId="com.android.messaging:id/conversation_snippet", textContains=target_text)
    if snippet_node.exists(timeout=3):
        print(f"【{GREEN}校验成功{END}】会话列表已收到：{target_text}")
        return True
    else:
        print(f"【{RED}校验失败{END}】未检测到目标短信：{target_text}")
        return False

def sms_cycle_test(mo_sn, assist_dev, receiver_phone, send_phone, cycle_count, click_x, click_y):
    for i in range(1, cycle_count + 1):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        content = f"modem_sms_test{i}+{now_str}"
        print(f"\n[{mo_sn}] 第{i}轮 | 接收号码:{receiver_phone} | 短信内容:{content}")

        # 纯adb发送短信
        send_result = send_sms_by_adb(mo_sn, receiver_phone, content, click_x, click_y)
        if not send_result:
            print(f"{RED}[{mo_sn}] 本轮发送失败，跳过校验{END}")
            print("-" * 60)
            continue

        print(f"[{mo_sn}] 第{i}轮短信发送完成，等待2秒接收...")
        time.sleep(2)

        # 辅助机校验短信
        check_receive_sms(assist_dev, send_phone, content)
        print("-" * 60)

if __name__ == "__main__":
    # 输入adb点击发送按钮坐标
    click_x = int(input("输入发送按钮X坐标：").strip())
    click_y = int(input("输入发送按钮Y坐标：").strip())

    # 设备、号码配置
    mo_sn = "N0OC120112"
    assist_sn = "N0OC240164"
    send_phone = "17801605642"
    receiver_phone = "16737113203"
    loop_num = int(input("输入循环发送次数：").strip())

    # 仅辅助机需要u2连接（只用来校验短信）
    print("正在连接辅助校验机...")
    d_assist = u2.connect(assist_sn)
    print("辅助机连接成功，开始测试！\n")

    sms_cycle_test(mo_sn, d_assist, receiver_phone, send_phone, loop_num, click_x, click_y)
    print(f"\n{GREEN}全部测试轮次执行完毕！{END}")