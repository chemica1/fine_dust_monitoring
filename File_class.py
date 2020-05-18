import os


class File_class:
    dir_path = os.getcwd()

    def __init__(self, file='', index = 0):
        self.file = file
        self.index = index
        self.list = []
        self.file_to_list()

    def file_to_list(self):
        tempList = []
        with open(f'{self.dir_path}\\txt\\{self.file}.txt', 'r', encoding='UTF8') as fp:
            while (1):
                line = fp.readline()
                try:
                    escape = line.index('\n')
                except:
                    escape = len(line)
                if line:
                    tempList.append(line[0:escape])
                else:
                    break

        self.list = tempList

    def call_the_list(self):
        return self.list

    def save_the_list(self, index, newInfo):
        self.list[index] = newInfo
        with open(f'{self.dir_path}\\txt\\{self.file}.txt', 'w', encoding='UTF8') as fp:
            for i in self.list:
                data = i
                fp.write(data + '\n')

    def read_the_list(self):
        with open(f'{self.dir_path}\\txt\\{self.file}.txt', 'r', encoding='UTF8') as fp:
            temp = fp.read()
        return temp