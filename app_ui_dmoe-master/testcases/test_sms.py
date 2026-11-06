import allure
from page.sms_page import SmsPage
from datetime import datetime

@allure.feature("短信模块")
@allure.story("短信收发测试")
def test_send_sms(main_driver, sup_driver, sms_data):
    sms_page = SmsPage(main_driver)
    sup_page = SmsPage(sup_driver)
    data = sms_data["SUP_sim1"]
    with allure.step("打开短信APP"):
        sms_page.open_sms_app()
    with allure.step("新建短信，填写收件人"):
        sms_page.create_new_sms()
        sms_page.set_receiver(data["receiver"])
    with allure.step("填写短信内容并发送"):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        sms_page.set_content(now_str)
        sms_page.click_select_sim_card()
        sms_page.click_sim2()
        sms_page.send_sms()
    with allure.step("辅助机接收短信并校验内容"):
        sup_page.open_sms_app()
        assert sup_page.check_sms_content(now_str), "辅助机未在期限内收到目标短信"
