# state = 0
# if state == 0:
#         a = "Anh/Chị có đơn cần phê duyệt! (vui lòng truy cập vào web):"
# elif state == 1:
#         a = "Đơn đã được phê duyệt! (vui lòng truy cập vào web)"
# html = f"""\
#     <html>
#     <body>
#         <p>Hi,<br>
#         {a}</p>
#         <p><a href="http://hrm-dor.tbslogistics.com.vn/">link web nghỉ phép.</a></p>
#         <p> Feel free to <strong>let us</strong> know what content would be useful for you!</p>
#     </body>
#     </html>
#     """
# print(html)
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#isalnum : kiểm tra xem ký tự có phải là chử cái hay số không
#unicodedata.category(c) == 'Zs' : kiểm tra có khoảng trắng hay không
#unicodedata.category(c) == 'Ll' : chữ cái viết thường
#unicodedata.category(c) == 'Lu' : chữ cái viết hoa
#unicodedata.category(c) == 'Lt' : chữ cái viết hoa nhưng không phải ký tự chữ
#unicodedata.category(c) == 'Lo' : Các ký tự thuộc loại này bao gồm các chữ cái trong các bảng mã khác nhau như Latin, Cyrillic, Greek, Hangul, Hiragana, Katakana và các ký tự chữ cái trong các ngôn ngữ khác như tiếng Trung, tiếng Ả Rập, tiếng Hebrew, tiếng Hindi, tiếng Thái, tiếng Hàn Quốc, tiếng Nhật và nhiều ngôn ngữ khác nữa.
#unicodedata.category(c) == 'Pd' : ký tự dấu gạch ngang
# import unicodedata

# string = '   ctk5-bdcs    '
# is_alpha_numeric = all(c.isalnum() 
#                        or unicodedata.category(c) == 'Zs' 
#                        or unicodedata.category(c) == 'Ll' 
#                        or unicodedata.category(c) == 'Lu' 
#                        or unicodedata.category(c) == 'Lt' 
#                        or unicodedata.category(c) == 'Pd'  
#                        for c in string)

# if is_alpha_numeric:
#     remove_blank = string.strip(' ') # remove khoảng trống (đầu-cuối) của chuỗi
#     blank_index = remove_blank.find(" ") # tình vị trí khoảng trống (nằm ở vị trí thứ mấy)
#     hyphen_index = remove_blank.find('-') # tìm vị trí dấu gạch ngang (nằm ở vị trí thứ mấy)
#     result = ''
#     if blank_index > 0 and hyphen_index >= 0:
#         print('Tên phòng ban không được phép')
#     elif blank_index > 0:
#         split_blank = remove_blank.split(" ")
#         new_list = []
#         for index in split_blank:
#             print(index)
#             # print(split_blank[index])
#             if index != '':
#                 new_list.append(index)
#                 result += index[0].upper()
#         print(result)
#     elif hyphen_index > 0:
#         split_hyphen = remove_blank.split("-")
#         print(split_hyphen)
#         for index in split_hyphen:
#             if index != '':
#                 result += index[0].upper()
#         print(result)
                
#         print("Chuỗi này chỉ chứa các chữ cái không dấu, các chữ cái có dấu và số")
# else:
#     # return ("Tên phòng ban không được phép")
#     print("Tên phòng ban không được phép")


#-----------------------------------------------------------------------------------------------------------------------------

# remove_blank = string.strip(' ') # remove khoảng trống (đầu-cuối) của chuỗi


# blank_index = remove_blank.find(" ") # tình vị trí khoảng trống (nằm ở vị trí thứ mấy)
# hyphen_index = remove_blank.find('-') # tìm vị trí dấu gạch ngang (nằm ở vị trí thứ mấy)



# if blank_index > 0 and hyphen_index >= 0:
#     print('Tên phòng ban không được phép')
# elif blank_index > 0:
#     split_blank = remove_blank.split(" ")
#     new_list = []
#     result = ''
#     print(split_blank)
#     for index in split_blank:
#         print(index)
#         # print(split_blank[index])
#         if index != '':
#             new_list.append(index)
#             result += index[0].upper()
# elif hyphen_index > 0:
#     split_hyphen = remove_blank.split("-")
#     print(split_hyphen)
#     for i in split_hyphen:
#         if i == '':
#             print(1)

#----------------------------------------------------------------------------------------------------------------------------

