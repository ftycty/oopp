class Forum:
    def __init__(self, title, content, type):
        self.__title = title
        self.__content = content
        self.__type = type

#setter
    def set_title(self, title):
        self.__title = title

    def set_content(self, content):
        self.__content = content

    def set_type(self, type):
        self.__type = type

#getter
    def get_title(self):
        return self.__title

    def get_content(self):
        return self.__content

    def get_type(self):
        return self.__type