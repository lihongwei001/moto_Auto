import allure
from page.call_page import CallPage

@allure.feature("通话模块")
@allure.story("呼叫测试")
#DUT_sim1 呼叫 SUP_sim1
def call_D1S1(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim1"]
    with allure.step("DUT_sim1拨打电话"):
        call_page.voice_dial(data["receiver"], sim_slot=1)
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("sup接听来电"):
        sup_page.accept_incoming_call()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=1, expected=2)
        sup_page.wait_call_state(sim_slot=1, expected=2)

#DUT_sim1 呼叫 SUP_sim2
def call_D1S2(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim2"]
    with allure.step("DUT_sim1拨打电话"):
        call_page.voice_dial(data["receiver"], sim_slot=1)
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("sup接听来电"):
        sup_page.accept_incoming_call()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=1, expected=2)
        sup_page.wait_call_state(sim_slot=2, expected=2)
#DUT_sim2 呼叫 SUP_sim1
def call_D2S1(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim1"]
    with allure.step("DUT_sim2拨打电话"):
        call_page.voice_dial(data["receiver"], sim_slot=2)
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("sup接听来电"):
        sup_page.accept_incoming_call()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=2, expected=2)
        sup_page.wait_call_state(sim_slot=1, expected=2)
#DUT_sim2 呼叫 SUP_sim2
def call_D2S2(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim2"]
    with allure.step("DUT_sim2拨打电话"):
        call_page.voice_dial(data["receiver"], sim_slot=2)
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("sup接听来电"):
        sup_page.accept_incoming_call()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=2, expected=2)
        sup_page.wait_call_state(sim_slot=2, expected=2)
#DUT_sim1 video呼叫 SUP_sim1
def video_call_D1S1(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim1"]
    with allure.step("DUT_sim1拨打视频电话"):
        call_page.video_dial(data["receiver"], sim_slot=1)
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("sup接听视频来电"):
        sup_page.answer_video()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=1, expected=2)
        sup_page.wait_call_state(sim_slot=1, expected=2)
#DUT_sim1 video呼叫 SUP_sim2
def video_call_D1S2(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim2"]
    with allure.step("DUT_sim1拨打视频电话"):
        call_page.video_dial(data["receiver"], sim_slot=1)
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("sup接听视频来电"):
        sup_page.answer_video()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=1, expected=2)
        sup_page.wait_call_state(sim_slot=2, expected=2)
#DUT_sim2 video呼叫 SUP_sim1
def video_call_D2S1(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim1"]
    with allure.step("DUT_sim2拨打视频电话"):
        call_page.video_dial(data["receiver"], sim_slot=2)
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("sup接听视频来电"):
        sup_page.answer_video()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=2, expected=2)
        sup_page.wait_call_state(sim_slot=1, expected=2)
def video_call_D2S2(main_driver, sup_driver, call_data):
    call_page = CallPage(main_driver)
    sup_page = CallPage(sup_driver)
    data = call_data["SUP_sim2"]
    with allure.step("DUT_sim2拨打视频电话"):
        call_page.video_dial(data["receiver"], sim_slot=2)
    with allure.step("等待通话"):
        main_driver.sleep(data["wait_seconds"])
    with allure.step("sup接听视频来电"):
        sup_page.answer_video()
    with allure.step("等待双方进入通话状态"):
        call_page.wait_call_state(sim_slot=2, expected=2)
        sup_page.wait_call_state(sim_slot=2, expected=2)
#DUT挂断电话
def hang_up_DUT(main_driver):
    call_page = CallPage(main_driver)
    with allure.step("DUT挂断电话"):
        call_page.hang_up()
    with allure.step("检查双方通话是否为空闲状态"):
        call_page.wait_call_state(sim_slot=1, expected=0)
        call_page.wait_call_state(sim_slot=2, expected=0)

# SUP挂断电话
def hang_up_SUP(sup_driver):
    sup_page = CallPage(sup_driver)
    with allure.step("sup挂断电话"):
        sup_page.hang_up()
    with allure.step("检查通话是否为空闲状态"):
        sup_page.wait_call_state(sim_slot=1, expected=0)
        sup_page.wait_call_state(sim_slot=2, expected=0)

# SUP2挂断电话
def hang_up_SUP2(sup2_driver):
    sup2_page = CallPage(sup2_driver)
    with allure.step("sup2挂断电话"):
        sup2_page.hang_up()
    with allure.step("检查通话是否为空闲状态"):
        sup2_page.wait_call_state(sim_slot=1, expected=0)
        sup2_page.wait_call_state(sim_slot=2, expected=0)
def other_call_Action(main_driver):
    call_page = CallPage(main_driver)
    with allure.step("打开呼叫保持"):
        call_page.hold_call()
    with allure.step("升级为视频"):
        call_page.switch_to_videoCall()
    with allure.step("打开静音"):
        call_page.mute()
    with allure.step("添加通话"):
        call_page.add_call()
    with allure.step("打开扬声器"):
        call_page.call_speaker()
    with allure.step("挂断电话"):
        call_page.hang_up()


