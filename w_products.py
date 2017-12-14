class Products:
    def __init__(self,name,price,offer,link,image):
        self.__name = name
        self.__price = price
        self.__offer = offer
        self.__link = link
        self.__image = image

    def get_name(self):
        return self.__name
    def get_price(self):
        return self.__price
    def get_offer(self):
        return self.__offer
    def get_link(self):
        return self.__link
    def get_image(self):
        return self.__image

    def set_name(self,name):
        self.__name = name
    def set_price(self,price):
        self.__price = price
    def set_offer(self,offer):
        self.__offer = offer
    def set_link(self,link):
        self.__link = link
    def set_image(self,image):
        self.__image = image
