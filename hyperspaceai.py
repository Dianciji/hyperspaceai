#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import sys
import shutil
import select

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_command(command, shell=True):
    """执行命令并返回输出和状态码"""
    try:
        result = subprocess.run(command, shell=shell, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def check_ipv6():
    """检查 IPv6 是否开启"""
    print("第一步: 检查 IPv6 是否开启...")
    stdout, stderr, code = run_command("cat /proc/sys/net/ipv6/conf/all/disable_ipv6")
    
    if code != 0:
        print("无法检查 IPv6 状态，错误信息:", stderr)
        return False
    
    if stdout.strip() == "0":
        print("IPv6 已开启，继续下一步...")
        return True
    else:
        print("IPv6 未开启，正在自动配置...")
        
        # 自动修改 sysctl.conf 文件
        config_lines = [
            "net.ipv6.conf.default.disable_ipv6=0",
            "net.ipv6.conf.all.disable_ipv6=0"
        ]
        
        try:
            # 使用 echo 命令添加配置
            for line in config_lines:
                run_command(f'echo "{line}" | sudo tee -a /etc/sysctl.conf')
            
            # 应用新配置
            run_command("sudo sysctl -p")
            
            # 再次检查 IPv6 状态
            stdout, stderr, code = run_command("cat /proc/sys/net/ipv6/conf/all/disable_ipv6")
            if stdout.strip() == "0":
                print("IPv6 已成功开启，继续下一步...")
                return True
            else:
                print("IPv6 启用失败，请检查系统配置。")
                return False
                
        except Exception as e:
            print(f"配置 IPv6 时发生错误: {e}")
            return False

def update_packages():
    """更新软件包"""
    print("\n第二步: 更新软件包...")
    stdout, stderr, code = run_command("sudo apt update")
    if code == 0:
        print("软件包更新成功！")
        return True
    else:
        print("软件包更新失败，错误信息:", stderr)
        return False

def install_screen():
    """安装 screen"""
    print("\n第三步: 安装 screen...")
    stdout, stderr, code = run_command("sudo apt install -y screen")
    if code == 0:
        print("screen 安装成功！")
        return True
    else:
        print("screen 安装失败，错误信息:", stderr)
        return False

def install_hyperspace():
    """安装 hyperspace"""
    print("\n第四步: 安装 hyperspace...")
    
    try:
        # 使用os.system直接执行命令，这样输出会直接显示在控制台
        return_code = os.system("curl https://download.hyper.space/api/install | bash")
        
        if return_code == 0:
            print("hyperspace 安装成功！")
            return True
        else:
            print("hyperspace 安装失败，返回码:", return_code)
            return False
    except Exception as e:
        print(f"安装 hyperspace 时发生错误: {e}")
        return False


def source_bashrc():
    """执行 source /root/.bashrc"""
    print("\n第五步: 加载环境变量...")
    print("如果没有手动执行source /root/.bashrc 请按两次CTRL+c 退出程序。")
    print("手动执行之后请重新运行脚本。")
    print("如果已执行请等待15秒自动进入下一步。")
    # 设置15秒计时
    start_time = time.time()
    while time.time() - start_time < 15:
        try:
            remaining = int(15 - (time.time() - start_time))
            print(f"\r剩余时间: {remaining:2d} 秒", end="", flush=True)
            # 使用select模块检查标准输入是否有数据可读
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:  # 如果有输入
                choice = input(" 输入1手动更新: ")
                if choice == "1":
                    print("\n请手动执行以下命令：")
                    print("source /root/.bashrc")
                    print("然后重新运行脚本")
                    sys.exit(0)
        except:
            pass  # 忽略输入异常
        time.sleep(0.1)
    
    print("\n15秒计时结束，自动继续...")
    return True


def start_screen_session():
    """启动 screen 会话"""
    print("\n第六步: 启动 screen 会话...")
    
    # 检查并清理现有的 hyperspace 会话
    print("检查并清理现有 'hyperspace' 会话...")
    stdout, stderr, code = run_command("screen -ls | grep hyperspace")
    
    if stdout:
        print("发现现有 hyperspace 会话，正在清理...")
        # 先分离所有 Attached 会话
        run_command("screen -ls | grep 'hyperspace' | grep 'Attached' | awk '{print $1}' | xargs -I{} screen -S {} -d")
        # 再终止所有 hyperspace 会话
        run_command("screen -ls | grep 'hyperspace' | awk '{print $1}' | xargs -I{} screen -S {} -X quit")
    else:
        print("未发现现有 hyperspace 会话")
    
    # 启动新的 screen 会话（后台运行）
    stdout, stderr, code = run_command("screen -S hyperspace -d -m")
    
    if code == 0:
        print("screen 会话已在后台启动！")
        return True
    else:
        print("screen 会话启动失败，错误信息:", stderr)
        return False

def start_aios_cli():
    """启动 aios-cli"""
    print("\n第七步: 启动 aios-cli...")
    
    # 检查 aios-cli 是否已安装

    # 在 screen 会话中执行 aios-cli start
    stdout, stderr, code = run_command("screen -S hyperspace -X stuff 'aios-cli start\n'")
    
    if code == 0:
        print("aios-cli start 命令已发送到 screen 会话")
        print("等待 aios-cli 启动（5秒）...")
        time.sleep(5)
        
        # 检查 aios-cli 是否成功启动
        stdout, stderr, code = run_command("screen -S hyperspace -X hardcopy -h /tmp/screenlog")
        if code == 0:
            stdout, stderr, code = run_command("cat /tmp/screenlog")
            if "Checked for auto-update" in stdout or "already running" in stdout:
                print("aios-cli 启动成功！")
                return True
        
        # 如果无法自动检测，询问用户
        success = input("无法自动确认 aios-cli 是否启动成功，请手动确认 (y/n): ").lower() == 'y'
        if success:
            print("aios-cli 启动成功！")
            return True
        else:
            print("aios-cli 启动失败！")
            return False
    else:
        print("向 screen 会话发送命令失败，错误信息:", stderr)
        return False

def download_model():
    """下载模型"""
    print("\n第八步: 下载模型...")
    print("正在下载模型，请稍候...")
    
    try:
        # 使用正确的 aios-cli 路径
        return_code = os.system("/root/.aios/aios-cli models add hf:TheBloke/phi-2-GGUF:phi-2.Q4_K_M.gguf")
        
        if return_code == 0:
            print("模型下载成功！")
            return True
        else:
            print("模型下载失败，返回码:", return_code)
            # 提示用户手动下载
            print("\n请尝试手动执行以下命令下载模型:")
            print("/root/.aios/aios-cli models add hf:TheBloke/phi-2-GGUF:phi-2.Q4_K_M.gguf")
            success = input("模型是否已成功下载? (y/n): ").lower() == 'y'
            return success
    except Exception as e:
        print(f"下载模型时发生错误: {e}")
        return False
    
def hive_login():
    """登录 hive"""
    print("\n第十步: 登录 hive...")
    stdout, stderr, code = run_command("aios-cli hive login")
    if code == 0 and "successful" in stdout.lower():
        print("hive 登录成功！")
        return True
    else:
        print("hive 登录失败，错误信息:", stderr)
        print("输出:", stdout)
        return False

def hive_connect():
    """连接 hive"""
    print("\n第十一步: 连接 hive...")
    stdout, stderr, code = run_command("aios-cli hive connect")
    if code == 0 and "successful" in stdout.lower():
        print("hive 连接成功！")
        return True
    else:
        print("hive 连接失败，错误信息:", stderr)
        print("输出:", stdout)
        return False

def select_tier():
    """选择 tier"""
    print("\n第十二步: 自动选择 tier...")
    stdout, stderr, code = run_command("aios-cli hive select-tier 5")
    if code == 0 and "successful" in stdout.lower():
        print("tier 自动选择成功！")
        return True
    else:
        print("tier 选择失败，错误信息:", stderr)
        print("输出:", stdout)
        return False

def deploy_node():
    """一键部署节点"""
    clear_screen()
    print("===== 一键部署节点 =====")
    
    steps = [
        check_ipv6,
        update_packages,
        install_screen,
        install_hyperspace,
        source_bashrc,
        start_screen_session,
        start_aios_cli,
        download_model,
        hive_login,
        hive_connect,
        select_tier
    ]
    
    for i, step_func in enumerate(steps):
        success = step_func()
        if not success:
            print(f"\n第 {i+1} 步失败，部署中断！")
            input("按回车键返回主菜单...")
            return
    
    print("\n第十三步: 部署完成！")
    print("恭喜！节点部署成功！")
    
    # 执行 aios-cli hive whoami 并显示输出
    print("\n正在获取节点密钥信息...")
    stdout, stderr, code = run_command("aios-cli hive whoami")
    if code == 0:
        print("\n密钥信息:")
        print(stdout)
    else:
        print("获取节点密钥失败，错误信息:", stderr)
    
    input("按回车键返回主菜单...")

def check_points():
    """查看积分"""
    clear_screen()
    print("===== 查看积分 =====")
    stdout, stderr, code = run_command("aios-cli hive points")
    if code == 0:
        print("\n积分信息:")
        print(stdout)
    else:
        print("获取积分失败，错误信息:", stderr)
    
    input("按回车键返回主菜单...")

def check_logs():
    """查看最新日志"""
    clear_screen()
    print("===== 查看最新日志 =====")
    
    # 获取日志目录中的所有文件
    stdout, stderr, code = run_command("ls -t ~/.cache/hyperspace/kernel-logs")
    
    if code != 0:
        print("无法获取日志文件列表，错误信息:", stderr)
        input("按回车键返回主菜单...")
        return
    
    # 获取最新的日志文件
    log_files = stdout.strip().split('\n')
    if not log_files or log_files[0] == '':
        print("未找到日志文件")
        input("按回车键返回主菜单...")
        return
    
    latest_log = log_files[0]
    print(f"正在显示最新日志文件: {latest_log}")
    
    # 显示最新日志文件的内容
    stdout, stderr, code = run_command(f"cat ~/.cache/hyperspace/kernel-logs/{latest_log}")
    
    if code == 0:
        print("\n日志内容:")
        print(stdout)
    else:
        print("无法读取日志文件，错误信息:", stderr)
    
    input("按回车键返回主菜单...")


def monitor_node():
    """监控节点"""
    clear_screen()
    print("===== 节点监控中 =====")
    print("每半小时检查一次积分，如果3小时内积分未变化将自动重启节点")
    
    points_history = []  # 存储最近6次的积分记录
    
    try:
        while True:
            # 获取当前积分
            stdout, stderr, code = run_command("aios-cli hive points")
            if code == 0:
                # 提取Points值
                for line in stdout.split('\n'):
                    if "Points:" in line:
                        current_points = line.split(':')[1].strip()
                        points_history.append(current_points)
                        print(f"\n当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"当前积分: {current_points}")
                        
                        # 保持最近6次记录（3小时）
                        if len(points_history) > 6:
                            points_history.pop(0)
                        
                        # 检查是否3小时内积分未变化
                        if len(points_history) == 6 and len(set(points_history)) == 1:
                            print("\n警告：积分3小时未变化，正在重启节点...")
                            
                            # 执行kill命令
                            run_command("aios-cli kill")
                            print("节点已停止")
                            
                            # 按顺序执行恢复步骤
                            steps = [
                                (start_aios_cli, "启动节点"),
                                (hive_login, "登录hive"),
                                (hive_connect, "连接hive"),
                                (select_tier, "选择tier")
                            ]
                            
                            for step_func, step_name in steps:
                                print(f"\n正在{step_name}...")
                                success = step_func()
                                if not success:
                                    print(f"{step_name}失败，将在下次检查时重试")
                                    break
                            else:
                                print("\n恢复节点运行成功！")
                            
                            # 清空历史记录
                            points_history.clear()
            else:
                print(f"\n获取积分失败: {stderr}")
            
            # 等待30分钟
            time.sleep(1800)
            
    except KeyboardInterrupt:
        print("\n监控已停止")
        input("按回车键返回主菜单...")

def check_whoami():
    """查看密钥信息"""
    clear_screen()
    print("===== 查看密钥信息 =====")
    stdout, stderr, code = run_command("/root/.aios/aios-cli hive whoami")
    if code == 0:
        print("\n密钥信息:")
        print(stdout)
    else:
        print("获取密钥信息失败，错误信息:", stderr)
        print("输出:", stdout)
    
    input("按回车键返回主菜单...")

def main_menu():
    """主菜单"""
    while True:
        clear_screen()
        print("===== HyperSpace 节点部署工具 =====")
        print("===== 作者：马走日 =====")
        print("===== 故障反馈或者实时更新请关注X:@erlili359891 ===== ")
        print("=======================================================")
        print("1. 一键部署节点")
        print("2. 查看积分")
        print("3. 查看最新日志")
        print("4. 监控节点")
        print("5. 查看密钥信息")
        print("0. 退出")
        
        choice = input("\n请选择操作 [0-5]: ")
        
        if choice == "1":
            deploy_node()
        elif choice == "2":
            check_points()
        elif choice == "3":
            check_logs()
        elif choice == "4":
            monitor_node()
        elif choice == "5":
            check_whoami()
        elif choice == "0":
            print("感谢使用，再见！")
            sys.exit(0)
        else:
            print("无效选择，请重试！")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
