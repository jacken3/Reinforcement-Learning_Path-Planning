import configparser

class Config:
    def __init__(self):
        self.file="envconfig_1.ini"
        self.con=configparser.ConfigParser()
        self.filename=self.con.read(self.file,encoding='utf-8')
        self.obs=dict(self.con.items("Obs")) #得到section名为Obs的键值对信息
        self.range=dict(self.con.items("Range")) 
    

    







