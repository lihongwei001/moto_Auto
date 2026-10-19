import allure
from page.call_page import CallPage

@allure.feature("通话模块")
@allure.story("呼叫测试")
def test_make_call(driver, call_data):
    call_page = CallPage(driver)
    data = call_data["call_case1"]
    with allure.step("打开拨号应用"):
        call_page.open_call_app()
    with allure.step("输入号码发起呼叫"):
        call_page.input_number_by_click(data["phone_number"])
        call_page.make_call()
    with allure.step("等待通话"):
        driver.sleep(data["wait_seconds"])
    # with allure.step("接听来电"):
    #     call_page.accept_incoming_call()
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

def test_answer_video_call(driver):
    call_page = CallPage(driver)
    with allure.step("接听视频来电"):
        call_page.answer_video()

def test_mo_video_call(driver):
    call_page = CallPage(driver)
    with allure.step("发起视频通话"):
        call_page.click_latest_number()
        call_page.click_video_call_button()
        call_page.click_video_call_sim2()


