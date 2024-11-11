import requests
import json
import base64


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


def user_pass_base64(username, password):
    # 要编码的数据，通常是二进制格式
    username_to_encode = username.encode("utf-8")
    password_to_encode = password.encode("utf-8")

    # 使用base64.b64encode()函数进行编码
    encoded_data_username = base64.b64encode(username_to_encode)
    encoded_data_password = base64.b64encode(password_to_encode)

    # 编码后的结果是bytes类型，可以转换为str类型以便打印或存储
    base64_username = encoded_data_username.decode("utf-8")
    base64_password = encoded_data_password.decode("utf-8")

    return base64_username, base64_password


def get_token(username, password):
    try:
        url = "https://v2.api.z-xin.net/auth/login"
        base64_username, base64_password = user_pass_base64(username, password)

        data = {"username": str(base64_username), "password": str(base64_password)}

        response = requests.post(url, data=data).json()
        code = response["code"]
        msg = response["msg"]
        if code == 2000:
            print("登录成功")
            token = response["data"]["token"]
            print(f"token: {token}")
            return token
        else:
            print("登录失败")
            print(f"错误信息: {msg}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}，请检查网络连接")
        return None
    except KeyError as e:
        print(f"响应中缺少预期的键: {e}，请检查账号密码是否正确")
        return None


def process_course_data(course_data):
    if course_data:
        # 保存到文件
        with open("course_data.json", "w", encoding="utf-8") as file:
            json.dump(course_data, file, ensure_ascii=False, indent=4)
        print("[+]数据已保存到 course_data.json 文件中")

        if course_data["msg"] == "成功":
            print("[+]数据获取成功")
            print("[+]即将开始解析数据")
            data = ""
            # 解析数据
            for course in course_data["data"]:
                for homework in course["homework"]:
                    print(f"课程名称: {course['course']['name']}")
                    data += f"课程名称: {course['course']['name']}\n"
                    print(f"课程老师: {course['teacher']['user']['nickname']}")
                    data += f"课程老师: {course['teacher']['user']['nickname']}\n"
                    print(f"作业标题: {homework['title']}")
                    data += f"作业标题: {homework['title']}\n"
                    print(f"作业类型: {homework['category']}")
                    data += f"作业类型: {homework['category']}\n"
                    print(f"开始时间: {homework['starttime']}")
                    data += f"开始时间: {homework['starttime']}\n"
                    print(f"截止时间: {homework['endtime']}")
                    data += f"截止时间: {homework['endtime']}\n"
                    if homework["studenthomework"]:
                        print(
                            f"作答次数: {homework['studenthomework'][0]['answerProgress']}"
                        )
                        data += f"作答次数: {homework['studenthomework'][0]['answerProgress']}\n"
                        print(
                            f"正确次数: {homework['studenthomework'][0]['correctProgress']}"
                        )
                        data += f"正确次数: {homework['studenthomework'][0]['correctProgress']}\n"
                        print(
                            f"最终得分: {homework['studenthomework'][0]['finalScore']} (若已提交显示0分可能是教师未评分)"
                        )
                        data += f"最终得分: {homework['studenthomework'][0]['finalScore']} (若已提交显示0分可能是教师未评分)\n"
                        print(
                            f"最后作答时间: {homework['studenthomework'][0]['lastAnswerTime']}"
                        )
                        data += f"最后作答时间: {homework['studenthomework'][0]['lastAnswerTime']}\n"
                    else:
                        print("暂未作答，无相关数据")
                    print(
                        "----------------------------------------------------------------"
                    )
                    data += "----------------------------------------------------------------\n"
            with open("result.txt", "w", encoding="utf-8") as file:
                file.write(data)
            print("[+]数据解析完成，结果已保存到 result.txt 文件中")
            print("[+]程序运行结束")
            print("--------------------------------")
            print("Power by W1ndys")
            print("https://github.com/W1ndys")
        else:
            print("[-]数据获取失败")


token = get_token("xxxx", "xxxx")
course_data = fetch_course_data(token)
process_course_data(course_data)