# my_string = "thi văn"
# for c in my_string:
#     print(c)
# if my_string.isalnum():
#     print("Chuỗi này chỉ chứa các ký tự và số")
# else:
#     print("Chuỗi này không chỉ chứa các ký tự và số")




#------------------------------------------------------------------------------------------------------------------------------------




           


# print(result)
# print(new_list) 
    # print(f'{split_blank} & {True}')



# elif c < 1:
#     print(f'{c} & {False}')
# b = a.split(" ")

# print(b)
# print(c)
# print(d)
# print(c)
# # b = a.split("-")
# # print(b)

# mylist = ['red', 'blue', 'yellow', 'black']
# print(mylist)
# #>> ['red', 'blue', 'yellow', 'black']

# popped1 = mylist.pop(2)
# print(popped1)
# #>> yellow

# print(mylist)
#>> ['red', 'blue', 'black']


# import os
# current_directory = os.getcwd()
# print(current_directory)


# b = 'thi van nhat'
# print(len(b))
# a = range(len(b))
# for i in a:
#     print(i)

# a = 0 

# for i in range(8):
#     # print(i)
#     a += i
#     print(a)

# a = '    aa       a'
# b = a.strip()

# for i in range(len(b)):
#     if b[i] == '' and b[i-1] =='':
#         del b[i]
# print(b)

# import re

# #Replace the first two occurrences of a white-space character with the digit 9:

# txt = "The    ----rain in Spain"
# x1 = re.sub("^\s+|\s+$", "", txt)
# x = re.sub("\s+", " ", txt)

# # x2 = re.sub("")
# print(x)


# a = 72
# c = [1,2,3,4,5]
# b = a/10
# print(max(c))

# a = range(73+1,80)
# b= 79
# # for i in a:
# #     print(i)
# if b in a and (b == 76 or b == 75):
#     print(True)
# else:
#     print(False)
    

# a = 75

# max = (int(a/10)*10)+ 10
# print(max)
# a = 2
# s = f'''selete JPLevel where JPLevelID = {a}'''
# print(s)

# for i in range(6):
#     print(i)

# a = 'ádasd'
# b= '123nhat'

# c = a+','+b

# import datetime



# a = datetime.date(2023,5,17)
# b = datetime.date(2023,5,19)
# c = b-a + datetime.timedelta(days=1)
# print(c)


# p = ''
# print(p)

from datetime import datetime

# date_string = "2023-04-24 00:00:00.1234567"
# date_format = "%Y-%m-%d %H:%M:%S.%f%f"

# date = datetime.strptime(date_string, date_format)
# print(date)




# def numberDays(emplID:int,startDate:datetime.date ,endDate:datetime.date): #: datetime.date,:datetime.date
    
#     print(emplID)
  
#     # x = endDate - startDate
#     # print(x)
#     list = []
#     list.append(startDate)
#     list.append(endDate)
#     print(list)
#     print(startDate)
#     print(endDate)
#     print(type(startDate))
#     print(type(endDate))



# year = '2023'
# month = '5'
# day = '20'
# day1 = '25'

# b = numberDays(emplID='adsfgasd',startDate=datetime.date(datetime(2023,5,20)),endDate=datetime.date(datetime(2023,5,25)))#datetime.date(2023,5,25)








# date1 = datetime.date(2023, 5, 19)
# date2 = datetime.date(2023, 5, 20)

# date1 < date2  # So sánh ngày, trả về True nếu date1 < date2

# delta = date2 - date1  # Tính toán khoảng cách giữa hai ngày
# print(delta.days)  # In ra số ngày giữa hai ngày

# date_string = date1.strftime('%Y-%m-%d')  # Định dạng chuỗi ngày
# print(date_string)


# import datetime

# d = datetime.date(2022, 12, 25)
# print(d)
# a = type(d)
# if type(d) == datetime.date:
#     print(a)

# def numberDays(emplID = None,startDate = None,endDate = None ):
#     if emplID is None or startDate is None or endDate is None:
#         print('False')
#     else:
#         print('nhât')

# a = numberDays(1)
# print(a)

# from datetime import date
#-----------------------------------------------

# import datetime
# from dateutil.relativedelta import relativedelta #sử dụng để cộng tháng vào 1 ngày cho trước
# startDate = datetime.date(2023,12,10)
# endDate = datetime.date(2023,5,29)

# x = endDate-startDate
# print(x.days)
# print(type(x))

