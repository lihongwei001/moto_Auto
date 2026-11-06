# Android UI 自动化测试框架

基于 **Python + pytest + uiautomator2 + Allure** 的 Android 真机 UI 自动化测试项目，采用 POM（Page Object Model，页面对象模式）组织代码，面向通话、短信、双卡及系统设置等测试场景。

**项目当前处于开发阶段。** 已具备基础分层、按需设备连接、统一条件等待及失败截图能力，但部分业务断言、页面适配及状态恢复仍待完善。本文描述当前实现，不代表所有用例已验证可运行。

## 1. 技术栈与测试范围

| 组件 | 用途 |
|---|---|
| Python | 编写公共能力、页面对象和测试用例 |
| pytest | 用例发现、fixture 管理及测试执行 |
| uiautomator2 | 连接 Android 设备并进行 UI 操作 |
| ADB | 设备识别、Shell 命令和设备信息查询 |
| allure-pytest / Allure CLI | 记录测试步骤、附件并生成测试报告 |

目前已编写的场景包括：

- 通话：拨号、接听、挂断、视频通话及通话状态查询。
- 短信：编辑、选择发送 SIM 卡、发送与辅助机接收检查。
- 双卡设置：首选通话卡切换、默认数据卡（DDS）切换。
- 系统设置：SIM 卡 PIN 锁定、网络类型读取及 4G/5G 相关页面操作。

部分用例仍包含注释掉的步骤，或只有操作、打印而没有有效断言，不能仅凭用例名称判断其覆盖完整性。

## 2. 项目结构

```text
app_ui_dmoe-master/
├── common/                     公共基础层
│   ├── __init__.py
│   ├── base_page.py             定位解析、等待、点击、输入、滑动与截图
│   ├── driver_util.py           设备连接、ADB Shell 与屏幕尺寸查询
│   ├── log_util.py              控制台和文件日志
│   └── init.py                  当前为空
├── page/                       页面对象层
│   ├── __init__.py
│   ├── call_page.py             通话页面与通话状态查询
│   ├── sms_page.py              短信页面与内容检查
│   └── settinng_page.py         系统设置页面（当前文件名保留现有拼写）
├── testcases/                  测试用例层
│   ├── test_call.py             通话相关用例
│   ├── test_sms.py              短信收发用例
│   ├── test_PIN1.py             SIM 卡 PIN 相关用例
│   ├── test_4_5G_switch.py      网络类型相关用例
│   ├── test_switch_call_sim.py  首选通话卡切换用例
│   └── test_switch_dds.py       默认数据卡切换用例
├── tests/
│   ├── test_device_connection.py 设备连接与失败截图的离线测试
│   ├── test_waiting.py         元素等待、状态轮询及页面行为的离线测试
│   └── test_shell.py           Shell 异常与输出解析的离线测试
├── data/
│   ├── __init__.py
│   └── data.json               设备与业务数据
├── conftest.py                 全局 fixture、命令行参数与测试报告钩子
├── pytest.ini                 用例发现规则及 Allure 结果输出配置
├── requirements.txt           依赖清单，当前为空，待补齐
└── README.md
```

`.idea`、`.pytest_cache`、`__pycache__` 等目录不属于业务分层。当前还存在 `log`、`testcases\logs`、`testcases\allure-results` 等目录，日志与报告路径尚未统一。

## 3. 分层与执行流程

```text
pytest 发现并执行用例
        ↓
conftest.py 读取配置、按用例需求连接设备
        ↓
testcases 组织业务步骤并进行断言
        ↓
page 封装页面元素与业务操作
        ↓
BasePage / DriverUtil 提供 UI 操作与设备能力
        ↓
uiautomator2 / ADB 操作 Android 设备
```

各层职责：

- **公共层 `common`**：提供跨页面复用的定位、等待、截图、设备和日志能力。
- **页面层 `page`**：维护页面元素和操作方法，不承担完整测试流程。
- **用例层 `testcases`**：组合业务步骤，明确前置条件、预期结果和清理动作。
- **数据层 `data`**：提供设备及业务数据；目前多个数据 fixture 均读取同一个 `data.json`。
- **执行入口 `conftest.py`**：提供共享 fixture 和 pytest 钩子。

### 设备对象约定

优先使用三个独立的 session 级 fixture，按用例入参连接设备，同一 session 内复用设备对象：

| fixture | 设备角色 | 配置字段 |
|---|---|---|
| `main_driver` | 主测机 | `DUT_SN`，可用 `--serial` 覆盖 |
| `sup_driver` | 第一台辅助机 | `SUP_SN` |
| `sup2_driver` | 第二台辅助机 | `SUP2_SN` |

