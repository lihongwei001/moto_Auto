from common.base_page import BasePage, WaitTimeoutError
from common.log_util import logger

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
        self.wait_element(self.new_msg_btn)

    def create_new_sms(self):
        self.click_element(self.new_msg_btn)

    def set_receiver(self, phone):
        self.input_text(self.receiver_input, phone)

    def set_content(self, content):
        self.input_text(self.content_input, content)
    def click_select_sim_card(self):
        self.click_element(self.sim_card_select)
    def click_sim1(self):
        self.click_element(self.sms_sim1)
    def click_sim2(self):
        self.click_element(self.sms_sim2)

    def send_sms(self):
        self.click_element(self.send_btn)
    def check_sms_content(self, target_text, timeout=30):
        """等待会话列表出现包含目标内容的短信，通信异常直接传播。"""
        element = self.driver(
            resourceId="com.android.messaging:id/conversation_snippet",
            textContains=target_text,
        )
        try:
            self.wait_until(
                lambda: bool(element.exists), bool,
                "会话列表出现目标短信", timeout,
            )
        except WaitTimeoutError:
            logger.warning(f"设备 {self.driver.serial} 在 {timeout}s 内未收到目标短信")
            return False
        logger.info("会话列表已收到目标短信")
        return True