#!/usr/bin/env python3

import subprocess
import sys
import os
import glob


def run_command(command):
    """执行系统命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print(f"成功: {result.stdout}")
            return True
        else:
            print(f"失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"异常: {str(e)}")
        return False
def save_to_pem(content, filename="my.pem"):
    """将用户输入的字符串保存为 my.pem 文件"""
    try:
        with open(filename, "w") as f:
            f.write(content)
        print(f"已保存为 {filename}")
        if os.path.exists(filename):
            print(f"文件路径: {os.path.abspath(filename)}")
        else:
            print("保存失败，未知错误")
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")


def view_latest_log(log_dir="~/.cache/hyperspace/kernel-logs"):
    """查看最近的日志文件"""
    # 解析用户主目录
    log_dir = os.path.expanduser(log_dir)

    # 检查目录是否存在
    if not os.path.exists(log_dir):
        print(f"错误：目录 {log_dir} 不存在！")
        return

    # 获取目录中的所有文件
    try:
        files = [f for f in glob.glob(os.path.join(log_dir, "*")) if os.path.isfile(f)]
        if not files:
            print(f"目录 {log_dir} 中没有日志文件！")
            return

        # 找到最近修改的文件
        latest_file = max(files, key=os.path.getmtime)
        latest_time = os.path.getmtime(latest_file)
        from datetime import datetime
        print(f"\n最近的日志文件: {os.path.basename(latest_file)}")
        print(f"最后修改时间: {datetime.fromtimestamp(latest_time).strftime('%Y-%m-%d %H:%M:%S')}")

        # 查看文件内容
        print(f"\n文件内容 ({latest_file}):")
        run_command(f"cat {latest_file}")

    except Exception as e:
        print(f"查询最近日志时出错: {str(e)}")


def check_and_enable_ipv6():
    """检查 IPv6 是否开启，未开启则启用并验证"""
    # 检查 IPv6 状态
    success, output = run_command("sysctl net.ipv6.conf.all.disable_ipv6")
    if not success:
        print("错误：无法检查 IPv6 状态，可能系统不支持 IPv6")
        return

    # 判断是否禁用
    ipv6_disabled = "net.ipv6.conf.all.disable_ipv6 = 1" in output
    if not ipv6_disabled:
        print("IPv6 已开启，检查可用性...")
        success, addr_output = run_command("ip -6 addr")
        if "inet6" in addr_output:
            print("IPv6 已启用并有地址分配")
        else:
            print("IPv6 已启用但无地址，可能网络未配置")
        return

    print("IPv6 当前被禁用，正在启用...")

    # 临时启用 IPv6
    if run_command("sysctl -w net.ipv6.conf.all.disable_ipv6=0")[0]:
        print("IPv6 已临时启用")
    else:
        print("临时启用 IPv6 失败，请检查权限或系统配置")
        return

    # 永久启用 IPv6（修改 sysctl.conf）
    try:
        with open("/etc/sysctl.conf", "r") as f:
            lines = f.readlines()

        disable_line = "net.ipv6.conf.all.disable_ipv6"
        updated = False
        for i, line in enumerate(lines):
            if disable_line in line:
                lines[i] = "net.ipv6.conf.all.disable_ipv6 = 0\n"
                updated = True
                break

        if not updated:
            lines.append("\n# Enable IPv6\n")
            lines.append("net.ipv6.conf.all.disable_ipv6 = 0\n")

        with open("/etc/sysctl.conf", "w") as f:
            f.writelines(lines)

        if run_command("sysctl -p")[0]:
            print("IPv6 已永久启用，重启后生效")
        else:
            print("应用 sysctl 配置失败")

    except Exception as e:
        print(f"修改 IPv6 配置时出错: {str(e)}")
        return

    # 验证 IPv6 是否生效
    print("验证 IPv6 是否可用...")
    success, addr_output = run_command("ip -6 addr")
    if success and "inet6" in addr_output:
        print("IPv6 已启用并有地址分配")
    else:
        print("IPv6 已启用但无地址，可能网络未配置 IPv6 支持")
        # 可选：尝试触发网络重新配置
        run_command("service networking restart || systemctl restart networking")




def menu():
    """显示菜单选项"""
    print("\n=== 脚本菜单 ===")
    print("1. 一键部署节点 ")
    print("2. 查看运行日志")
    print("3. 查看积分")
    print("4. 检测并启用 ipv6")
    print("5. 退出脚本")
    print("=====================")


def main():
    while True:
        # 显示菜单
        menu()

        # 获取用户输入
        choice = input("请输入选项 (1-5): ").strip()

        # 根据输入执行操作
        if choice == "1":
            print("正在更新软件包...")
            run_command("sudo apt update")
            print("正在安装 screen...")
            run_command("sudo apt install -y screen")
            print("正在下载并安装 hyperspace...")
            run_command("curl https://download.hyper.space/api/install | bash")
            print("正在刷新 bashrc...")
            # source 需要在 bash 中执行
            run_command("bash -c 'source /root/.bashrc && echo bashrc refreshed'")
            print("正在创建hyper会话...")
            run_command("screen -S hyperspace")
            print("正在更新软件包...")
            run_command("sudo apt update")
            print("正在启动aios-cli...")
            run_command("aios-cli start")
            print("正在启动 screen 会话并分离...")
            # 用 -d -m 启动一个分离的 screen 会话，并在其中跑一个命令
            run_command("screen -d -m bash -c 'echo Running in screen; sleep 1000'")
            print("Screen 会话已启动并分离，可用 'screen -r' 重新连接")

            print("正在安装模型...")
            run_command("aios-cli models add hf:TheBloke/phi-2-GGUF:phi-2.Q4_K_M.gguf")

            print("请粘贴你的秘钥：")
            content = input().strip()
            # 检查长度是否为44位
            if len(content) == 44:
                save_to_pem(content, "my.pem")
            else:
                print(f"错误：输入长度为 {len(content)} 位，必须是 44 位！")

            print("正在导入秘钥...")
            run_command("aios-cli hive import-keys ./my.pem")

            print("正在设置此会话...")
            run_command("aios-cli hive login")

            print("正在确认模型是否注册...")
            run_command("aios-cli hive connect")

            print("正在自动分配等级...")
            run_command("aios-cli hive select-tier 5")

            print("节点已部署成功...")




        elif choice == "2":
            print("正在查询最近日志...")
            view_latest_log()



        elif choice == "3":
            print("正在查询积分...")
            run_command("aios-cli hive points")



        elif choice == "4":
            print("正在检查ipv6是否正常...")
            check_and_enable_ipv6()


        elif choice == "5":
            print("退出脚本， bye!")
            sys.exit(0)

        else:
            print("无效选项，请输入 1-5 之间的数字！")

        # 询问是否继续
        cont = input("\n继续操作？(y/n): ").lower()
        if cont != "y":
            print("退出脚本， bye!")
            break


if __name__ == "__main__":
    print("欢迎使用hyperspaceai一键部署脚本！-by 马走日")
    print("X链接：https://x.com/erlili359891?t=ePrUNye3t75fBsTvO7QRVQ&s=09")
    print("注意！！请先检查ipv6是否启用")
    main()