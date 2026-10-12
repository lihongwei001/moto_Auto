import allure
from page.sms_page import SmsPage

@allure.feature("短信模块")
@allure.story("短信收发测试")
def test_send_sms(driver, sms_data):
    sms_page = SmsPage(driver)
    data = sms_data["sms_case1"]
    with allure.step("打开短信APP"):
        sms_page.open_sms_app()
    with allure.step("新建短信，填写收件人"):
        sms_page.create_new_sms()
        sms_page.set_receiver(data["receiver"])
    with allure.step("填写短信内容并发送"):
        sms_page.set_content(data["msg_content"])
        sms_page.click_select_sim_card()
        sms_page.click_sim2()
        sms_page.send_sms()