```python
# from page.call_page import CallPage
# 
# def test_single_device(main_driver):
#     main_page = CallPage(main_driver)
#
# def test_two_devices(main_driver, sup_driver):
#     main_page = CallPage(main_driver)
#     sup_page = CallPage(sup_driver)
#
# def test_three_devices(main_driver, sup_driver, sup2_driver):
#     main_page = CallPage(main_driver)
#     sup_page = CallPage(sup_driver)
#     sup2_page = CallPage(sup2_driver)
```

页面对象始终接收单个设备。未申请的设备不会连接；申请了设备但对应序列号缺失或为空，会在 setup 阶段明确报错，连接异常也会直接传播，不会返回 `None` 后继续操作。序列号统一去除首尾空白，已配置序列号不能重复。配置文件读取与校验不要求设备在线；未申请设备即使不在线，也不会触发连接。

现有业务用例已迁移到独立设备 fixture。单机用例只申请 `main_driver`，通话和短信双机场景申请 `main_driver`、`sup_driver`，尚未新增三机业务流程。

保留原来的 `driver` 作为兼容入口：

```python
# def test_legacy(driver):
#     main_driver, sup_driver, sup2_driver = driver
```

兼容入口会连接主机及所有已配置的辅助机，固定返回三个位置；未配置的辅助机对应位置为 `None`。新用例建议使用独立 fixture，避免连接不需要的设备。

设备对象由 fixture 持有，`DriverUtil` 不再保存单一全局设备。session 结束后清空设备注册表；这不是 ADB 断连，也不会停止全部应用。通话挂断、应用状态和 SIM 设置恢复应由具体场景设计，当前尚未统一实现。

### 元素定位约定

`BasePage` 使用字符串定位，键和值之间使用冒号：

```python
"resourceId:com.android.dialer:id/incall_end_call"
"text:确定"
"textContains:移动网络"
"description:接听"
"xpath://*[@content-desc='接听']"
```

普通选择器支持使用逗号组合多个条件：

```python
"resourceId:android:id/button1,text:确定"
```

当前解析方式会按逗号拆分普通选择器，因此值本身包含逗号时需要另外处理；XPath 表达式走独立分支。

### 等待与异常约定

| 接口 | 成功结果 | 超时或异常 |
|---|---|---|
| `is_element_exist(selector, timeout=3)` | 返回 `True` | 正常未出现返回 `False`；定位错误、设备异常直接传播 |
| `wait_element(selector, timeout=10)` | 返回原生 UI 对象或具体 XPath 元素 | 未出现抛出 `WaitTimeoutError`，它是 `TimeoutError` 的子类 |
| `wait_element_gone(selector, timeout=10)` | 元素消失后结束 | 未消失抛出 `WaitTimeoutError` |
| `wait_until(read, predicate, description, timeout=10, interval=0.2)` | 返回满足条件的实际读取结果 | 超时包含设备、目标和最后结果；读取异常直接传播 |
| `scroll_to_element(selector, max_swipes=5, timeout=1)` | 返回找到的元素 | 先查找再向上滑动，达到次数限制仍未找到则报错；`timeout` 是每次查找时限 |

`timeout=0` 表示立即检查一次，不使用底层默认等待。点击、输入和取文本复用等待得到的对象，不重新开启一轮默认等待；点击或输入执行失败不会自动重试，避免重复拨号、发送短信或输入 PIN。输入日志不记录输入内容。

原生定位和 XPath 都使用框架轮询；XPath 等待成功后直接操作具体匹配元素。轮询时限不是底层通信的强制中断：单次 UI RPC 仍受库本身的通信超时限制，Shell 命令默认使用独立的 10 秒超时。

页面跳转后由下一步元素等待保证同步，不再普遍使用固定休眠。打开拨号、短信和设置应用会等待对应关键元素；滑动查找有最大次数。通话用例原有接听前 `wait_seconds` 停留保持不变，之后接听操作仍会等待来电按钮出现。

业务状态接口：

- `CallPage.wait_call_state(sim_slot, expected, timeout=30)`：等待空闲 `0`、响铃 `1` 或通话中 `2`。通话用例接听后等待双方进入通话状态；挂断后等待两张 SIM 均空闲，找不到按钮但确认均空闲时才允许直接结束。
- `SettingPage.wait_sim_network_type(sim, expected, timeout=30)`：等待当前网络制式 `5G_NR` 或 `LTE`，不用于证明首选网络配置是否生效。
- `SmsPage.check_sms_content(target_text, timeout=30)`：等待短信内容匹配，未匹配返回 `False` 并记录警告；用例负责断言，通信异常不会转成 `False`。
- `SettingPage.check_pin_status(sim)`：等待 PIN 输入框消失，再读取 SIM 锁定开关的 `checked` 状态；不再通过点击“更改 PIN”或输入框是否出现来推断是否启用，也不会自动重试 PIN 输入。
- `SettingPage.check_dds_status(sim)`：读取并返回指定 SIM 的数据状态文本；具体业务预期仍需由用例断言。

