import uiautomator2 as u2
import time
import os

d = u2.connect()


def unlock_and_back_home():
    res = d.shell("dumpsys power").output
    screen_on = "mScreenOn=true" in res

    if not screen_on:
        d.screen_on()
        time.sleep(0.8)

    # 通用上滑解锁（所有安卓机都能用）
    d.shell("input swipe 300 1000 300 500 200")
    time.sleep(0.5)

    d.press("home")
def check_network_available():
    try:
        out = d.shell("ping -c 2 www.baidu.com").output
        return "ttl=" in out or "bytes from" in out
    except:
        return False


def init_env():
    """
    初始化：移动数据开 + WLAN关
    """
    unlock_and_back_home()
    # 移动数据
    d.shell("svc data enable")
    # WLAN
    d.shell("svc wifi disable")
    response = d.shell("settings get global airplane_mode_on")
    result_str = response.output.strip()
    apm = int(result_str)
    if apm == 1:
        # 飞行模式（设置界面不变）
        d.shell("am start -n com.android.settings/com.android.settings.SubSettings")
        time.sleep(1)
        d(text="移动网络").click()
        time.sleep(1.5)

        # 关闭飞行模式
        print("检测到飞行模式，已关闭")
        d(text="飞行模式").click()
        time.sleep(3)
    else:
        return 0

def step_test():

    # 1. 关闭移动数据
    print("1. 关闭移动数据")
    d.shell("svc data disable")
    time.sleep(1.5)

    # 2. 打开 WLAN
    print("2. 打开 WLAN")
    d.shell("svc wifi enable")
    # d.shell("am start -n com.android.settings/com.android.settings.Settings")
    # time.sleep(1)
    # d(text="网络与互联网").click()
    # time.sleep(1.5)
    # d(text="WLAN").click()
    # time.sleep(1.5)
    # d(text="使用 WLAN").click()
    time.sleep(10)


    # 3. 检查网络正常
    print("3. 检查网络是否正常")
    if check_network_available():
        print("   ✅ 网络正常")
    else:
        print("   ❌ 网络异常")
        return False

    # 4. 关闭 WLAN
    print("4. 关闭 WLAN")
    d.shell("svc wifi disable")
    time.sleep(3)

    # 5. 检查无网络
    print("5. 检查是否无网络")
    if not check_network_available():
        print("   ✅ 已无网络")
    else:
        print("   ❌ 网络未断开")
        return False

    # 6. 打开移动数据
    print("6. 打开移动数据")
    d.shell("svc data enable")
    time.sleep(3)

    d.press("Home")

    # 飞行模式（设置界面不变）
    d.shell("am start -n com.android.settings/com.android.settings.Settings")
    time.sleep(1)
    d(text="移动网络").click()
    time.sleep(1.5)

    # 7. 打开飞行模式
    print("7. 打开飞行模式")
    d(text="飞行模式").click()
    time.sleep(3)

    # 8. 检查无网络
    print("8. 检查是否无网络")
    if not check_network_available():
        print("   ✅ 已无网络")
    else:
        print("   ❌ 网络未断开")
        return False

    # 9. 关闭飞行模式
    print("9. 关闭飞行模式")
    d(text="飞行模式").click()
    time.sleep(9)

    # 10. 检查网络恢复
    print("10. 检查网络是否恢复")
    if check_network_available():
        print("   ✅ 网络恢复正常")
    else:
        print("   ❌ 网络未恢复")
        return False

    d.press("back")
    d.press("home")
    time.sleep(1)

    print("✅ 本轮全部 PASS")
    return True

if __name__ == "__main__":
    init_env()

    try:
        print("运行前请将系统语言设置为中文-清空后台")
        loop = input("循环次数（直接回车=无限）：")
        loop = int(loop) if loop.strip() else 0
    except:
        loop = 0

    count = 1
    ok_cnt = 0
    fail_cnt = 0

    while True:
        print(f"\n==================== 第 {count} 轮 ====================")
        ok = step_test()

        if ok:
            ok_cnt += 1
        else:
            fail_cnt += 1

        print(f"✅ 成功：{ok_cnt}  ❌ 失败：{fail_cnt}")

        count += 1
        if loop > 0 and count > loop:
            break

        time.sleep(2)