# print(startDate.day)
# print(startDate)
# is_date = isinstance(startDate, datetime.date)
# print(is_date)


# a = datetime.date.today()
# print(a.year)

# b = startDate + relativedelta(months=1)
# print(b)
# # x = b + 1
# print(x)
#-------------------------------------
# if a > startDate:
#     print('lớn hơn')
# else:
#     print('nhỏ hơn')

# g = ['sdfsd','sdfsdf','sdfsd22222','sdfsdf','sdfsd']

# for i in g:
#     print(i)
#     if i == 'sdfsd22222':
#         g.remove(i)


# print(g)
# del g[len(g)-1]
# print(g)

# a = 5

# b = a/2
# print(int(b))
#--------------------------------------------------------------------------------
# import calendar
# month = datetime.now().month
# year = datetime.now().year
# print(month)
# print(year)
# number_of_days = calendar.monthrange(year, month)[1]
# first_date = datetime(year, month, 1)

# last_date = datetime(year, month, number_of_days)
# delta = last_date - first_date

# print(type(number_of_days))



# a = calendar.monthrange(2023, 5)
# print(a[1])

#------------------------------------------------------------------------------------
import calendar
month = datetime.now().month
year = datetime.now().year
number_of_days = calendar.monthrange(year, month)[1]
# print(number_of_days)

firstDay = datetime.date(datetime(year,month,1))
# print(firstDay)



#----------------------------------------------------------------
# a = 123123123
# b = 'a09'

# c = str(a) + '-' +  b#f'{a}{b}'
# print(c)



# x = ['681102001-Việc Riêng', '621110001-Việc Riêng', '1-Việc Riêng', '621110001-Chờ Việc']
# for e in x:
#     if '621110001-Chờ Việc' == e:
#         print(True)

# i= ''
# print(i)

# a = 6
# if a in range(1,6):
#     print(True)


# x = {'a':1,'b':2,'c':3}


# if 'c' in x:
#     print(True)

# print(x.keys())

# a = '2023-05-01 00:00:00.0000000'

# append = []
# c = datetime.date(datetime.strptime(a[0:a.find(" ")],"%Y-%m-%d"))
# print(type(c))
# append.append(c)
# # print(type(a[0:a.find(" ")]))
# t = datetime.date(datetime(2023,5,1))
# print(t)
# print(append)
# if t in append:
#     print('đúng rồi')


# g = [1,2,3,4,5,6]
# y = [1,2,3]
# p = g+y
# print(p)



# a = 'chờ việc'

# b = (a[0] + a[(a.find(" ") + 1)]).upper()
# print(b)

# import pandas as pd
# o = [{'a':1,'b':2,'c':3},{'c':6,'a':4,'b':5}]

# df = pd.DataFrame(o)
# print(df)
#------------------------------------------------------------------------------------
import datetime

#công thức chuyển đổi số ngày 


#xét điều kiện ngày nhập vào >= 0.5

day = 2.5
hour = day*23.99
print(hour)
a = datetime.datetime(2023,5,25,6,30,30)
print(a.day)


# c = a + datetime.timedelta(hours=hour)# - datetime.timedelta(days=1)
# print(c)
# print(datetime.datetime.date(c))
# # datetime.datetime.date



# print(type(day)) #kiểm tra số int và float

# period = c-a
# # print(period)
# print(period.total_seconds()/86400)


b = datetime.datetime(2023,5,25)

if a>b:
    print(True)


b = '621809035'
a = (621809035,622109002,622211003,621808017)
if int(b) in a:
    print('thivannhat')




def daysInMonth(y,m):
    day_In_Month = []
    try:
        number_of_days = calendar.monthrange(y, m)[1]
        firstDay = datetime.date(datetime(y,m,1))
        print('nhat')
        for i in range(0,number_of_days):
            day = firstDay + datetime.timedelta(days=i)
            day_In_Month.append(day)
        return day_In_Month
    except:
        
        return day_In_Month



# a = datetime.datetime.strftime('2023-05-21 00:00:00',"%Y-%m-%d %H:%M:%S")
# b = datetime.datetime.strftime('2023-05-21 00:00:00',"%Y-%m-%d %H:%M:%S")
# if a > b:
#     print(True)
# else:
#     print ((False))
# 2023-05-21 00:00:00
# daysInMonth(23234,23423)
import math
a = 0.


b= math.ceil(a)
# print(b)


a = 2
b =3
if a == 2 and b ==2:
    print('nat')