import yaml, os


class Get_Data:

    def __init__(self):
        pass

    def get_yaml_data(self, file_name):
        # 返回读取yaml文件全部数据
        with open("./Data" + os.sep + file_name,"r", encoding="utf-8") as f:
            return yaml.load(f)
