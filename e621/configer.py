class configer:  # 这一个用来读取配置文件的类
    _configure = ''
    tags_file = {}

    def __init__(self, configure_file):  # 初始化方法接受一个配置文件的地址用来打开它
        current = ""
        lines = open(configure_file).readlines()  # 读取所有的行存储到lines变量中

        for line in lines:  # 循环每一行

            if line.startswith('#') or line.startswith('\n'):  # 去除注释
                continue

            if line.find('#') != -1:  # 去除行内注释
                line = line[0:line.find('#') - 1]
            line = line.strip()  # 去除空白字符

            if line.startswith('[') and line.endswith(']'):
                current = line[1:-1]
                self.tags_file[current] = []
                continue
            self.tags_file[current].append(line)

    def __getitem__(self, key):
        return self.tags_file[key]