`DriverUtil.adb_shell()` 和 `device_shell()` 均检查命令退出码，不将执行失败当作正常输出。屏幕尺寸输出无法解析时明确报错；网络制式查询失败直接报错，正常但未识别的制式保留为 `Unknown` 并记录警告。

## 4. 环境准备

以下命令以 Windows PowerShell 为例，建议始终在项目根目录执行。

### 4.1 创建 Python 虚拟环境

```powershell
Set-Location 'D:\Script\stress\app_ui_dmoe-master'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

若当前 PowerShell 策略不允许激活，可直接使用虚拟环境的解释器执行命令，无需修改系统策略：

```powershell
.\.venv\Scripts\python.exe -m pip --version
```

### 4.2 安装 Python 依赖

`requirements.txt` 当前为空，尚不能用它完整复现开发环境。根据现有代码，主要直接依赖可先安装：

```powershell
python -m pip install pytest uiautomator2 allure-pytest
```

以上命令未锁定版本，不代表已验证的兼容组合。后续应将实际验证过的依赖及版本补充到 `requirements.txt`。

### 4.3 准备 ADB 和测试设备

安装 Android SDK Platform-Tools，并确保 `adb` 已加入 PATH：

```powershell
adb version
adb devices -l
```

测试设备需要：

- 开启开发者选项与 USB 调试，并授权当前电脑。
- 在 `adb devices -l` 中显示为 `device`，而非 `unauthorized` 或 `offline`。
- 按业务需要准备主测机、辅助机及可用 SIM 卡。
- 保持设备解锁，并满足对应场景的权限、网络、SIM 卡及应用状态要求。

当前定位依赖 `com.android.dialer`、`com.android.messaging`、`com.android.settings` 等包名、中文文本及部分位置索引 XPath。不同系统版本、厂商界面、语言或应用版本可能需要适配。

### 4.4 安装 Allure CLI

`allure-pytest` 用于生成原始结果；查看 HTML 报告还需要单独安装 Allure CLI，并按所选版本要求准备运行环境。

```powershell
allure --version
```

## 5. 测试数据配置

配置文件为项目根目录下的 `data\data.json`，由 `conftest.py` 按绝对路径读取。

以下仅列出当前已读取代码中涉及的字段，不是对现有配置文件完整内容的描述：

| 字段 | 当前用途 |
|---|---|
| `DUT_SN` | 主测设备序列号，申请主测机时必须提供，可用 `--serial` 覆盖 |
| `SUP_SN` | 第一台辅助设备序列号，申请 `sup_driver` 时必须提供 |
| `SUP2_SN` | 第二台辅助设备序列号，申请 `sup2_driver` 时必须提供 |
| `SUP_sim1.receiver` | 通话与短信测试使用的目标号码 |
| `SUP_sim1.wait_seconds` | 通话用例中的等待时长 |
| `PIN1` | PIN 测试输入的数据 |

注意事项：

- 设备序列号以 `adb devices -l` 的实际输出为准。
- 用例中的目标号码、发送 SIM 卡和辅助机接收 SIM 卡应与实际设备配置对应。
- `--serial` 仅覆盖主测机序列号，优先级高于 `DUT_SN`；辅助机仍使用 JSON 配置。
- 序列号字段必须是字符串；未使用的设备可缺省或设为空字符串，不能使用 `null`。
- 同一 session 内配置只读取一次，`call_data`、`sms_data`、`pin1_data` 共享该配置，使用时不要修改原始数据。
- 不要将真实电话号码、设备标识及 PIN 等配置发布到公开仓库。

## 6. 执行测试

**以下命令会操作真实设备。** 通话和短信可能产生费用，双卡、网络和 PIN 操作会改变设备状态。执行前请确认测试目标及恢复方式，不建议在日常使用的设备上直接运行整个测试目录。

尤其是 PIN 场景：应确认当前 PIN 正确并了解剩余尝试次数，避免错误输入导致 SIM 卡锁定。

在项目根目录执行单个测试文件：

```powershell
python -m pytest testcases\test_sms.py -v
```

执行单个测试函数：

```powershell
python -m pytest testcases\test_call.py::test_make_call -v
```

通过命令行指定主测机，替换配置中的 `DUT_SN`：

```powershell
python -m pytest testcases\test_call.py::test_check_call_state --serial YOUR_MAIN_SERIAL -v
```

完成问题修复和运行条件确认后，再按需执行整个测试目录：

```powershell
python -m pytest testcases -v
```

当前 `pytest.ini` 配置为：

```ini
[pytest]
testpaths = testcases
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --alluredir=allure-results
```

由于存在下文列出的已知问题，上述执行命令不代表对应测试目前必定能够通过。

设备连接、等待、截图和 Shell 逻辑另有使用模拟设备的离线测试，不执行真实连接。可隔离业务目录的 fixture 配置运行：

```powershell
python -m pytest --confcutdir=tests -o addopts= tests -q
```

## 7. 日志与测试报告

### 日志

`common\log_util.py` 将日志同时输出到控制台和当前工作目录下的 `logs` 文件夹，文件名包含启动时间。

日志路径当前不是相对于项目根目录固定解析，因此从不同目录运行时，可能生成不同位置的日志。建议统一从项目根目录启动。

### Allure 报告

默认原始结果目录为启动目录下的 `allure-results`。测试结束后可查看：

```powershell
allure serve .\allure-results
```

也可以生成静态报告：

```powershell
allure generate .\allure-results -o .\allure-report --clean
allure open .\allure-report
```

原始结果目录可能保留历史执行结果，生成报告前应确认结果范围。用例执行阶段失败时，截图钩子只采集当前用例使用的已初始化设备，附件名包含 main、sup 或 sup2 角色；不会为了截图额外连接设备，也不会采集仅被前序用例使用的设备。兼容入口 `driver` 会采集该入口使用的全部设备。单台设备截图失败会记录异常并继续采集其他设备。设备初始化等 setup 阶段失败时不采集截图。

## 8. 已知问题与待完善项

以下问题来自当前代码阅读，尚未通过真机执行逐项验证。

| 问题 | 当前表现与影响 | 建议处理方向 |
|---|---|---|
| 业务状态恢复不完整 | session 结束会清空设备注册表，但不会自动挂断通话或恢复 SIM、网络、PIN 等设置 | 为具体场景设计失败与正常结束时的恢复流程 |
| 断言闭环仍待补全 | 短信接收和 PIN 启用已有断言，但 DDS 等场景尚未断言业务预期 | 对业务预期增加明确断言，避免业务失败但用例通过 |
| 通话状态解析依赖设备格式 | 状态解析依赖恰好两条 SIM 记录及其顺序 | 明确支持的设备输出格式并补充针对性校验 |
| 页面方法存在悬空引用 | `click_Hotspot()`、`click_changePIN1()` 引用的属性未定义 | 按实际页面整理定位和方法 |
| 状态验证语义需明确 | `gsm.network.type` 查询结果不等同于用户配置的首选网络类型，不能单独证明设置切换成功 | 分别定义配置状态、实际网络状态及验证方式 |
| 用例前置条件与隔离不足 | 部分导航步骤被注释，且使用 session 级设备，容易依赖前序用例留下的页面和状态 | 为每个场景明确准备、执行、断言和恢复步骤 |
| 定位仍依赖目标设备 | 存在位置索引 XPath，应用启动关键元素也依赖当前界面布局 | 按实际设备验证定位，优先使用稳定标识 |
| 配置与环境尚未收敛 | 依赖文件为空、输出目录未统一 | 补齐经验证的依赖，固定日志和报告路径 |

设备接口与等待、异常契约已统一，后续建议优先顺序：**真机页面适配与业务断言 → 状态恢复与用例隔离 → 失败现场完善 → 配置与依赖完善 → 扩展业务场景。**

## 9. 后续开发约定

- 沿用现有 POM 分层，优先完善公共能力，不在用例中重复实现底层操作。
- 页面对象接收单个设备；多机流程由用例明确协调。
- 页面层返回可用于判断的状态或数据，用例层负责对预期进行断言。
- 将条件等待与业务停留时间区分开，避免仅靠固定休眠判断操作完成。
- 新增用例时同步考虑前置条件、失败现场以及设备状态恢复。
- 新增能力应同步更新经验证的依赖、配置说明及对应文档。

## 10. 参考资料

- [uiautomator2 项目与使用说明](https://github.com/openatx/uiautomator2)
- [pytest 官方文档](https://docs.pytest.org/)
- [Allure 官方文档](https://allurereport.org/docs/)
- [UIAuto2 UI 查看工具](https://uiauto2.devsleep.com/)
