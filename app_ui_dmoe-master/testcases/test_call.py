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
    with allure.step("挂断电话"):
        call_page.hang_up()
