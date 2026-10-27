import time

from common.base_page import BasePage

class SmsPage(BasePage):
    sms_app_package = "com.android.messaging"
    new_msg_btn = "resourceId:com.android.messaging:id/start_new_conversation_button_activity"
    receiver_input = "xpath://android.widget.ScrollView"
    content_input = "resourceId:com.android.messaging:id/compose_message_text"
    sim_card_select = "resourceId:com.android.messaging:id/rl_sim_select"
    sms_sim1 = "xpath://*[@resource-id='com.android.messaging:id/sim_icon']"
    sms_sim2 = "xpath:(//*[@resource-id='com.android.messaging:id/sim_icon'])[2]"
    send_btn = "resourceId:com.android.messaging:id/send_icon"
    latest_sms_content_selector = "resourceId:com.android.messaging:id/conversation_snippet"

    def open_sms_app(self):
        self.driver.app_start(self.sms_app_package, stop=True)

    def create_new_sms(self):
        self.click_element(self.new_msg_btn)

    def set_receiver(self, phone):
        self.input_text(self.receiver_input, phone)

    def set_content(self, content):
        self.input_text(self.content_input, content)
    def click_select_sim_card(self):
        self.click_element(self.sim_card_select)
        time.sleep(2)
    def click_sim1(self):
        self.click_element(self.sms_sim1)
    def click_sim2(self):
        self.click_element(self.sms_sim2)

    def send_sms(self):
        self.click_element(self.send_btn)
    def check_sms_content(self, target_text):
        """获取最新一条短信的内容"""
        if self.driver(resourceId="com.android.messaging:id/conversation_snippet", textContains=target_text).exists(timeout=5):
            print(f"【校验成功】会话列表已收到：{target_text}")
            return True
        else:
            print(f"【校验失败】未检测到目标短信：{target_text}")
            return False