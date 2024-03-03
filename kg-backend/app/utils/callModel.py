# 在文献上传的时候，调用模型
# 把 content 先转化为 txt，便于调用模型，直接保存在模型的输入目录下
import json
import subprocess
from datetime import datetime

import paramiko

from app.models import Log

# 指定模型输入的文件的路径，也是上传文献后输出 txt 的路径
input_path = "app/utils/testData/1.txt"
# 将输入文件上传到服务器的路径
txt1_path = "/user_data/xuduo/zyt/RL_QG/datasets-squa/test/1.txt"
# 问答对：服务器
pred_path_remote = "/user_data/xuduo/zyt/RL_QG/results/s_base/predictions_list.json"
# 问答对：下载到本地
pred_path = "app/utils/testData/predictions_list.json"

# 获取图谱的三个文件，远程位置
graph_path_remote = '/user_data/xuduo/zyt/RL_QG/src/onqg/KGUpdate/data/DB300K/neo4j/graph.json'
graph_path_entity_map_remote = '/user_data/xuduo/zyt/RL_QG/src/onqg/KGUpdate/data/DB300K/entityId_map.txt'
graph_path_relation_map_remote = '/user_data/xuduo/zyt/RL_QG/src/onqg/KGUpdate/data/DB300K/relationId_map' \
                                 '.txt'

# 获取图谱的三个文件，保存的位置
graph_path = 'app/utils/testData/graph.json'
graph_path_entity_map = 'app/utils/testData/entityId_map.txt'
graph_path_relation_map = 'app/utils/testData/relationId_map.txt'


def call_model(content):
    # 提示语
    print("模型正在运行中……")
    # 把前端传来的文献内容保存为 txt，方便执行脚本
    save_string_to_txt(content, input_path)
    # 因为 Linux 和 Windows 文本换行格式不一样导致兼容性问题，需要处理一下
    with open(input_path, 'r', newline='\r\n', encoding='utf-8') as file:
        content = file.read()

    # 转换换行符为LF
    content = content.replace('\r\n', '\n')

    # 写入Linux文本文件
    with open(input_path, 'w', newline='\n', encoding='utf-8') as file:
        file.write(content)

    # 将这个文件上传到服务器
    print("文件上传到服务器")
    hostname = '218.199.69.22'
    port = 22
    username = 'xuduo'
    password = 'xuduo123456'

    # 创建SSH客户端对象
    client = paramiko.SSHClient()
    client.load_system_host_keys()  # 加载系统Host密钥
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH主机密钥
    client.connect(hostname, port, username, password)

    # 创建SFTP客户端对象
    sftp = client.open_sftp()
    try:
        # 把输入数据放到服务器
        sftp.put(input_path, txt1_path)

        print("调用服务器模型")
        line = sshclient_execmd(hostname, port, username, password, "sh /user_data/xuduo/zyt/shixun_0706/model.sh")
        # 脚本执行输出：
        print("脚本执行输出")
        for line_ in line:
            print(line_)

        # 日志功能有待完善（日志功能是老师最后又提出的新需求，实在不想写了）

        print("脚本执行后输出最后一行：")
        print(line[-1])

        string = line[-1]
        numbers = string.split()

        # 新增的点和边的数量
        number1 = 0
        number2 = 0

        # 确保字符串中有两个数字
        if len(numbers) == 2:
            # 提取两个数字并转换为整数类型
            number1 = int(numbers[0])
            number2 = int(numbers[1])

            print("Number 1:", number1)
            print("Number 2:", number2)
        else:
            print("Invalid input: String does not contain two numbers.")

        import json
        import re

        with open(pred_path, 'r', encoding='utf-8') as json_file:
            array_a = json.loads(json_file.read())

        # 从服务器获取模型解析好之后生成的几个文件
        sftp.get(graph_path_remote, graph_path)
        sftp.get(graph_path_relation_map_remote, graph_path_relation_map)
        sftp.get(graph_path_entity_map_remote, graph_path_entity_map)
        sftp.get(pred_path_remote, pred_path)

        with open(pred_path, 'r', encoding='utf-8') as json_file:
            array_b = json.loads(json_file.read())

        # 新增的问答对数量
        qa_count = 0
        for element in array_b:
            if element not in array_a:
                qa_count += 1

        # 读取 JSON 文件
        with open(pred_path, 'r', encoding='utf-8') as json_file:
            json_list = json_file.read()

        # 将日志存入数据库（暂时没有考虑模型调用失败的情况）
        log = Log(log_info="模型调用成功", update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), vertices_count=number1,
                        edges_count=number2, qa_count=qa_count)
        log.save()

        # 使用正则表达式提取问题和答案（处理问答对文件）
        pattern = r'^(.*?)\? (.*)$'
        qa_list = []

        for line in json.loads(json_list):
            match = re.match(pattern, line)
            if match:
                question = match.group(1).strip()
                answer = match.group(2).strip()
                qa_dict = {
                    'question': question + ' ?',
                    'answer': answer
                }
                qa_list.append(qa_dict)
    finally:
        # 关闭SFTP和SSH连接
        sftp.close()
        client.close()
        print("模型调用结束")

    return qa_list


# 将字符串保存到 txt 文件
def save_string_to_txt(string, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(string)


'''示例用法
my_string = "这是一个示例字符串。"
file_path = "example.txt"
save_string_to_txt(my_string, file_path)'''


# 执行 Shell 脚本
def run_shell_script(script_path):
    try:
        # 执行 Shell 脚本，并捕获输出内容
        result = subprocess.run(script_path, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr

        # 将输出保存为 txt 文件
        output_file = "script_output.txt"
        with open(output_file, "w") as f:
            f.write(output)

        print(f"脚本执行完成，输出已保存到 {output_file}")

    except Exception as e:
        print("出现错误:", e)


# 读取 txt 格式文件
def read_txt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: An error occurred while reading the file - {e}")
        return None


# 读取 JSON 格式文件
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Unable to decode JSON data in file '{file_path}' - {e}")
        return None
    except Exception as e:
        print(f"Error: An error occurred while reading the file - {e}")
        return None


def sshclient_execmd(hostname, port, username, password, execmd):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command(execmd)

    line = stdout.readlines()
    print(stderr.read())
    s.close()
    return line
