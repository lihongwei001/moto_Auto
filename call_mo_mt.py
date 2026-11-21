# -*- coding: utf-8 -*-
import uiautomator2 as u2
import time
import subprocess

def adb_shell(sn, cmd):
    """通用adb shell执行函数"""
    p = subprocess.Popen(["adb", "-s", sn, "shell", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    return out.strip()

def wake_up_screen(sn):
    """adb唤醒屏幕，替代dev.screen_on()"""
    adb_shell(sn, "input keyevent 26")
    time.sleep(1.2)

def get_call_state(dev):
    """
    获取电话状态，底层telephony.registry 双卡兼容
    return 0空闲 1响铃 2通话中
    """
    res_obj = dev.shell("dumpsys telephony.registry")
    res = res_obj.output
    state_list = []
    lines = res.splitlines()
    for line in lines:
        if "mCallState=" in line:
            val = line.split("=")[-1].strip()
            state_list.append(int(val))
    if 2 in state_list:
        return 2
    elif 1 in state_list:
        return 1
    else:
        return 0

def wait_ringing(dev, timeout=12):
    """等待设备进入响铃状态 mCallState=1"""
    print(f"[{dev.serial}] 等待来电响铃...")
    for _ in range(timeout):
        if get_call_state(dev) == 1:
            print(f"[{dev.serial}] 检测到来电响铃")
            return True
        time.sleep(1)
    raise Exception(f"[{dev.serial}] 等待响铃超时，未收到来电")

def is_talking(dev, retry=3, wait=1):
    """重试判断是否处于通话接通状态 mCallState=2"""
    for _ in range(retry):
        if get_call_state(dev) == 2:
            return True
        time.sleep(wait)
    return False

def is_idle(dev, retry=3, wait=1):
    """重试判断是否回到空闲挂断状态 mCallState=0"""
    for _ in range(retry):
        if get_call_state(dev) == 0:
            return True
        time.sleep(wait)
    return False

def init_device(sn):
    """纯adb实现，移除自动亮屏唤醒逻辑"""
    dev = u2.connect(sn)
    # 清理异常uia2服务
    adb_shell(sn, "am force-stop com.wetest.uia2.stub; killall atx-agent")
    time.sleep(2)
    dev.press("home")
    time.sleep(0.5)
    return dev

def dial_call(dev, target_phone):
    print(f"[{dev.serial}] 打开拨号盘，准备拨打 {target_phone}")
    dev.app_start("com.android.dialer", stop=True)
    # dev(resourceId="com.android.dialer:id/fab").click()
    time.sleep(1.8)

    num_input = dev(className="android.widget.EditText")
    if num_input.exists(timeout=1):
        num_input.clear_text()
        num_input.set_text(target_phone)
    else:
        for num in target_phone:
            dev(text=num).click(timeout=0.2)
            time.sleep(0.1)
    time.sleep(1.2)

    dial_ok = False
    # 第一层：限定拨号面板内 包含“sim1”
    dial_panel = dev(resourceId="com.android.dialer:id/sim_card_0")
    if dial_panel.exists(timeout=1):
        dial_btn = dev(resourceId="com.android.dialer:id/sim_card_0")
        if dial_btn.exists(timeout=1.2):
            dial_btn.click()
            dial_ok = True
            print(f"[{dev.serial}] 在拨号面板匹配到sim1按钮，执行拨号")

    # 第二层：面板内找不到，全局页面搜索含“中国”按钮兜底
    if not dial_ok:
        dial_btn_all = dev(resourceId="resourceId:com.android.dialer:id/lable_sim1")
        if dial_btn_all.exists(timeout=1):
            dial_btn_all.click()
            dial_ok = True
            print(f"[{dev.serial}] 全局页面匹配到含「中国」按钮，执行拨号")

    # 兜底：完全找不到文字按钮，用系统标准拨号ID
    if not dial_ok:
        print(f"[{dev.serial}] 未找到带「中国」文字按钮，使用通用拨号键兜底")
        if dev(resourceId="com.android.dialer:id/dialButton").exists(timeout=1):
            dev(resourceId="com.android.dialer:id/dialButton").click()
        else:
            dev(textContains="拨打电话").click()
    time.sleep(2)

def answer_incoming(dev):
    """adb按键接听来电"""
    print(f"[{dev.serial}] 执行adb接听按键 KEYCODE_CALL=5")
    dev.shell("input keyevent 5")
    time.sleep(4)

def hangup_call(dev):
    """adb按键挂断通话"""
    print(f"[{dev.serial}] 使用adb按键挂断通话 KEYCODE_ENDCALL=6")
    dev.shell("input keyevent 6")
    time.sleep(2)
    dev.press("home")

def single_call_flow(caller_sn, caller_phone, callee_sn, callee_phone):
    print("\n==================== 本次流程：{} 呼叫 {} ====================".format(caller_sn, callee_sn))
    caller_dev = init_device(caller_sn)
    callee_dev = init_device(callee_sn)

    # 1. 主叫拨号呼出
    dial_call(caller_dev, callee_phone)

    # 2. 等待被叫响铃（新增响铃状态判断）
    wait_ringing(callee_dev)

    # 3. 被叫执行接听
    answer_incoming(callee_dev)

    # 4. ADB校验双方是否成功接通通话(mCallState=2)
    time.sleep(4)
    caller_connected = is_talking(caller_dev)
    callee_connected = is_talking(callee_dev)

    print(f"[{caller_dev.serial}] 通话状态：{'已接通通话中' if caller_connected else '未接通异常'}")
    print(f"[{callee_dev.serial}] 通话状态：{'已接通通话中' if callee_connected else '未接通异常'}")
    if not (caller_connected and callee_connected):
        raise Exception("通话建立失败，至少一方未进入ACTIVE通话状态")

    # 保持通话5秒
    time.sleep(5)

    # 5. 主叫挂断
    hangup_call(caller_dev)

    # 6. ADB校验挂断后双方回到空闲(mCallState=0)
    time.sleep(4)
    caller_idle = is_idle(caller_dev)
    callee_idle = is_idle(callee_dev)

    print(f"[{caller_dev.serial}] 挂断后状态：{'挂断正常(空闲)' if caller_idle else '挂断异常，仍通话中'}")
    print(f"[{callee_dev.serial}] 挂断后状态：{'挂断正常(空闲)' if callee_idle else '挂断异常，仍通话中'}")
    if not (caller_idle and callee_idle):
        raise Exception("挂断失败，设备未回到空闲状态，仍处于通话")

    print("==================== 本轮通话流程完成 ====================\n")
    time.sleep(3)

if __name__ == "__main__":
    test_sn = input("请输入【测试机】序列号：").strip()
    test_phone = input("请输入【测试机】本机手机号：").strip()
    aux_sn = input("请输入【辅助机】序列号：").strip()
    aux_phone = input("请输入【辅助机】本机手机号：").strip()
    loop_count = int(input("请输入需要循环测试总次数：").strip())

    for current_round in range(1, loop_count + 1):
        print(f"\n========== 第 {current_round} / {loop_count} 轮测试 ==========")
        try:
            print("===== 流程1：测试机呼叫辅助机 =====")
            single_call_flow(
                caller_sn=test_sn,
                caller_phone=test_phone,
                callee_sn=aux_sn,
                callee_phone=aux_phone
            )

            print("===== 流程2：辅助机呼叫测试机 =====")
            single_call_flow(
                caller_sn=aux_sn,
                caller_phone=aux_phone,
                callee_sn=test_sn,
                callee_phone=test_phone
            )
            print(f"========== 第 {current_round} 轮全部双向通话完成 ==========\n")
        except Exception as e:
            print(f"第{current_round}轮执行异常：{e}")
            print("终止脚本")
            break

    print("\n全部循环测试执行完毕！")