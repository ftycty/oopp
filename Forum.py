class Forum:
    def __init__(self, title, content, type):
        self.__title = title
        self.__content = content
        self.__type = type

#getter
    def get_title(self):
        return self.__title

    def get_content(self):
        return self.__content

    def get_type(self):
        return self.__type
