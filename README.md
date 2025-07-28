## 📱 抖音美女识别自动滑动工具

利用 Python + ADB + 百度人脸识别接口，自动刷抖音视频，识别是否为美女（女性且颜值高），自动点赞、分享、滑动下一条。

---

### 🧠 灵感来源

本项目灵感来自知乎专栏文章：

> [用Python实现自动刷抖音并识别美女](https://zhuanlan.zhihu.com/p/357624649)
> 作者展示了结合 ADB + 百度AI 接口实现刷视频并识别颜值的思路。

在此基础上进行了封装与增强，支持跳过直播、支持环境变量保护密钥等功能。

---

### 📦 功能概览

* ✅ 启动抖音
* ✅ 自动截图
* ✅ 百度 AI 识别美女（性别 + 颜值）
* ✅ 双击点赞 + 分享给好友
* ✅ 自动跳过直播
* ✅ 自定义视频数量和颜值评分阈值

---

### 🛠 项目结构

```
your_project/
├── main.py            # 用于刷抖音的主程序
├── .env               # 环境变量（存放 API 密钥，⚠️ 不可上传）
├── templates/         # 存放直播识别模板图像
└── README.md          # 项目说明
```

---

### ✅ 环境准备

1. **Python 版本**：推荐 Python 3.8+
2. **依赖安装**：

```bash
pip install -r requirements.txt
```

如果没有 `requirements.txt`，可手动安装：

```bash
pip install opencv-python requests python-dotenv
```

3. **ADB 环境**

* 安装并配置好 adb 工具
* 手机开启「USB调试模式」并连接电脑
* 需要启用「USB调试（安全设置）」不然不能模拟点击

---

### 🔐 配置密钥（非常重要）

创建 `.env` 文件：

```env
BAIDU_API_KEY=你的APIKey
BAIDU_SECRET_KEY=你的SecretKey
```

获取地址：[百度人脸识别开放平台](https://console.bce.baidu.com/ai/#/ai/face/app/list)

---

### 🖼️ 准备模板图（直播识别）

将直播画面的截图保存为模板图，放入 `templates/` 文件夹中。程序会自动匹配跳过直播视频。

---

### 🚀 如何运行

```bash
python main.py
```

程序将：

* 启动抖音
* 自动截图识别
* 点赞、分享美女视频
* 跳过直播
* 连续处理多条视频

---

### ⚙️ 自定义参数

```python
NUM_VIDEO = 10  # 要刷的视频条数
SCORE = 70  # 美女颜值评分阈值
```

---

### 🧷 安全提醒

* 请勿将 `.env` 文件上传至公开平台
* 项目仅供学习研究，不可用于任何违反法律或平台规则的用途

---

### 🙋‍♀️ 联系与贡献

欢迎提交 Issue 或 PR 提出建议与改进。

---
