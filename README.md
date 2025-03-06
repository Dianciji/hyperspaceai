# HyperSpace 节点部署工具使用指南（零基础版）

## 一、准备工作

1. **系统要求**：
   - Ubuntu 系统（推荐 Ubuntu 20.04 或更高版本）
   - root 权限
   - 稳定的网络连接

2. **必要工具安装**：
```bash
apt update
apt install -y git python3
```

## 二、下载脚本

1. **从 GitHub 下载脚本**：
```bash
wget https://raw.githubusercontent.com/Dianciji/hyperspaceai/main/hyperspaceai.py -O hyperspaceai.py
```

2. **进入脚本目录**：
```bash
cd 你的仓库名
```

## 三、运行脚本

1. **赋予脚本执行权限**：
```bash
chmod +x hyperspaceai.py
```

2. **执行脚本**：
```bash
python3 hyperspaceai.py
```

## 四、使用说明

### 首次使用流程

1. **选择选项 1 "一键部署节点"**
   - 脚本会自动执行 13 个步骤
   - 在第五步时请特别注意提示信息

2. **第五步特别说明**：
   - 当看到 "如果没有手动执行source /root/.bashrc" 的提示时
   - 请按两次 CTRL+C 退出程序
   - 然后执行：
     ```bash
     source /root/.bashrc
     ```
   - 再重新运行脚本：
     ```bash
     python3 hyai.py
     ```

### 日常使用功能说明

脚本主菜单提供以下功能：

1. **一键部署节点**（首次使用选择）
2. **查看积分**（查看当前节点积分）
3. **查看最新日志**（查看运行状态）
4. **监控节点**（自动监控和维护）
5. **查看密钥信息**（查看节点密钥）
0. **退出程序**

### 常见问题解决

1. **如果遇到权限问题**：
   ```bash
   sudo python3 hyai.py
   ```

2. **如果提示 "command not found"**：
   ```bash
   source /root/.bashrc
   ```
   然后重新运行脚本

3. **如果需要停止程序**：
   - 按 CTRL+C 两次

## 五、维护建议

1. **定期检查**：
   - 使用选项 2 查看积分
   - 使用选项 3 查看运行日志

2. **长期运行**：
   - 建议使用选项 4 开启节点监控
   - 可以自动处理积分不增长的情况

3. **安全建议**：
   - 使用选项 5 查看密钥信息后请妥善保管
   - 不要泄露给他人

## 六、获取帮助

如遇到问题：
- 请访问 X(Twitter): @erlili359891
- 或在 GitHub 项目页面提交 Issue

## 注意事项

1. 请确保服务器网络稳定
2. 保持系统时间准确
3. 不要随意中断程序运行
4. 定期检查节点状态
5. 妥善保管密钥信息

祝您使用愉快！如有任何问题，欢迎随时反馈。
