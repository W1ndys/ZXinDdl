import requests
import json
from get_token import get_token  # 导入get_token函数


def fetch_course_data(token):
    try:
        api_url = "https://v2.api.z-xin.net/stu/course/getJoinedCourse2"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        }
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


def process_course_data(course_data):
    if course_data:
        # 把数据直接保存到文件
        with open("course_data.json", "w", encoding="utf-8") as file:
            json.dump(course_data, file, ensure_ascii=False, indent=4)
        print("[+]读取数据成功，数据已保存到 course_data.json 文件中")

        if course_data["msg"] == "成功":
            print("[+]数据获取成功")
            print("[+]即将开始解析数据")
            data = ""
            # 解析数据
            for course in course_data["data"]:
                for homework in course["homework"]:
                    data += f"课程名称: {course['course']['name']}\n"
                    data += f"课程老师: {course['teacher']['user']['nickname']}\n"
                    data += f"作业标题: {homework['title']}\n"
                    data += f"作业类型: {homework['category']}\n"
                    data += f"开始时间: {homework['starttime']}\n"
                    data += f"截止时间: {homework['endtime']}\n"
                    if homework["studenthomework"]:
                        data += f"作答次数: {homework['studenthomework'][0]['answerProgress']}\n"
                        data += f"正确次数: {homework['studenthomework'][0]['correctProgress']}\n"
                        data += f"最终得分: {homework['studenthomework'][0]['finalScore']} (若已提交显示0分可能是教师未评分)\n"
                        data += f"最后作答时间: {homework['studenthomework'][0]['lastAnswerTime']}\n"
                    else:
                        data += "暂未作答，无相关数据\n"
                    data += "----------------------------------------------------------------\n"

            with open("course_data.txt", "w", encoding="utf-8") as file:
                file.write(data)
            print("[+]课程数据解析完成，结果已保存到 course_data.txt 文件中")
            print("[+]课程数据程序运行结束")
            print("--------------------------------")
            print("Power by W1ndys")
            print("https://github.com/W1ndys")
        else:
            print("[-]课程数据获取失败")


def read_config():
    # 从配置文件中读取账号和密码
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        username = config["username"]
        password = config["password"]
        print("--------------------------------")
        print("[+]读取账号密码成功")
        print("[+]账号：" + username)
        print("[+]密码：" + password)
        return username, password


if __name__ == "__main__":
    username, password = read_config()
    token = get_token(username, password)
    if token:
        course_data = fetch_course_data(token)
        process_course_data(course_data)
    else:
        print("[-]获取token失败")
