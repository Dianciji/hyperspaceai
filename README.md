# HyperSpace节点部署工具使用指南

## 功能介绍

这是一个用于自动部署和管理HyperSpace节点的工具，主要功能包括：

1. **一键部署节点** - 自动完成从IPv6配置到节点启动的全部步骤
2. **查看积分** - 显示当前节点的积分情况
3. **查看最新日志** - 查看节点运行的最新日志文件
4. **监控节点** - 自动监控节点状态，当积分长时间不变时自动重启节点

## 运行环境要求

- Linux系统（Ubuntu/Debian等）
- Python 3
- 需要有root权限
- 稳定的网络连接

## 基础运行步骤

### 1. 下载脚本

打开终端，输入以下命令下载脚本：

```bash
wget https://github.com/Dianciji/hyperspaceai.git
```

> 注意：请将"你的用户名"替换为实际的GitHub用户名

### 2. 添加执行权限

```bash
chmod +x hyai.py
```

### 3. 运行脚本

```bash
./hyai.py
```

或者

```bash
python3 hyai.py
```

### 4. 使用菜单选项

运行脚本后，会显示以下菜单：

```
===== HyperSpace 节点部署工具 =====
1. 一键部署节点
2. 查看积分
3. 查看最新日志
4. 监控节点
0. 退出

请选择操作 [0-4]:
```

- 输入 `1` 进行一键部署节点
- 输入 `2` 查看当前积分
- 输入 `3` 查看最新日志
- 输入 `4` 启动节点监控
- 输入 `0` 退出程序

## 详细功能说明

### 一键部署节点

选择此选项后，脚本会自动执行以下步骤：

1. 检查并配置IPv6
2. 更新系统软件包
3. 安装screen工具
4. 安装hyperspace
5. 加载环境变量
6. 启动screen会话
7. 启动aios-cli
8. 下载必要的模型
9. 登录hive
10. 连接hive
11. 选择tier
12. 显示节点密钥信息

整个过程全自动完成，无需手动干预。

### 查看积分

显示当前节点的积分情况，包括总积分和详细信息。

### 查看最新日志

自动查找并显示最新的日志文件内容，帮助排查问题。

### 监控节点

启动后会每30分钟检查一次积分，如果发现3小时内积分没有变化，会自动执行以下操作：

1. 停止节点
2. 重新启动节点
3. 登录hive
4. 连接hive
5. 选择tier

监控会持续运行，直到按下Ctrl+C手动停止。

## 常见问题

### 如何确认节点是否正常运行？

可以通过"查看积分"选项查看积分是否在增加，或通过"查看最新日志"检查日志中是否有错误信息。

### 如何在后台运行监控？

可以使用nohup命令在后台运行：

```bash
nohup python3 hyai.py &
```

然后选择选项4启动监控。

### 如果部署过程中断怎么办？

重新运行脚本，选择"一键部署节点"选项重新开始部署。

## 注意事项

- 请确保使用root用户或有sudo权限的用户运行脚本
- 部署过程中请保持网络连接稳定
- 监控功能需要持续运行，建议在服务器上使用screen或nohup等工具在后台运行

---

如有任何问题或建议，请在GitHub仓库提交issue或联系开发者。
