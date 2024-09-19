class configer:
    _configure = ''
    config = {}

    def __init__(self, configure_file):
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
                self.config[current] = []
                continue
            self.config[current].append(line)
        print(self.config)

    def __getitem__(self, key):
        return self.config[key]
