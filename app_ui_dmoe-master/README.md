POM_AutoTest/
├── common/                     # 基础层
│   ├── driver_util.py        # 驱动管理：uia2初始化、adb封装、设备连接、关闭
│   ├── base_page.py          # BasePage：所有页面父类，封装通用点击、输入、等待、截图
│   └── log_util.py           # 日志工具，输出文件+控制台
├── pages/                    # 页面对象层 POM
│   ├── call_page.py          # 通话页面：拨号、呼叫、接听、挂断元素+操作方法
│   └── sms_page.py           # 短信页面：新建短信、输入号码、输入内容、发送、读取短信
├── data/                     # 数据层 json文件
│   ├── call_data.json        # 通话测试数据：被叫号码、等待时长
│   └── sms_data.json         # 短信测试数据：收件人号码、短信内容
├── testcases/                # 测试用例层 pytest
│   ├── test_call.py
│   └── test_sms.py
├── allure-results/           # allure原始结果（自动生成，不用手动建）
├── logs/                     # 日志存放目录
├── conftest.py               # pytest钩子：全局fixture（驱动初始化/销毁，allure截图钩子）
├── pytest.ini                # pytest配置文件
└── requirements.txt          # 依赖清单
