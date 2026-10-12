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
