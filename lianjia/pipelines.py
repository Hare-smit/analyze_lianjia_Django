# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import LianjiaItem
from warehouse import models
from visual import visual_main,data_up

import pymysql

class LianjiaPipeline(object):
    tt = [] #装载每次插入的数据
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="hanhua./",
                                    database="lianjia", charset='utf8')
        self.cursor = self.conn.cursor()    #定义游标

    def open_spider(self, spider):
        self.cursor.execute("truncate table warehouse_housing_update;")  #清空数据库
        self.conn.commit()  #执行

    def close_spider(self, spider):
        print("closing spider,last commit", len(self.tt))
        self.bulk_insert_to_mysql(self.tt,"warehouse_housing_update")
        self.conn.commit()
        #查看获取爬去数据是否足够
        len_s = models.Housing_update.objects.count()
        #
        # def select(sql):  # 获取函数，不用此方法游标缘故获取内容会有问题
        #     self.cursor.execute(sql)
        #     relist = self.cursor.fetchall()
        #     return relist
        # sql1 = "select * from warehouse_housing_update;"
        # relist1 = select(sql1)  # 获取到内容
        time.sleep(1)
        if len_s>1000:
            print("符合标准")
            time.sleep(1)
            data_up.update_datebases()

        #
        #     self.cursor.execute("truncate table warehouse_housing;")  # 清空数据库
        #     self.conn.commit()
        #     self.bulk_insert_to_mysql(relist1,"warehouse_housing")
        #     #print("爬取入库完成")
        # self.cursor.close()
        # self.conn.close()
        time.sleep(1)
        visual_main.make_main()
        print("html更新完成")





    #插入函数
    def bulk_insert_to_mysql(self, list,db):   #插入函数
        try:
            print("the length of the data-------", len(self.tt))
            sql = f"insert into {db}(area,title,community,position,tag,re_price,unit_price,housetype,housesize,direction,fitment,plce,master_map) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            self.cursor.executemany(sql, list)  #插入数据   插入多用executemany，少用exectue
            self.conn.commit()
        except:
            self.conn.rollback()



    def process_item(self, item, spider):
        print(item)
        area = item["area"]
        title = item["title"]
        community = item["community"]
        position = item["position"]
        tag = item["tag"]
        re_price = round(float(item['re_price']),2)

        unit = item["unit_price"]
        units = unit.replace(",","")[:-3]
        unit_price = round(float(units),2)

        housetype = item["housetype"]
        housesize = round(float(item["housesize"]),2)
        direction = item["direction"]
        fitment = item["fitment"]
        plce = item["plce"]
        master_map = item["master_map"]

        self.tt.append((area,title,community,position,tag,re_price,unit_price,housetype,housesize,direction,fitment,plce,master_map))
        if len(self.tt) == 500:
            self.bulk_insert_to_mysql(self.tt,"warehouse_housing_update")
            # 清空缓冲区
            del self.tt[:]
        # sql = "insert into taobao(title,price,place,sell,store) values (%s,%s,%s,%s,%s)"
        # self.curser.executemany(sql,self.tt)
        return item









    #
    # def process_item(self, item, spider):
    #     print('打开了数据库')
    #     print(item)
    #     # item.save()
    #     print('关闭了数据库')
    #     return item
