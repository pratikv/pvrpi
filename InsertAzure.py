

from azure.storage import *
table_service = TableService(account_name='https://tempraturemonitoringservice', account_key='EtvjLIeYlvVKUKTqalwRgzuEUgpFMd58')

temp = {'deviceid': '1', 'temprature': '37', 'createdAt' : '2014-09-17 17:15:54.467'}
table_service.insert_entity('temprature', temp)


