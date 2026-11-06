import allure
from page.call_page import CallPage

@allure.feature("通话模块")
@allure.story("呼叫测试")
def test_make_call(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim1"]
    with allure.step("打开拨号应用"):
        call_page.open_call_app()
    with allure.step("输入号码发起呼叫"):
        call_page.input_number_by_click(data["receiver"])
        call_page.make_call()
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("接听来电"):
        sup_page.accept_incoming_call()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=1, expected=2)
        sup_page.wait_call_state(sim_slot=1, expected=2)
    # with allure.step("拒接来电"):
    #     call_page.disaccept_incoming_call()
    # with allure.step("打开呼叫保持"):
    #     call_page.hold_call()
    # with allure.step("升级为视频"):
    #     call_page.switch_to_videoCall()
    # with allure.step("打开静音"):
    #     call_page.mute()
    # with allure.step("添加通话"):
    #     call_page.add_call()
    # with allure.step("打开扬声器"):
    #     call_page.call_speaker()
    with allure.step("挂断电话"):
        call_page.hang_up()

def test_answer_video_call(main_driver):
    call_page = CallPage(main_driver)
    with allure.step("接听视频来电"):
        call_page.answer_video()

def test_mo_video_call(main_driver):
    call_page = CallPage(main_driver)
    with allure.step("发起视频通话"):
        call_page.click_latest_number()
        call_page.click_video_call_button()
        call_page.click_video_call_sim2()


def test_check_call_state(main_driver):
    call_page = CallPage(main_driver)

    # 获取 SIM1 状态
    sim1 = call_page.get_call_state(sim_slot=1)
    print(f"SIM1：{sim1['call_state_name']}")
    print(f"SIM1 是否保持：{sim1['is_holding']}")

    # 获取 SIM2 状态
    sim2 = call_page.get_call_state(sim_slot=2)
    print(f"SIM2：{sim2['call_state_name']}")
    print(f"SIM2 是否保持：{sim2['is_holding']}")

    state = call_page.get_call_state(sim_slot=2)
    # 判断空闲
    assert state["call_state"] == 0, f"SIM2 未处于空闲状态：{state}"

    # # 判断响铃
    # assert state["call_state"] == 1, f"SIM1 未处于响铃状态：{state}"
    #
    # # 判断通话中（此字段本身不能区分正常通话和保持）
    # assert state["call_state"] == 2, f"SIM1 未处于通话状态：{state}"
    #
    # # 判断保持
    # assert state["is_holding"], f"SIM1 未进入保持状态：{state}"