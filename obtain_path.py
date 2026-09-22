import uiautomator2 as u2
import time

if __name__ == "__main__":
    sn = input("输入设备SN：").strip()
    dev = u2.connect(sn)

    # 直接抓取当前前台页面XML，不跳转短信、不填号码
    hierarchy = dev.dump_hierarchy()

    print("==========页面控件布局开始==========")
    print(hierarchy)
    print("==========页面控件布局结束==========")

    with open("current_window1.xml", "w", encoding="utf-8") as f:
        f.write(hierarchy)

    print("\n当前窗口布局已保存 current_window.xml")