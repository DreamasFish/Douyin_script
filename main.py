from dotenv import load_dotenv
import subprocess
import time
import random
import base64
import requests
import cv2
import os

# 加载 .env 文件
load_dotenv()

# 一些参数
API_KEY = os.getenv("BAIDU_API_KEY")
SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")
SCORE = 70
NUM_VIDEO = 100


# --- ADB 工具 ---
def adb_shell(cmd):
    subprocess.run(f"adb shell {cmd}", shell=True)


def adb_pull(remote_path, local_path):
    subprocess.run(f"adb pull {remote_path} {local_path}", shell=True)


def launch_douyin():
    print("🚀 启动抖音...")
    adb_shell("am start -n com.ss.android.ugc.aweme/.main.MainActivity")
    time.sleep(5)


def capture_screen(filename="screen.png"):
    adb_shell("screencap -p /sdcard/screen.png")
    adb_pull("/sdcard/screen.png", filename)
    print("📸 已截图")


# --- 简单滑动 ---
def swipe_up():
    x1 = random.randint(400, 600)
    x2 = random.randint(600, 700)
    y1 = random.randint(1400, 1600)
    y2 = random.randint(700, 1000)
    duration = random.randint(150, 200)
    adb_shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")
    print(f"➡️ 简单滑动：({x1}, {y1}) → ({x2}, {y2})")


# --- 百度人脸识别 ---
def get_baidu_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    res = requests.post(url, data=params)
    data = res.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        print("❌ 获取token失败：", data)
        return None


def is_beautiful_baidu(image_path, token, score_threshold=SCORE):
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode()
    url = f"https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token={token}"
    headers = {"Content-Type": "application/json"}
    data = {
        "image": img_base64,
        "image_type": "BASE64",
        "face_field": "gender,beauty",
        "max_face_num": 1
    }
    response = requests.post(url, headers=headers, json=data)
    res = response.json()
    if res.get("error_code") == 0:
        face = res['result']['face_list'][0]
        gender = face['gender']['type']
        beauty = face['beauty']
        print(f"识别：性别={gender}, 颜值={beauty:.1f}")
        return gender == 'female' and beauty >= score_threshold
    else:
        print("❌ 识别失败：", res.get("error_msg"))
        return False


def double_tap(x=None, y=None):
    """
    模拟双击屏幕，默认在中间
    """
    if x is None or y is None:
        x, y = 600, 1400  # 默认屏幕中下部（可调整）

    print(f"💗 模拟双击 ({x}, {y}) 点赞")
    adb_shell(f"input tap {x} {y}")
    time.sleep(0.1)
    adb_shell(f"input tap {x} {y}")


def share_to_friend():
    # 点击分享按钮
    x_share, y_share = 1006, 1942
    print(f"🔗 点击分享按钮 ({x_share}, {y_share})")
    adb_shell(f"input tap {x_share} {y_share}")
    time.sleep(1)  # 等待分享界面打开

    # 点击发送给好友按钮
    x_send, y_send = 115, 1892
    print(f"🧑‍🤝‍🧑 选择好友 ({x_send}, {y_send})")
    adb_shell(f"input tap {x_send} {y_send}")

    # 点击发送
    x_send, y_send = 811, 2279
    print(f"📤 发送 ({x_send}, {y_send})")
    adb_shell(f"input tap {x_send} {y_send}")


def is_live_stream_image(screen_path="screen.png", template_dir="templates", threshold=0.7):
    img = cv2.imread(screen_path)
    if img is None:
        print("❌ 屏幕图读取失败")
        return False

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 遍历多张模板图
    for template_file in os.listdir(template_dir):
        template_path = os.path.join(template_dir, template_file)
        template = cv2.imread(template_path, 0)
        if template is None:
            continue

        # 模糊匹配（可选）
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
        template_blur = cv2.GaussianBlur(template, (3, 3), 0)

        result = cv2.matchTemplate(img_blur, template_blur, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        print(f"模板 [{template_file}] 匹配得分：{max_val:.3f}")
        if max_val > threshold:
            return True

    return False


# --- 主逻辑 ---
def run_loop(total=30):
    token = get_baidu_token()
    if not token:
        print("❌ 无法继续：token 获取失败")
        return

    for i in range(total):
        print(f"\n========== 第 {i + 1} 条视频 ==========")
        time.sleep(2)
        capture_screen()

        # 先用图像判断直播
        if is_live_stream_image("screen.png"):
            print("🎥 是直播，跳过滑动下一条")
            swipe_up()
            continue

        if is_beautiful_baidu("screen.png", token):
            print("✅ 是美女，停留观看")
            time.sleep(3 + random.uniform(1, 3))
            double_tap()
            share_to_friend()
            swipe_up()
        else:
            print("❌ 非美女，滑动下一条")
            swipe_up()


# --- 启动 ---
if __name__ == "__main__":
    launch_douyin()
    run_loop(NUM_VIDEO)
