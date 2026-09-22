# # -*- coding: utf-8 -*-
# import uiautomator2 as u2
# import time
# import subprocess
#
# def adb_run(sn, cmd):
#     p = subprocess.run(
#         ["adb", "-s", sn, "shell", cmd],
#         capture_output=True,
#         text=True
#     )
#     return p.stdout, p.stderr, p.returncode
#
# def send_sms_by_app_activity(dev, receiver, msg):
#     sn = dev.serial
#     # 1. 显式启动Google Messaging会话列表首页
#     launch_cmd = f'am start com.google.android.apps.messaging/com.google.android.apps.messaging.ui.ConversationListActivity'
#     adb_run(sn, launch_cmd)
#     time.sleep(2)
#
#     # 2. 点击新建短信按钮（新建会话）
#     try:
#         dev(text="Start chat").wait(timeout=4).click()
#     except Exception:
#         dev(description="Create new conversation").wait(timeout=4).click()
#     time.sleep(1)
#
#     # 3. 输入接收手机号
#     dev(resourceId="com.google.android.apps.messaging:id/recipient_text_view").set_text(receiver)
#     time.sleep(1)
#     # 点击匹配到的联系人会话
#     dev(textContains=receiver).wait(timeout=3).click()
#     time.sleep(1)
#
#     # 4. 输入短信内容
#     input_box = dev(resourceId="com.google.android.apps.messaging:id/compose_message_text")
#     input_box.wait(timeout=4).click()
#     dev.set_text(msg)
#     time.sleep(1)
#
#     # 5. 无坐标点击发送按钮：通过Send SMS向上找可点击父容器
#     try:
#         dev(resourceId="Compose:Draft:Send").click()
#     except Exception:
#         # 兜底坐标（你原有备用点位）
#         dev(description="SMS").parent(clickable=True).wait(timeout=5).click()
#     time.sleep(1)
#     return True
#
# def sms_cycle_test(dev, receiver, cycle_count):
#     sn = dev.serial
#     for i in range(1, cycle_count + 1):
#         content = f"modem_sms_test{i}"
#         print(f"[{sn}] 第{i}轮 | 目标号码:{receiver} | 短信内容:{content}")
#         send_sms_by_app_activity(dev, receiver, content)
#         print(f"[{sn}] 第{i}轮短信发送完成\n")
#         time.sleep(2)  # 每轮间隔2秒，可自行调整
#
# if __name__ == "__main__":
#     loop_num = int(input("输入循环发送次数：").strip())
#     d_mo = u2.connect("N2FM220269")
#     # 号码不带+，内部页面会自动补全
#     sms_cycle_test(d_mo, "17801605642", loop_num)

# -*- coding: utf-8 -*-
import uiautomator2 as u2
import time
import subprocess
from datetime import datetime
RED = '\033[31m'
GREEN = '\033[32m'
END = '\033[0m'

def adb_run(sn, cmd):
    p = subprocess.run(
        ["adb", "-s", sn, "shell", cmd],
        capture_output=True,
        text=True
    )
    return p.stdout, p.stderr, p.returncode

def send_sms_intent(dev, receiver, msg):
    sn = dev.serial
    # 拉起短信编辑页面
    cmd = f'am start -a android.intent.action.SENDTO -d sms:{receiver} --es sms_body "{msg}"'
    out, err, code = adb_run(sn, cmd)
    time.sleep(2.5)
    # 点击发送按钮，异常兜底坐标
    try:
        dev(resourceId="Compose:Draft:Send").click()
    except Exception:
        dev.click(1130, 1755)
        # dev.click(1015, 780)
    time.sleep(2)
    return code == 0

def check_receive_sms(assist_dev, send_phone, target_text):
    print("\n===== 辅助机开始校验短信 =====")
    assist_dev.press("home")
    time.sleep(1)
    assist_dev.app_start("com.google.android.apps.messaging", stop=True)
    time.sleep(2)

    # 直接定位会话摘要控件，匹配短信内容
    if assist_dev(resourceId="com.google.android.apps.messaging:id/conversation_snippet", textContains=target_text).exists(timeout=3):
        print(f"【{GREEN}校验成功{END}】会话列表已收到：{target_text}")
        return True
    else:
        print(f"【{RED}校验失败{END}】未检测到目标短信：{target_text}")
        return False
def sms_cycle_test(mo_dev, assist_dev, receiver_phone, send_phone, cycle_count):
    mo_sn = mo_dev.serial
    for i in range(1, cycle_count + 1):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        content = f"modem_sms_test{i}+{now_str}"
        print(f"\n[{mo_sn}] 第{i}轮 | 接收号码:{receiver_phone} | 短信内容:{content}")
        send_sms_intent(mo_dev, receiver_phone, content)
        print(f"[{mo_sn}] 第{i}轮短信发送完成，等待2秒接收...")
        time.sleep(2)

        # 调用辅助机校验函数
        check_receive_sms(assist_dev, send_phone, content)
        print("-" * 60)


if __name__ == "__main__":
    # 交互式输入所有设备与号码信息
    mo_sn = input("【发送机】设备序列号：").strip()
    assist_sn = input("【辅助校验机】设备序列号：").strip()
    send_phone = input("【发送机本机号码(不加+86)】：").strip()
    receiver_phone = input("【接收手机号(不加+86)】：").strip()
    # mo_sn = "N0OC120112"
    # assist_sn = "N0OC240164"
    # send_phone = "17801605642"
    # receiver_phone = "16737113203"
    loop_num = int(input("输入循环发送次数：").strip())
    # 连接两台设备
    print("正在连接发送机...")
    d_mo = u2.connect(mo_sn)
    print("正在连接辅助校验机...")
    d_assist = u2.connect(assist_sn)
    print("两台设备连接成功，开始测试！\n")

    # 执行循环发送+每轮校验
    sms_cycle_test(d_mo, d_assist, receiver_phone, send_phone, loop_num)
    print("\n全部测试轮次执行完毕！")