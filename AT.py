import json
import subprocess
import sys
import time
import serial

PORT = "COM47"
BAUDRATE = 115200
RESPONSE_TIMEOUT = 10
CONFIG_FILE = "commands_config.json"

def load_command_config(file_path):
    """加载命令配置文件"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def execute_adb_commands(commands):
    """执行 ADB 命令"""
    for cmd in commands:
        print(f"执行 ADB 命令: {cmd}")
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ADB 命令失败: {cmd}\n错误: {result.stderr}", file=sys.stderr)
            return False
        if "am start" in cmd:  # Example for `at+chup` prerequisites
            time.sleep(10)
        elif "setprop" in cmd:
            time.sleep(8)
    return True

def send_command(port, command):
    """发送 AT 命令并接收响应"""
    print(f"发送：{command!r}")
    port.write(command + b"\r\n")
    port.flush()

    deadline = time.monotonic() + RESPONSE_TIMEOUT
    pending = bytearray()
    responses = []

    while time.monotonic() < deadline:
        pending.extend(port.read(port.in_waiting or 1))

        while b"\n" in pending:
            raw_line, _, remainder = pending.partition(b"\n")
            pending = bytearray(remainder)
            line = raw_line.decode("ascii", errors="backslashreplace").strip()
            if line:
                print(f"接收：{line}")
                responses.append(line)

            if line in {"OK", "ERROR"} or line.startswith(("+CME ERROR", "+CMS ERROR")):
                return responses

    print(f"等待响应超时，未完成行：{bytes(pending)!r}", file=sys.stderr)
    return responses

def main():
    config = load_command_config(CONFIG_FILE)
    try:
        with serial.Serial(
            port=PORT,
            baudrate=BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.2,
            write_timeout=2,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        ) as port:
            print(f"已打开 {PORT}，波特率 {BAUDRATE}")

            for item in config["commands"]:
                prerequisites = item.get("prerequisites", [])
                if prerequisites and not execute_adb_commands(prerequisites):
                    print(f"跳过命令 {item['at_command']}，因为前置 ADB 命令失败。", file=sys.stderr)
                    continue

                responses = send_command(port, item["at_command"].encode("ascii"))
                print(f"命令 {item['at_command']!r} 的响应：{responses}")

                # 增加指令间的间隔时间
                time.sleep(5)

    except (serial.SerialException, OSError) as exc:
        print(f"串口操作失败：{exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())