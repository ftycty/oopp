class User:
    def __init__(self,name,nric,email,password,homephone,mobilephone,address,postalcode,newsletter):
        self.__name = name
        self.__nric = nric
        self.__email = email
        self.__password = password
        self.__homephone = homephone
        self.__mobilephone = mobilephone
        self.__address = address
        self.__postalcode = postalcode
        self.__newsletter = newsletter

    #getters
    def get_name(self):
        return self.__name
    def get_nric(self):
        return self.__nric
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def get_homephone(self):
        return self.__homephone
    def get_mobilephone(self):
        return self.__mobilephone
    def get_address(self):
        return self.__address
    def get_postalcode(self):
        return self.__postalcode
    def get_newsletter(self):
        return self.__newsletter

    #setters
    def set_name(self,name):
        self.__name = name
    def set_nric(self,nric):
        self.__nric = nric
    def set_email(self,email):
        self.__email = email
    def set_password(self,password):
        self.__password = password
    def set_homephone(self,homephone):
        self.__homephone = homephone
    def set_mobilephone(self,mobilephone):
        self.__mobilephone = mobilephone
    def set_address(self,address):
        self.__address = address
    def set_postalcode(self,postalcode):
        self.__postalcode = postalcode
    def set_newsletter(self,newsletter):
        self.__newsletter = newsletter
