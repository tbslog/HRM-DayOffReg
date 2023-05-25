import os
from fastapi import Depends,HTTPException,status,File,UploadFile,Request
import numpy as np
from  projects.models import *

from pydantic import BaseModel
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
import pandas as pd
# import functions as fn
from  projects import functions as fn
from projects.security import validate_token
from  projects.setting import  app
import random
import string
from datetime import timedelta
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
# from fastapi.exceptions import RequestValidationError
import uuid
import unicodedata
import re
import calendar
# txt = "    The    rain    in     Spain    "
# x = re.sub("^\s+|\s+$", "", txt) cắt khoảng trắng đầu và đuôi
# x = re.sub("\s+", " ", txt) thay thế nhiều khoảng trắng thành 1 khoảng trắng
import requests


import tempfile
import binascii
import secrets
import asyncio
import shutil
# ------------------------------------------------------------------------------------------------------------
cn = fn.cn

app.mount("/static",StaticFiles(directory="tempDir"),name="static") #câu lệnh trả về link ảnh



# @app.post("/dangnhapUsernamePass", tags=['HRM'], dependencies=[Depends(validate_token)])
@app.post("/Login", tags=['Login'],summary='Đăng nhập') #done
def index(formdata: CheckLogin): 
    s = ''
    if formdata.username.isnumeric():
        s = f"""SELECT top 1 EmpID, Password FROM Users WHERE EmpID = '{formdata.username}'"""
    else:
        s = f"""SELECT top 1 EmpID, Password FROM Users WHERE UserName = '{formdata.username}'"""
    result = fn.get_data(s)
    if len(result) > 0:
        # -- a Thái
        if (fn.check_pw(formdata.password,result[0][1])):
            #đăng nhập thành công, có hình ảnh đại diện mặc định
            s = f'''SELECT COUNT(*) FROM dbo.Image WHERE EmpID = {result[0][0]}'''
            check = fn.get_data(s)
            if check[0][0] < 1:
                # tempDir = os.path.join('tempDir','30b39c90-f927-4154-bbe7-acd069988a54.JPG')
                tempDir = '30b39c90-f927-4154-bbe7-acd069988a54.JPG'
                s = f'''INSERT INTO dbo.Image(EmpID,ImageData)
                        VALUES({result[0][0]},N'{tempDir}')'''
                fn.commit_data(s)
            return  {'rCode': 3,
                    'rData':{'token':fn.generate_token(username=formdata.username,days=30),
                    'empid':result[0][0]},
                    'rMsg': 'Đăng nhập thành công'}
        else:
            return {'rCode': 0,'rMsg': 'Tài khoản hoặc mật khẩu không đúng'}
        # -- a Thái
    elif len(result) == 0:
        if fn.checkEmplID(formdata.username) == True:
            if formdata.autogen == 1:
                # chuoi = string.ascii_letters + string.digits
                # kq_chuoi = ''.join((random.choice(chuoi) for i in range(6)))
                passWord = fn.genPass()
                s = f'''INSERT INTO dbo.Users(UserName,EmpID,Password,UserType,Email,Status,LastModify,Modifier) 
                values ('{formdata.username}','{formdata.username}','{fn.hashpw(passWord)}',0,'{formdata.username+"@tbslogistics.com"}',0,SYSDATETIME(),0)''' 
                fn.commit_data(s)
                return {'rCode': 2,
                        'rData':{'token':fn.generate_token(username=formdata.username,days=30),'password':passWord},
                        'rMsg':'Anh/chị nhớ lưu lại password'}
            else:
                return {'rCode' : 1, 'rMsg' : "Đăng nhập không thành công, EmpID tồn tại"}
        else:
            return {'rCode': 0,'rMsg': 'Tài khoản không tồn tại'}

#đổi password
# @app.post('/changePass',tags=['Login'],summary='Thay đổi password')
async def change(form:ChangePass):
    s = ''
    a = ['Xác nhận password không đúng']
    b = ['Password mới đang rỗng']
    c = ['Password mới phải lớn hơn 5 và nhỏ hơn 10 ký tự']
    if form.username.isnumeric():
        s = f"""
                    SELECT top 1 EmpID, Password FROM Users WHERE EmpID = '{form.username}'
                """
    else:
        s = f"""
                    SELECT top 1 EmpID, Password FROM Users WHERE UserName = '{form.username}' 
                """
    result = fn.get_data(s)
    if len(result) > 0:
        # -- a Thái
        if (fn.check_pw(form.currentPassword,result[0][1])):
            if form.newPassword == form.confirmPass and form.newPassword != '' and 5 < len(form.newPassword) < 10:
                s = f"""
                    UPDATE dbo.Users SET Password = '{fn.hashpw(form.confirmPass)}'
                    WHERE EmpID = '{result[0][0]}'
                    """
                fn.commit_data(s)
                
                return {'rCode':1,'rMsg':'Thay đổi password thành công'}
            else:
                return{'rCode':0,'rError':{'Lỗi newPassWord':a + b + c}}

    return {'rCode': 0,
            'rMsg': 'tài khoản hoặc mật khẩu không đúng'
            }


#đổi password
@app.post('/changePass',tags=['Login'],summary='Thay đổi password')
async def change(form:ChangePass):
    if form.username.isnumeric():
        s = f"""SELECT top 1 EmpID, Password FROM Users WHERE EmpID = '{form.username}'"""
    else:
        s = f"""SELECT top 1 EmpID, Password FROM Users WHERE UserName = '{form.username}'"""
    result = fn.get_data(s)
    if len(result) > 0:
        if (fn.check_pw(form.currentPassword,result[0][1])):
            # if form.newPassword == form.confirmPass and form.newPassword != '' and 5 < len(form.newPassword) < 10:
            if form.newPassword == '':
                return {'rCode':0,'rError':'Password mới đang rỗng'}
            if form.newPassword != form.confirmPass:
                return {'rCode':0,'rError':'Xác nhận password không đúng'}
            if len(form.newPassword) <= 5 or len(form.newPassword) > 10:
                return {'rCode':0,'rError':'Password mới phải lớn hơn 5 và nhỏ hơn hoặc bằng 10 ký tự'}
            s = f"""
                UPDATE dbo.Users SET Password = '{fn.hashpw(form.confirmPass)}'
                WHERE EmpID = '{result[0][0]}'
                """
            fn.commit_data(s)
            return {'rCode':1,'rMsg':'Thay đổi password thành công'}
    return {'rCode': 0,'rMsg': 'tài khoản hoặc mật khẩu không đúng'}




# getEmpInfo -lấy thông tin nhân viên
@app.get('/getEmpInfo',dependencies=[Depends(validate_token)], tags=['GetEmpInfo'],summary='Lấy thông tin nhân viên')
async def getEmpInfo(empId: str = None,token: str = Depends(validate_token)): #Done
    note = {'statusCode': 0,'note': 'EmpID chưa được tạo Users'}
    note1 = {'statusCode': 0,'note':'Anh/Chị hãy nhập mã nhân viên'}
    if empId == None:
        if str(token).isnumeric(): #and len(str(EmpId)) > 0
            # if fn.checkEmplIDUser(token) == True:
                s = f"""
                        SELECT Emp.FirstName,Emp.LastName,Emp.ComeDate,Emp.ZoneID,Z.ZoneName,
                            jp.JobPosID,JPL.JPLevelID, DP.DeptID,AL.AnnualLeave,JP.Name,JPN.Name,JPL.Name,DP.Name FROM Employee AS Emp
                            LEFT JOIN dbo.Zone AS Z ON Emp.ZoneID = Z.ZoneID
                            LEFT JOIN dbo.JobPosition AS JP	ON Emp.PosID = JP.JobPosID
                            LEFT JOIN dbo.JPLevel AS JPL ON JP.JPLevel = JPL.JPLevelID
                            LEFT JOIN dbo.Department AS DP ON jp.DeptID = DP.DeptID
                            LEFT JOIN dbo.AnnualLeave AS AL ON Emp.EmpID = AL.EmpID
                            LEFT JOIN dbo.JPName AS JPN ON jp.JPName = JPN.JPNameID
                            WHERE Emp.EmpID  = '{token}'
                        """
                result = fn.get_data(s)
                df = pd.DataFrame([tuple(t) for t in result], columns=[
                                'FirstName','LastName','ComeDate','ZoneID','ZoneName','JobPosID','JPLevelID',
                                'DeptID','AnnualLeave','JobpositionName','JPName','JPLevelName','DepartmentName'])
                return {'rCode':1,
                        'rData': df.to_dict('Records')[0], #trả về dữ liệu: Dict kiểu 'Records'
                        'rMsg': 'Lấy thông tin thành công'
                        }
            #else:
                #return note
        else:
            return note1
    elif str(empId).isnumeric():
        # if str(empId).isnumeric(): #and len(str(EmpId)) > 0
        #if fn.checkEmplIDUser(empId) == True:
            s = f"""
                    SELECT Emp.FirstName,Emp.LastName,Emp.ComeDate,Emp.ZoneID,Z.ZoneName,
                        jp.JobPosID,JPL.JPLevelID, DP.DeptID,AL.AnnualLeave,JP.Name,JPN.Name,JPL.Name,DP.Name FROM Employee AS Emp

                        LEFT JOIN dbo.Zone AS Z ON Emp.ZoneID = Z.ZoneID
                        LEFT JOIN dbo.JobPosition AS JP	ON Emp.PosID = JP.JobPosID
                        LEFT JOIN dbo.JPLevel AS JPL ON JP.JPLevel = JPL.JPLevelID
                        LEFT JOIN dbo.Department AS DP ON jp.DeptID = DP.DeptID
                        LEFT JOIN dbo.AnnualLeave AS AL ON Emp.EmpID = AL.EmpID
                        LEFT JOIN dbo.JPName AS JPN ON jp.JPName = JPN.JPNameID
                        WHERE Emp.EmpID = '{empId}'
                    """
            result = fn.get_data(s)
            df = pd.DataFrame([tuple(t) for t in result], columns=[
                            'FirstName','LastName','ComeDate','ZoneID','ZoneName','JobPosID','JPLevelID',
                            'DeptID','AnnualLeave','JobpositionName','JPName','JPLevelName','DepartmentName'])
            return {'rCode':1,
                    'rData': df.to_dict('Records')[0], #trả về dữ liệu: Dict kiểu 'Records'
                    'rMsg': 'Lấy thông tin thành công'
                    }
        #else:
            #return note
        # else:
        #     return note1
    else:
        return note1
        



# lấy list typyoff
@app.get("/dayOffType", tags=['OffRegister'],summary='lấy danh sách loại phép') #dependencies=[Depends(validate_token)], 
async def getDayOffType(): #done
    s = f"""
            SELECT * FROM OffType
            """
    result = fn.get_data(s)
    
    # cursor = cn.cursor()
    # rows = cursor.execute(s).fetchall()
    df = pd.DataFrame([tuple(t) for t in result], columns=[
                      'OffTypeID', 'Name', 'Note', 'DeletedFlag'])
    # print(df)
    return {'rCode':1,
            'rData':df.to_dict('records'),
            'rMsg': 'Lấy danh sách thành công'
            }



# đăng ký nghỉ phép --- 
# @app.post("/day-off-letter", tags=['OffRegister'],dependencies=[Depends(validate_token)])
# async def offDayRegister(empID:int,type:int,reason:str,period:int,startDate:datetime.date | None = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y%m%d")):
async def offDayRegister(form: Offregister,emplid: str = Depends(validate_token)): #Done
    note = {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
    note1 = {'rCode': 0,'rMsg':'EmpID chưa được tạo Users'}
    offtypeId = []
    s = f'''
            SELECT OffTypeID FROM dbo.OffType
            '''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))

    if form.type in offtypeId:
        if form.period > 0:
            #if form.startdate >= datetime.date.today() + timedelta(days=2) and form.startdate.isoweekday() != 7: #isoweekday lấy số nguyên theo thứ trong tuần (7 là ngày chủ nhật)
            #trường hợp lưu lại: regdate = NULL #comment là trạng thái 0: lưu , 1: gửi đơn
            a = []
            b = []
            if form.startdate < datetime.date.today() + timedelta(days=2):
                a = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
            if form.startdate.isoweekday() == 7:
                b = ['Ngày nghỉ phép là ngày chủ nhật']

            if form.command == 0:
                c = 'NULL'
                d = 'Đơn đã lưu'
            elif form.command == 1:
                c = 'SYSDATETIME()'
                d = 'Đơn đã gửi'
            else:
                return note
            
            if form.reason == "":
                return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}
            
            #code cải tiến (viết lần 2)
            if fn.checkEmplIDUser(emplid):
                s = f'''
                    INSERT INTO dbo.OffRegister(EmpID,Type,Reason,Startdate,Period,RegDate,AnnualLeave,Address) 
                    VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{form.period}',{c},0,N'{form.address}')           
                    ''' 
                fn.commit_data(s)
                if a == [] and b == []:
                    return {'rCode':1,'rMsg': d}
                return {'rCode':1,'rMsg': d,'rError':{'startdate': a + b}}
            else:
                return note1

            #viết lần 1
            # if form.command == 0:
            #     if fn.checkEmplIDUser(emplid):
            #         s = f'''
            #             INSERT INTO dbo.OffRegister(EmpID,Type,Reason,StartDate,Period,RegDate,AnnualLeave,Address) VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{form.period}',NULL,0,'{form.address}')
            #             ''' 
            #         fn.commit_data(s)
            #         return {'rCode':1,'rData':{},'rMsg':{'notification':'Đơn đã lưu','startdate':a + b}}
            #     else:
            #         return note1
            # #trường hợp gửi đơn: regdate = ngày đăng ký
            # elif form.command == 1:
            #     if fn.checkEmplIDUser(emplid):
            #         s = f'''
            #             INSERT INTO dbo.OffRegister(EmpID,Type,Reason,StartDate,Period,RegDate,AnnualLeave,Address) VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{form.period}',SYSDATETIME(),0,'{form.address}')
            #             ''' 
            #         fn.commit_data(s)

            #         return {'rCode':1,'rData':{},'rMsg':{'notification':'Đơn đã gửi','startdate':a + b}}
            #     else:
            #         return note1
            # else:
            #     return note
        else:
            return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID (loại phép)'}


# đăng ký nghỉ phép - gửi mail - đang sử dụng
# @app.post("/day-off-letter", tags=['OffRegister'],summary='đăng ký nghỉ phép - gửi mail',dependencies=[Depends(validate_token)])#,dependencies=[Depends(validate_token)]
async def offDayRegister(form: Offregister,emplid: str = Depends(validate_token)): #Done
    note = {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
    note1 = {'rCode': 0,'rMsg':'EmpID chưa được tạo Users'}
    offtypeId = []
    s = f'''SELECT OffTypeID FROM dbo.OffType'''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))
    if form.type in offtypeId:
        if form.period > 0:
            #if form.startdate >= datetime.date.today() + timedelta(days=2) and form.startdate.isoweekday() != 7: #isoweekday lấy số nguyên theo thứ trong tuần (7 là ngày chủ nhật)
            #trường hợp lưu lại: regdate = NULL #comment là trạng thái 0: lưu , 1: gửi đơn
            warning = []
            warning_2 = []
            if form.period < 3:
                if form.startdate < datetime.date.today() + timedelta(days=2):
                    warning = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
            elif form.period < 7:
                if form.startdate < datetime.date.today() + timedelta(days=5):
                    warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 5 ngày cho lần sau']
            elif form.period >= 7:
                if form.startdate < datetime.date.today() + timedelta(days=10):
                    warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 10 ngày cho lần sau']
            if form.startdate.isoweekday() == 7:
                warning_2 = ['Ngày nghỉ phép là ngày chủ nhật']
            if form.command == 0:
                c = 'NULL'
                rMsg = ['Đơn đã lưu']
                email_notifi = ['Đơn chưa được gửi mail']
            elif form.command == 1:
                c = 'SYSDATETIME()'
                rMsg = ['Đơn đã gửi']
                email_notifi = []
                if form.reason == "":
                    return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}
            else:
                return note
            #code cải tiến (viết lần 2)
            if fn.checkEmplIDUser(emplid):
                s = f'''INSERT INTO dbo.OffRegister(EmpID,Type,Reason,Startdate,Period,RegDate,AnnualLeave,Address) 
                    VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{form.period}',{c},0,N'{form.address}')''' 
                fn.commit_data(s)
                #gửi mail nếu như tình trạng đơn đã gửi
                if form.command == 1:
                    receiver_mails_manag = fn.get_receiver_email_manag(emplid)
                    # email_ApprovalOder = fn.get_email_ApprovalOder(emplid)
                    # receiver_mails_manag.extend(email_ApprovalOder)
                    print(receiver_mails_manag)
                    if len(receiver_mails_manag)>0:
                        fn.sentMail(receiver_mails_manag,0)
                if warning == [] and warning_2 == [] and email_notifi == []:
                    return {'rCode':1,'rMsg': rMsg}
                return {'rCode':1,'rMsg': rMsg + email_notifi,'rError':{'startdate': warning + warning_2}}
            else:
                return note1
        else:
            return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID (loại phép)'}




@app.get("/day-off-letters",tags=['OffRegister'],summary='truyền vào số 1: quản lý đơn nghỉ phép, 0:lấy đơn chính mình, khác: lấy đơn nghỉ phép được chỉ định')
async def getsListoffstatus(needAppr: int = "",astatus:str = "",emplid: int = Depends(validate_token)):
    list_astatus = []
    if astatus != "":
        split_ = astatus.split(",")
        for i in range(0,len(split_)):
            if split_[i].isnumeric():
                list_astatus.append(int(split_[i]))
    s = f'''
            SELECT e.DeptID,j.JPLevel FROM dbo.Employee e
            LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
            WHERE e.EmpID = '{emplid}'
            '''
    result = fn.get_data(s)
    for i in result:
        depid = i[0]
        jplevel = i[1]
        
    jplevel_TP_PP = ((int(jplevel/10)+1)*10)+9



    if needAppr == 1:
        if jplevel <= 50  and jplevel >= 40:
            query = fn.depart_manager(emplid) + fn.roommates(depid,jplevel,1) #fn.depart_manager(emplid,jplevel_TP_PP) lấy đơn trưởng phó phòng
        elif jplevel < 40:
            query = fn.TPPP_manager(emplid,jplevel_TP_PP) + fn.roommates(depid,jplevel,1)
        else:   
            return {'rCode':0,'rData':[],'rMsg':''}
    elif needAppr == 0:
        if jplevel == 50:
            query = fn.myself(emplid) + fn.roommates(depid,jplevel)
        #elif jplevel < 50:
            #query = fn.myself(emplid)# + fn.roommates(depid,jplevel,1)
        else:
            query = fn.myself(emplid)
    else:
        query = fn.entrust(emplid)
    
    if len(list_astatus)>0:
        ketqua = []
        for i in query:
            if i['aStatus'] in list_astatus:
                ketqua.append(i)
        return {'rCode':1, 'rData': ketqua,'rMsg': 'lấy danh sách nghĩ phép thành công'}
    return {'rCode':1, 'rData': query,'rMsg': 'lấy danh sách nghĩ phép không thành công'}


#sử dụng lần đầu
# @app.put("/adjust-day-off",tags=['OffRegister'],summary='Điều chỉnh đơn nghỉ phép')   
async def adjust(form: AdjustDayOff, emplid: int = Depends(validate_token)):
    offtypeId = []
    s = f'''SELECT OffTypeID FROM dbo.OffType'''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))
    s1 = f"""SELECT EmpID  FROM dbo.OffRegister WHERE regID = '{form.regid}' AND RegDate IS NULL"""
    result_1 = fn.get_data(s1)
    # if emplid == 
    if len(result_1) > 0:
        if int(emplid) == result_1[0][0]:
            if form.offtype in offtypeId:
                if form.period > 0:
                    warning = []
                    warning_2 = []
                    if form.period < 3:
                        if form.startdate < datetime.date.today() + timedelta(days=2):
                            warning = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
                    elif form.period < 7:
                        if form.startdate < datetime.date.today() + timedelta(days=5):
                            warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 5 ngày cho lần sau']
                    elif form.period >= 7:
                        if form.startdate < datetime.date.today() + timedelta(days=10):
                            warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 10 ngày cho lần sau']
                    if form.startdate.isoweekday() == 7:
                        warning_2 = ['Ngày nghĩ phép là ngày chủ nhật']
                    if form.command == 0:
                        c = 'NULL'
                        rMsg = ['Chỉnh sửa đơn thành công, đơn đã được lưu']
                        email_notifi = ['Đơn chưa được gửi mail']
                    elif form.command == 1:
                        c = 'SYSDATETIME()'
                        rMsg = ['Chỉnh sửa đơn thành công, đơn đã được gửi']
                        email_notifi = []
                        if form.reason == "":
                            return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}
                    else:
                        return {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
                    s = f'''UPDATE dbo.OffRegister 
                            SET Type = '{form.offtype}', Reason = N'{form.reason}',StartDate = '{form.startdate}',Period = '{form.period}',RegDate = {c},Address = N'{form.address}'
                            WHERE regID = {form.regid}''' 
                    fn.commit_data(s)
                    #gửi mail nếu như đã phê duyệt đồng ý
                    if form.command == 1:
                        receiver_mails_manag = fn.get_receiver_email_manag(emplid)
                    # email_ApprovalOder = fn.get_email_ApprovalOder(emplid)
                    # receiver_mails_manag.extend(email_ApprovalOder)
                        print(receiver_mails_manag)
                        if len(receiver_mails_manag)>0:
                            fn.sentMail(receiver_mails_manag,0)
                    if warning == [] and warning_2 == [] and email_notifi == []:
                        return {'rCode':1,'rMsg': rMsg}
                    return {'rCode':1,'rMsg': rMsg + email_notifi,'rError':{'startdate': warning + warning_2}}
                else:
                    return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
            else:
                return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID'}
        else:
            return {'rCode':0, 'rData': {},'rMsg':'Bạn không được regid adjustment'}
    else: 
        return {'rCode':0,'rData':{},'rMsg':'regId không tồn tại hoặc regId đã gửi đơn'}


# tìm đơn nghĩ phép thep regID viết lần 4
@app.get("/day-off-letter",tags=['OffRegister'],summary='lấy đơn nghỉ phép theo regID (mã đơn)')
async def dayoffregID(regid = None):
    if str(regid).isnumeric():
        
        s = f"""
                SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.Type,
                        e.FirstName,e.LastName,e.comedate,e.DeptID,e.PosID,
		                j.Name AS JobPositionName,
                        d.Name AS departmentName,
						jpl.Name AS Position,
                    case 
                        when o.RegDate is null then 0 --N'chưa gửi' 
                        --đơn đó duyệt thì trường regdate phải có data
                        when sum(a.ApprovalState) is null then 1 --N'Chờ Duyệt' 
                        when sum(a.ApprovalState) = 1 then 2 --N'Đã Duyệt'
                        when sum(a.ApprovalState) = 0 then 3 --N'Từ Chối'
                        when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận'
                        when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
                    ELSE 'Error!' end as aStatus 
                FROM dbo.OffRegister o
                LEFT JOIN dbo.Approval a ON a.regID = o.regID
                LEFT JOIN Employee e ON o.EmpID = e.EmpID
				LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
				LEFT JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
                WHERE o.regID = '{regid}'
                group by o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.type,
                e.FirstName,e.LastName,e.comedate,e.DeptID,e.PosID,
				j.Name,d.Name,jpl.Name
                """
        result = fn.get_data(s,1)
        # print(result[0]['aStatus'])
        # if result[0]['aStatus'] == 0:
        # if result[0]['aStatus'] == 1:
        if len(result)>0: # kết quả của câu truy vấn lần 1 lấy status (trường hợp có data)
            
            s1 = f"""
                        SELECT a.ApprovalID,a.regID,a.ApprOrder,a.Approver,a.JobPosID AS 'ApproJobposID',a.Comment,a.ApprovalState,a.ApprovalDate,
                        e.DeptID AS 'ApproDeptID',e.LastName AS 'ApproLastName',e.FirstName AS 'ApproFirstName',
                        j.Name AS ApproJobName,
                        d.Name AS departmentName,
						jpl.Name AS Position
                        FROM dbo.Approval AS a
                        LEFT JOIN dbo.Employee AS e ON e.EmpID = a.Approver
                        LEFT JOIN dbo.JobPosition AS j ON j.JobPosID = a.JobPosID
                        LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
						LEFT JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
                        WHERE regID = '{regid}'
                        ORDER BY a.ApprOrder ASC
                        """
            rApprInf = fn.get_data(s1,1)
            if len(rApprInf)>0:
                for i in range(0,len(rApprInf)):
                    if rApprInf[i]['ApprOrder'] == 1:
                        if rApprInf[i]['ApprovalState'] == 1:
                            rApprInf[i]['StateName'] = 'Chấp nhận'
                        elif rApprInf[i]['ApprovalState'] == 0:
                            rApprInf[i]['StateName'] = 'Từ chối'
                    elif rApprInf[i]['ApprOrder'] == 2:
                        rApprInf[i]['StateName'] = 'Đã nhận'
                    else:
                        rApprInf[i]['StateName'] = 'Đã Kiểm soát'

            result[0]['apprInf'] = rApprInf
            return {'rCode': 1,'rData':result[0],'rMsg':'Lấy đơn thành công'}
    return {'rCode': 0,'rData':{},'rMsg':'Đơn không tồn tại'}
           




# phê duyệt
# @app.post("/approve",tags=['Approve'],summary='Phê duyệt đơn')
async def approve(form: Approve,approver: str = Depends(validate_token)): #form: Approve
    # kiểm tra regID có tồn tại hay ko
    s = f"""
            SELECT RegDate FROM dbo.OffRegister
            WHERE regID = '{form.regid}' AND RegDate IS NOT NULL      
        """
    result = fn.get_data(s)
    
    #kiểm nếu có đơn thì kiểm tra duyệt chưa, không có đơn trả về lỗi
    if len(result)>0:
        # kiểm tra regID đã được phê duyệt chưa
        s = f"""
                SELECT CASE WHEN max(apprOrder) IS NULL THEN 0   ELSE max(apprOrder)   END as aOrder 
                FROM dbo.Approval
                WHERE regID = '{form.regid}'      
            """
        result = fn.get_data(s)
        
        aOrder = result[0][0]
        if aOrder == 0: #chưa phê duyệt
            aOrder += 1
            #lấy thông tin người approve
            s = f"""
                select e.PosID,j.JPLevel from Employee e
                inner join JobPosition j on e.PosID = j.JobPosID 
                where EmpID = '{approver}'
                """
            result = fn.get_data(s)


            jobposid = ''
            if len(result) >0:
                jobposid = result[0][0]
                if result[0][1]>=60:
                    return {'rCode':0,'rData':{},'rMsg':'Bạn chưa được phân quyền phê duyệt'}
            # if form.comment == '':
            #     return {'rCode':0,'rMsg':'vui lòng nhập lý do phê duyệt'}
            
            if form.state != 1:
                form.state = 0
                if form.comment == '':
                    return {'rCode':0,'rMsg':'vui lòng nhập lý do phê duyệt'}
            
            s = f'''
            INSERT INTO dbo.Approval(regID,ApprOrder,Approver,JobPosID,adjType,adjStartDate,adjPeriod,Comment,ApprovalState,ApprovalDate)
            VALUES
            ('{form.regid}','{aOrder}','{approver}','{jobposid}',0,SYSDATETIME(),0,N'{form.comment}','{form.state}',SYSDATETIME())
            ''' 
            fn.commit_data(s)
            return {'rCode':1,'rData':{},'rMsg':'Phê duyệt thành công'}
        else:
            return {'rCode':0,'rData':{},'rMsg':'Phê duyệt không thành công, đơn đã được phê duyệt trước đó'}
    else:
        return{'rCode':0,'rdata': {},'rMsg':'Regid không tồn tại'}
   
# @app.post("/approve",tags=['Approve'],summary='Phê duyệt đơn') #phê duyệt gửi mail
async def approve(form: Approve,approver: str = Depends(validate_token)): #form: Approve
    # kiểm tra regID có tồn tại hay ko
    s = f"""
            SELECT o.RegDate, u.Email FROM dbo.OffRegister o
            LEFT JOIN dbo.Users u ON u.EmpID = o.EmpID 
            WHERE regID = '{form.regid}' AND RegDate IS NOT NULL      
        """
    result1 = fn.get_data(s)
    
    #kiểm nếu có đơn thì kiểm tra duyệt chưa, không có đơn trả về lỗi
    if len(result1)>0:
        # kiểm tra regID đã được phê duyệt chưa
        s = f"""
                SELECT CASE WHEN max(apprOrder) IS NULL THEN 0   ELSE max(apprOrder)   END as aOrder 
                FROM dbo.Approval
                WHERE regID = '{form.regid}'      
            """
        result = fn.get_data(s)
        
        aOrder = result[0][0]
        if aOrder == 0: #chưa phê duyệt
            aOrder += 1
            #lấy thông tin người approve
            s = f"""select PosID from Employee where EmpID = '{approver}'"""
            result = fn.get_data(s)
            jobposid = ''
            if len(result) >0:
                jobposid = result[0][0]
            if form.state != 1:
                form.state = 0
                if form.comment == '':
                    return {'rCode':0,'rMsg':'vui lòng nhập lý do phê duyệt'}
            s = f'''
            INSERT INTO dbo.Approval(regID,ApprOrder,Approver,JobPosID,adjType,adjStartDate,adjPeriod,Comment,ApprovalState,ApprovalDate)
            VALUES
            ('{form.regid}','{aOrder}','{approver}','{jobposid}',0,SYSDATETIME(),0,N'{form.comment}','{form.state}',SYSDATETIME())
            ''' 
            fn.commit_data(s)
            receiver_mail = []
            receiver_mail.append(result1[0][1])
            fn.sentMail(receiver_mail,1)
            if form.state == 1:
                #lấy mail nhân sự
                mail_HRM = []
                s1 = f'''  
                        SELECT e.EmpID,e.FirstName,e.LastName,j.JPLevel,u.Email FROM dbo.Employee e 
                        LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                        LEFT JOIN dbo.Users u ON u.EmpID = e.EmpID
                        WHERE e.DeptID = 'NS'AND j.JPLevel <=50
                        '''
                query = fn.get_data(s1)
                for row in query:
                    mail_HRM.append(row[4])
                fn.sentMail(mail_HRM,2)
            return {'rCode':1,'rData':{},'rMsg':'Phê duyệt thành công'}
        else:
            return {'rCode':0,'rData':{},'rMsg':'Phê duyệt không thành công, đơn đã được phê duyệt trước đó'}
    else:
        return{'rCode':0,'rdata': {},'rMsg':'Regid không tồn tại'}





# @app.get("/day-off-summary",tags=['Version 2'],summary='lấy file tổng kết số ngày nghĩ phép trong tháng') #chỉnh sửa lại method
async def sum(date: datetime.date):
    m = date.month
    y = date.year
    s = f'''
            SELECT o.EmpID,ot.Name AS 'OffTypeName',SUM(o.Period) AS 'Period',
                        --MONTH(o.StartDate) AS month,
						--YEAR(o.StartDate) AS year,
                        e.FirstName,e.LastName,FORMAT(e.ComeDate,'MM/dd/yyyy') AS ComeDate,
                        j.Name AS 'JobPositionName',
                        d.Name AS 'departmentName',
                        al.AnnualLeave
                FROM dbo.OffRegister o
                INNER JOIN dbo.Approval a ON a.regID = o.regID
                INNER JOIN dbo.OffType ot ON ot.OffTypeID = o.Type
                INNER JOIN dbo.Employee e ON e.EmpID = o.EmpID
                INNER JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                INNER JOIN dbo.Department d ON d.DeptID = e.DeptID
                LEFT JOIN dbo.AnnualLeave al ON al.EmpID = e.EmpID
                WHERE a.ApprOrder = 1 AND a.ApprovalState = 1
                    AND YEAR(o.StartDate) = {y}
					AND MONTH(o.StartDate) = {m}
                GROUP BY o.EmpID,o.Type,
                        ot.Name,
                        e.FirstName,e.LastName,e.DeptID,e.PosID,ComeDate,
                        j.Name,
                        d.Name,al.AnnualLeave
                        --MONTH(o.StartDate),
						--YEAR(o.StartDate),al.AnnualLeave
                order by ot.name asc
        '''
    result_query = fn.get_data(s,1)

    # print(result_query)
    key = []
    list_key = []
    output_result = []
    for row in result_query:
        key = row['EmpID']
        if key not in list_key:
            list_key.append(key)
            row[row['OffTypeName']] = row['Period']
            del row['OffTypeName'], row['Period']
            output_result.append(row)
        else:
            number = 0
            for i in output_result:
                if key == i['EmpID']:
                    # print(output_result[number])
                    output_result[number][row['OffTypeName']] = row['Period']
                    # print(output_result[number])
                number += 1

    #     if NOT output.exists(key):
    #         output[key] = row
    #         output[key][row['OffTypeName']] = row['Period']
    #         del output[key]['OffTypeName'], output[key]['Period']
    #     else:
    #         if NOT output[key].exists(row['OffTypeName']):
    #             output[key][row['OffTypeName']] = 0
                
    #         output[key][row['OffTypeName']] += row['Period']
    # i =0
    # for each key in output.keys:
    #     output_result[i] = output[key]
    #     i++
    # -------------------------------------------------------------------
    df = pd.DataFrame(output_result)
    s1 = """
            SELECT Name FROM dbo.OffType
            """
    result_query1 = fn.get_data(s1)

    headers = []
    offtype = []
    for row in result_query1:
        offtype.append(row[0])
    print(output_result)
    for index in output_result:
        # print(index)
        for x in index:
            # print(x)
            if x not in headers:
                headers.append(x)
                # print(headers)
    print(df['EmpID'])
    for index in offtype:
        if index not in headers:
            df[index] = ""
    
    df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
    
   
    # print(df)
    # df = pd.DataFrame(output_result).to_excel("data.xlsx",index= False)
    # df = pd.DataFrame(output_result)
    # print(df)
    # return {'rCode': 1, 'rData': output_result, 'rMsg':'Lấy danh sách loại phép thành công'}
    return FileResponse('file.xlsx',filename='Data.xlsx')
    




# Nhân sự lấy đơn đã duyệt (tiếp nhận)
@app.get("/day-off-letter-HRM",tags=['Version 2'],summary='Nhân sự lấy đơn đã duyệt (tiếp nhận)')
async def dayOffLetterHrm(emplid: int = Depends(validate_token)):
    s = f'''
            SELECT e.DeptID,j.JPLevel FROM dbo.Employee e
            INNER JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
            WHERE e.DeptID = 'NS' AND j.JPLevel <= 50 AND e.EmpID = '{emplid}'
                '''
    query_s = fn.get_data(s)
    
    if len(query_s)>0:
        s1 = f'''
                SELECT o.regID,o.EmpID,e.FirstName,e.LastName,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,
                a.ApprOrder,a.Approver,a.Comment,a.ApprovalDate,
                epl.FirstName AS Approver_FirstName,epl.LastName AS Approver_LastName,
                j.Name AS Approver_jobPosition
                FROM dbo.OffRegister o
                INNER JOIN dbo.Approval a ON a.regID = o.regID
                INNER JOIN	dbo.Employee e ON e.EmpID = o.EmpID
                INNER JOIN dbo.Employee epl ON epl.EmpID = a.Approver
                INNER JOIN dbo.JobPosition j ON j.JobPosID = epl.PosID
                WHERE o.regID IN (
                                SELECT regID FROM dbo.Approval
                                WHERE ApprovalState = 1
                                GROUP BY regID
                                HAVING SUM(ApprOrder) = 1
                                )
                '''
        query_s1 = fn.get_data(s1,1)
        return {'rCode':1,'rData':query_s1,'rMsg':'lấy danh sách nghĩ phép thành công'}
    return {'rCode':0,'rData':{},'rMsg':'Bạn không phải là nhân viên NS hoặc không đủ quyền'}

#PNG,JPG,GIF,TIFF,PSD,PDF,JPEG,SVG
#JPEG,JPG -- tốc dộ tải ảnh lên web . PNG kiểm tra thêm
# @app.post("/add-Department",tags=[''])
@app.post("/upload/",tags=['Version 2'])
async def upload_file(file: UploadFile,emplID: str = Depends(validate_token)): #= File(...)
    # s = f'''SELECT * FROM dbo.Image WHERE EmpID = {emplID}'''
    # result = fn.get_data(s)
    # if len(result) < 1:
    #     s = f'''INSERT INTO dbo.Image(EmpID,ImageData) VALUES({emplID},NULL)'''
    #     fn.commit_data(s)

    #xóa đường link ảnh củ
    s = f'''SELECT ImageData FROM dbo.Image WHERE EmpID = {emplID}'''
    result = fn.get_data(s)
    if os.path.exists(result[0][0]):
        if result[0][0] != os.path.join('tempDir','30b39c90-f927-4154-bbe7-acd069988a54.JPG'): 
            os.remove(result[0][0])
        else:
            print(result[0][0]== os.path.join('tempDir','30b39c90-f927-4154-bbe7-acd069988a54.JPG')) #kiểm tra kết quả đường dẫn có bằng nhau không --> trả về True
    extension = file.filename.split(".")[1].upper()
    if extension not in ["PNG","JPG","JPEG"]:
        return {'rCode': 0,'rData': [],'rMsg':"đuôi ảnh không cho phép"}
    filename = str(uuid.uuid4()) + "." + extension
    file_path = os.path.join('tempDir',filename)
    print(file_path)
    with open(file_path, "wb") as buffer: #buffer là file object mở sẳn để ghi dữ liệu vào đó
        buffer.write(file.file.read()) #đọc file và viết vào file đệm
        print(buffer)
        # buffer.close()
    # s = f'''UPDATE image SET imagedata = '{file_path}' WHERE empID =  {emplID}'''
    s = f'''UPDATE image SET imagedata = '{filename}' WHERE empID =  {emplID}'''
    fn.commit_data(s)
    # os.remove(file_path)
    return {'rCode':1,'rMsg': 'Upload ảnh thành công'}

# @app.get('/get-image/',tags=['Version 2'])
# async def get_image(emplID: str = Depends(validate_token)):
#     s = f'''SELECT ImageData FROM dbo.Image WHERE EmpID = {emplID}'''
#     result = fn.get_data(s)
#     print('nhat')
#     print(result[0][0])

  
#     if os.path.exists(result[0][0]):
#         # current_directory = os.getcwd()
#         # file_path = os.path.join(current_directory,result[0][0])
#         # print(file_path)
#         a =2
#         return FileResponse(result[0][0],media_type="image/png")
       
#     return {'rCode':0,'rData':[],'rMsg':'hình ảnh không tồn tại'}
#----------------------------------------------------------------------------------------------------------------------------------------
# @app.get("/get-image/",tags=['Version 2'])#tags=['Version 2'],response_class=FileResponse
# async def get_image(emplID: str = Depends(validate_token)):
#     print('nhat')
#     s = f'''SELECT ImageData FROM dbo.Image WHERE EmpID = {emplID}'''
#     result = fn.get_data(s)
#     print(os.path.exists(result[0][0]))
#     print(result[0][0])
#     if os.path.exists(result[0][0]):
#         print('con quỷ')
#         return FileResponse(result[0][0])
#     return {'rCode':0,'rData':[],'rMsg':'hình ảnh không tồn tại'}
    
@app.get("/profile_img/",tags=['Version 2'])#tags=['Version 2'],response_class=FileResponse
async def profile_img(emplID: str = Depends(validate_token)):
    s = f'''SELECT ImageData FROM dbo.Image WHERE EmpID = {emplID}'''
    result = fn.get_data(s)
    path = os.path.join('tempDir',result[0][0])
    print()
    if os.path.exists(path):
        return {'rCode':1,
            'rData':f'/static/{result[0][0]}',
            'rMsg':'lấy thông tin thành công'}
    return {'rCode':0,'rData':[],'rMsg':'hình ảnh không tồn tại'}
    
   



# @app.get('/aaa/')
# async def aaa(request: requests):
#     return {'rData': requests.__url__('aaa')}

    #------------------------------------------------------------
    # file_image = file.filename
    # extension = file_image.split(".")[1].upper()
    # print(extension)
    # if extension not in ["PNG","JPG","JPEG"]:
    #     return {"status": "error", "detail": "đuôi ảnh không cho phép"}
    
    # filename = str(uuid.uuid4()) + '.' + extension
    # Link_image = os.path.join("tempDir", filename)
    # print(filename)
    
    
    # toke_name = secrets.token_hex(10)+"."+extension
    # print(file.file.read())
    # a = await file.read()
    # print(a)
    #-----------------------------------------------------------------------------------
   



    # print(file.filename)
    # # file.filename = f"{uuid.uuid4()}.jpg"
    # print(file.filename)
    # contents = await file.read()
    
    # with open(f"{ImageDir}{file.filename}","wb") as f:
    #     print(f)
    #     f.write(contents)

    
    # s = f'''
    #     INSERT INTO dbo.NHAT
    #         (
    #             EmpID,
    #             ImageName,
    #             ImageData
    #         )
    #         VALUES
    #         (   622110103,   -- EmpID - bigint
    #             'aaa',  -- ImageName - varchar(100)
    #             {contents} -- ImageData - varbinary(max)
    #             )
    #     '''
    # fn.commit_data(s)
    # return True
    #-------------------------------------------------------------------------------------------------------------------------------
    # file_temp = tempfile.NamedTemporaryFile(delete=False)
    # file_temp.write(await file.read())
    # file_temp.close()

    # with open(file_temp.name,"rb") as f:
    #     image_data = f.read()
    # image_data_binary = binascii.a2b_base64(image_data)
    # print(f)
    # s = f'''
    #     INSERT INTO dbo.NHAT
    #         (
    #             EmpID,
    #             ImageName,
    #             ImageData
    #         )
    #         VALUES
    #         (   622110103,   -- EmpID - bigint
    #             '',  -- ImageName - varchar(100)
    #             {image_data_binary} -- ImageData - varbinary(max)
    #             )
    #     '''
    # fn.commit_data(s)

    # return {'Note': image_data_binary}



#isalnum : kiểm tra xem ký tự có phải là chử cái hay số không
#unicodedata.category(c) == 'Zs' : kiểm tra có khoảng trắng hay không
#unicodedata.category(c) == 'Ll' : chữ cái viết thường
#unicodedata.category(c) == 'Lu' : chữ cái viết hoa
#unicodedata.category(c) == 'Lt' : chữ cái viết hoa nhưng không phải ký tự chữ
#unicodedata.category(c) == 'Lo' : Các ký tự thuộc loại này bao gồm các chữ cái trong các bảng mã khác nhau như Latin, Cyrillic, Greek, Hangul, Hiragana, Katakana và các ký tự chữ cái trong các ngôn ngữ khác như tiếng Trung, tiếng Ả Rập, tiếng Hebrew, tiếng Hindi, tiếng Thái, tiếng Hàn Quốc, tiếng Nhật và nhiều ngôn ngữ khác nữa.
#unicodedata.category(c) == 'Pd' : ký tự dấu gạch ngang

@app.get('/get-department',tags=['Department'],summary='lấy danh sách phòng ban hiện có')
async def get_department():
    s = f'''SELECT d.DeptID,d.Name,d.DeptLevel,d.pDeptID,d.DeptMng,d.Status,d.Note,
		            dl.DLvlName 
            FROM dbo.Department d
            INNER JOIN dbo.DeptLevel dl ON dl.DLvlCode = d.DeptLevel'''
    result = fn.get_data(s,1)
    if len(result)>0:
        return {'rCode':1,'rData': result,'rMsg':'Lấy danh sách phòng ban thành công'}
    else:
        return {'rCode':0,'rData': {},'rMsg':'Không có danh sách phòng ban'}
    

@app.post('/import-department',tags=['Department'],summary='thêm phòng ban')
async def import_department(form: Im_department):
    if form.name_deptID == '':
        return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập tên phòng ban'}
    else:
        is_alpha_numeric = all(c.isalnum()
                    or unicodedata.category(c) == 'Zs' 
                    or unicodedata.category(c) == 'Ll' 
                    or unicodedata.category(c) == 'Lu' 
                    or unicodedata.category(c) == 'Lt' 
                    or unicodedata.category(c) == 'Pd'  
                    for c in form.name_deptID)
        if is_alpha_numeric:
            remove_blank = form.name_deptID.strip(' ') # remove khoảng trống (đầu-cuối) của chuỗi
            print(len(remove_blank))
            blank_index = remove_blank.find(" ") # tình vị trí khoảng trống (nằm ở vị trí thứ mấy)
            # print(blank_index)
            hyphen_index = remove_blank.find('-') # tìm vị trí dấu gạch ngang (nằm ở vị trí thứ mấy)
            # print(hyphen_index)
            deptID = ''
            split_ = ''
            if blank_index > 0 and hyphen_index >= 0: #không cho dấu cách và dấu gạch cùng lúc
                return {'rCode':0,'rData':{},'rMsg': 'Tên phòng ban không được phép'}
            elif blank_index > 0: #Tách chuỗi theo điều kiện khoảng cách
                split_ = remove_blank.split(" ")
            elif hyphen_index > 0: #Tách chuỗi theo điều kiện dấu gạch ngang
                split_ = remove_blank.split("-")
                # new_list = []
            elif blank_index < 0 and hyphen_index < 0: #nếu không có dấu gạch và dấu cách thì ko cần tách
                 split_ = remove_blank
            else:
                return {'rCode':0,'rData':{},'rMsg': 'Tên phòng ban không được phép'}
            # print(split_)
           
            for index in split_: #chạy từng phần tử của trong list hoặc chuỗi
                # print(index)
                if index != '':
                    # print(index)
                    # new_list.append(index)
                    deptID += index[0].upper() #nối từng phần tử đầu tiên của chuỗi trong list lại và chuyển thành chử hoa
                    
            print("Chuỗi này chỉ chứa các chữ cái không dấu, các chữ cái có dấu và số")
            # print(result)
            if form.deptlevel not in fn.deptlevel(): #form.deptlevel.isnumeric() == False or 
                return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập cấp độ phòng ban'}
            print(len(form.pDeptID))
            if len(form.pDeptID) > 0:
                # form.pDeptID = 'NULL'
                s = f''' SELECT * FROM dbo.Department WHERE DeptID = '{form.pDeptID}' '''
                query = fn.get_data(s)
                if len(query) <= 0 or query[0][2] >= int(form.deptlevel): #ràng buộc điều kiện (kết quả truy vấn không có hoặc cấp độ phòng ban quản lý 'lơn hơn hoặc =' phòng ban đang thêm vào)
                    return {'rCode':0,'rData':{},'rMsg':'vui lòng chọn phòng ban quản lý khác'} #phòng ban quản lý không đủ 
            else:
                return {'rCode':0,'rData':{},'rMsg':'vui lòng chọn phòng ban quản lý'}
                # print(123)
            print(len(form.note))
            if  len(form.note) <= 0:
                form.note = ''
                print(form.note)
            if deptID in fn.deptID_list():
                letters_and_digits = string.digits #string.ascii_letters + 
                autogenous = ''.join((random.choice(letters_and_digits) for i in range(5)))
                deptID += f'-{autogenous}'
                print(deptID)
                if deptID in fn.deptID_list():
                    return {'rCode': 0,'rData':{},'rMsg':'Phòng ban đã tồn tại, vui lòng kiểm tra trước khi thêm phòng ban'}
                # def generate_autogenous_id(length):
                #     letters_and_digits = string.ascii_letters + string.digits
                #     autogenous_id = ''.join((random.choice(letters_and_digits) for i in range(length)))
                #     return autogenous_id
                # id = generate_autogenous_id(10)
            if len(deptID) > 0:
            #viết thêm câu lệnh insert
                name = re.sub("\s+", " ", remove_blank) # thay thế 1 khoảng trống, từ nhiều khoảng trống
                s = f'''INSERT INTO dbo.Department(DeptID,Name,DeptLevel,pDeptID,DeptMng,Status,Note)
                        VALUES
                        (   '{deptID}',  -- DeptID - varchar(8)
                            N'{name}', -- Name - nvarchar(50)
                            {int(form.deptlevel)},   -- DeptLevel - tinyint
                            '{form.pDeptID.upper()}',  -- pDeptID - varchar(8)
                            NULL,   -- DeptMng - bigint
                            0,   -- Status - tinyint
                            N'{form.note}'  -- Note - nvarchar(200)
                            )'''
                fn.commit_data(s)
                return {'rCode':1,'rData':{'DeptID':deptID,'name_deptID':name,'status': 0},'rMsg':'Thêm phòng ban thành công'}
            else:
                return {'rCode': 0,'rData':{},'rMsg':'vui lòng nhập tên phòng ban'} 
        else:
            return {'rCode':0,'rData':{},'rMsg':'Tên phòng ban không được phép'}




@app.put('/update-department',tags=['Department'],summary='cập nhật lại phòng ban')
async def update_department(form: Update_department):
    s = f'''SELECT * FROM dbo.Department WHERE DeptID = '{form.deptID}' '''
    result = fn.get_data(s)
    print(result)
    if len(result)>0:
        name = result[0][1]
        if len(form.nameDeptID)>0:
            is_alpha_numeric = all(c.isalnum() 
                        or unicodedata.category(c) == 'Zs' 
                        or unicodedata.category(c) == 'Ll'
                        or unicodedata.category(c) == 'Lu' 
                        or unicodedata.category(c) == 'Lt' 
                        or unicodedata.category(c) == 'Pd'  
                        for c in form.nameDeptID)
            if is_alpha_numeric:
                remove_blank = form.nameDeptID.strip(' ') # remove khoảng trống (đầu-cuối) của chuỗi
                name = re.sub("\s+", " ", remove_blank) #thay thế nhiều khoảng trống thành 1 khoảng trắng
            else:
                return {'rCode':0,'rData':{},'rMsg':'Tên phòng ban không được phép'}
            
        deptlevel = result[0][2]
        if form.deptLevel > 0:
            if form.deptLevel in fn.deptlevel():
                deptlevel = form.deptLevel
            else:
                return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập cấp độ phòng ban'}
        
        #pDeptID = result[0][3] #pDeptID chưa được update (đã có trước đó)
        if len(form.pDeptID) > 0:
        # form.pDeptID = 'NULL'
            s = f''' SELECT * FROM dbo.Department WHERE DeptID = '{form.pDeptID}' '''
            query = fn.get_data(s)
            if len(query) > 0:
                r = {'rCode':0,'rData':{},'rMsg':'vui lòng chọn phòng ban quản lý khác'}
                #if form.deptLevel >0: #so sánh deptlevel mới input vào
                if query[0][2] >= deptlevel or query[0][0] == form.deptID.upper():
                    return r
                else:
                    pDeptID = form.pDeptID
                # elif form.deptLevel < 0: #so sánh deptlevel trước đó (input không nhập)
                #     if query[0][2] >= deptlevel or query[0][0] == form.deptID.upper() :
                #         return r
                #     else:
                #         pDeptID = form.pDeptID
                #---------------------------------------------------------------------------------------------------
                # if len(query) <= 0 or query[0][2] >= int(deptlevel) or query[0][0] == form.deptID.upper() or result[0][2] <= query[0][2]: #ràng buộc điều kiện (kết quả truy vấn không có hoặc cấp độ phòng ban quản lý 'lơn hơn hoặc =' phòng ban đang thêm vào)
                #     return {'rCode':0,'rData':{},'rMsg':'vui lòng chọn phòng ban quản lý khác'}
                # else:
                #     pDeptID = form.pDeptID
            else:
                return {'rCode':0,'rData':{},'rMsg':'phòng ban quản lý không tồn tại'} 
        else:
            s = f''' SELECT * FROM dbo.Department WHERE DeptID = '{result[0][3]}' ''' #lấy deptlevel của phòng ban cha (old) so sánh với deptlevel (old or new) của phòng ban con
            query = fn.get_data(s)
            if len(query) > 0: #or query[0][2] >= deptlevel:
                r = {'rCode':0,'rData':{},'rMsg':'deptlevel cấp độ phòng ban lớn hơn hoặc bằng phòng ban parents'}
                if query[0][2] >= deptlevel:
                    return r
                else:
                    pDeptID = result[0][3] #lấy lại phòng quản lý trong cũ (deptlevel của phòng ban quản lý cũ hợp lệ(nhỏ hơn) với deptlevel của phòng ban cập nhật)
            else:
                return {'rCode':0,'rData':{},'rMsg':'phòng ban quản lý không tồn tại'} 

        deptMng = 'NULL'
        if form.deptMng != 0:
            deptMng = 'NULL'
        status = 1
        if form.status != 1:
            status = 0
        if  len(form.note) <= 0:
            form.note = result[0][6]
        print(deptlevel)
        s = f'''UPDATE dbo.Department SET Name = N'{name}',DeptLevel = {deptlevel},pDeptID = '{pDeptID.upper()}',DeptMng = {deptMng},Status = {status},Note = N'{form.note}'
                where deptID = '{form.deptID}' '''
        fn.commit_data(s)
        return {'rCode': 1,'rData':{'status':status},'rMsg':'Cập nhật phòng ban thành công'}
    else:
        return {'rcode':0, 'rData':{},'rMsg':'Phòng ban không tồn tại'}


    # s = f'''UPDATE dbo.Department SET DeptID = 'ádasdas',Name = N'adsjasldj',DeptLevel = 121,pDeptID = 'kjlkj',DeptMng = NULL,Status = 1,Note = N'dfsdf' '''





        
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

# app.mount(
#     "/static", StaticFiles(directory="tempDir"), name="tempDir")
# templates = Jinja2Templates(directory="tempDir")
# @app.get("/")
# def static(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


@app.get('/get-department-tree',tags=['Department'],summary='lấy cây thư mục phòng ban')
async def get_department_tree(deptID: str = None):
    a = fn.department_deptID(deptID)
    # print(len(a))
    # print(a)
    # print(a[0]['DeptID'])
    if len(a) > 0:
        b = fn.department_pdeptID(a[0]['DeptID'])
        a[0]['children'] = b
        # index = len(b)
        k = 0
        for row in b:
            c = fn.department_pdeptID(row['DeptID']) #print(row['DeptID'])
            if len(c)>0:
                a[0]['children'][k]['children'] = c #k
                k1 = 0
                # for row1 in c:
                for row1 in c:
                    d = fn.department_pdeptID(row1['DeptID'])
                    if len(d)>0:
                        a[0]['children'][k]['children'][k1]['children'] = d #k1
                        k2 = 0
                        for row2 in d:
                            e = fn.department_pdeptID(row2['DeptID'])
                            if len(e)>0:
                                a[0]['children'][k]['children'][k1]['children'][k2]['children'] = e #k2
                                k3 = 0
                                for row3 in e:
                                    f = fn.department_pdeptID(row3['DeptID'])
                                    if len(f) > 0:
                                        a[0]['children'][k]['children'][k1]['children'][k2]['children'][k3]['children'] = f  #k3
                                        k4 = 0
                                        for row4 in f:
                                            g = fn.department_pdeptID(row4['DeptID'])
                                            if len(g)>0:
                                                a[0]['children'][k]['children'][k1]['children'][k2]['children'][k3]['children'][k4]['children'] = g #k4
                                                k5 = 0
                                                for row5 in g:
                                                    h = fn.department_pdeptID(row5['DeptID'])
                                                    if len(h)>0:
                                                        a[0]['children'][k]['children'][k1]['children'][k2]['children'][k3]['children'][k4]['children'][k5]['children'] = h #k5
                                                    k5+=1
                                            k4+=1
                                    k3+=1
                            k2+=1
                    k1+=1
            k+=1
        return {'rCode':0,'rData':a,'rMsg':'lấy danh sách thành công'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập ID'}



@app.get('/get-deptlevel',tags=['Department'],summary='lấy cấp độ phòng ban')
async def get_deptlevel():
    s = f''' SELECT * FROM deptlevel'''
    result = fn.get_data(s,1)
    if len(result)>0:
        return {'rCode':1,'rData':result,'rMsg':'Lấy danh sách thành công'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'danh sách không tồn tại'}


        
@app.get('/get-jplevel',tags=['JobTitle'],summary='lấy danh sách chức vụ')
async def get_jplevel():
    s = f'''SELECT * FROM dbo.JPLevel'''
    query = fn.get_data(s,1)
    if len(query)>0:
        return {'rCode': 1,'rData':query,'rMsg': 'lấy danh sách thành công'}
    return {'rCode': 0,'rData':{},'rMsg':'Danh sách không tồn tại'}

@app.post('/import-jplevel',tags=['JobTitle'],summary='thêm chức vụ')
async def import_jplevel(form: Import_position):
    if len(form.Name)>0:
        is_alpha_numeric = all(c.isalnum() 
            or unicodedata.category(c) == 'Zs' 
            or unicodedata.category(c) == 'Ll'
            or unicodedata.category(c) == 'Lu' 
            or unicodedata.category(c) == 'Lt' 
            or unicodedata.category(c) == 'Pd'  
            for c in form.Name)
        if is_alpha_numeric:
            remove_blank = form.Name.strip(' ')
            name = re.sub("\s+", " ", remove_blank) #thay thế nhiều khoảng trống thành 1 khoảng trắng
            # pJplevel = 'NULL'
            # if form.pJPlevel != 0:
            #     pJplevel = 'NULL'
            note = ''
            if len(form.note) > 0:
                note_blank = form.note.strip(' ') 
                note = re.sub("\s+", " ", note_blank)
        else:
            return {'rCode':0,'rData':{},'rMsg':'tên chức vụ không được phép'}
            
        jplevelID = []
        s = f'''SELECT JPLevelID FROM dbo.JPLevel'''
        query = fn.get_data(s)
        if len(query)> 0:
            for row in query:
                jplevelID.append(row[0])
            # if form.state == 1:
            #     max_jplevelID = (int(max(jplevelID)/10)*10) + 9 # lấy cấp chức vụ lớn nhất trong cùng 1 hàng đơn vị 79,89,....
            #     if form.jplevelID not in range(max(jplevelID)+1,max_jplevelID + 1): 
            #         return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập lại mã chức vụ (jplevelID)'}
            # else:
            #     print((int(max(jplevelID)/10)*10) + 10)
            #     if form.jplevelID != (int(max(jplevelID)/10)*10) + 10:
            #         return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập lại mã chức vụ (jplevelID)'}
            # max_jplevelID = (int(max(jplevelID)/10)*10) + 10
            # print(max_jplevelID)
            if form.jplevelID not in jplevelID:
                s = f'''insert into JPLevel (JPLevelID,Name,Status,pJPLevel,Note) 
                values
                ( {form.jplevelID},N'{name}',0,Null,N'{note}')'''
                fn.commit_data(s)
                return {'rCode':1,'rData':{},'rMsg':'Thêm chức danh thành công'}
            else:
                return {'rCode':0,'rData':{},'rMsg':'mã chức vụ (jplevelID) đã tồn tại'}
        else:
            return {'rCode':0,'rData':{},'rMsg':'vui lòng liên hệ IT'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'Vui lòng nhập tên chức vụ'}

                

                        




            
            # else:
            #     return False
            

            # if max_jplevelID == max(jplevelID):
            #     return True
            # else:
            #     return False
        # if form.jplevelID not in jplevelID and form.jplevelID in ((int(max(jplevelID)/10))+9): 
        #     return True
        
        # else:
        #     return {'rCode': 0,'rData':[],'rMsg':'Vui lòng nhập mã ID chức vụ (jplevelID)'}
    


    # print(jplevelID)
    # return False
# @app.post("/Đăng ký ngày nghỉ phép",tags=['test'])

@app.put('/update-jplevel',tags=['JobTitle'],summary='cập nhật chức vự')
async def update_jplevel(form:Update_position):
    s = f'''select * from JPLevel where JPLevelID = {form.jplevelID}'''
    query = fn.get_data(s)
    print(query)
    if len(query)>0:
        name = query[0][1]
        if len(form.name)>0:
            is_alpha_numeric = all(c.isalnum() 
                or unicodedata.category(c) == 'Zs' 
                or unicodedata.category(c) == 'Ll'
                or unicodedata.category(c) == 'Lu' 
                or unicodedata.category(c) == 'Lt' 
                or unicodedata.category(c) == 'Pd'  
                for c in form.name)
            if is_alpha_numeric:
                remove_blank = form.name.strip(' ')
                name = re.sub("\s+", " ", remove_blank)
            else:
                return {'rCode':0,'rData':{},'rMsg':'tên chức vụ không được phép'}
                # pJplevel = 'NULL'
                # if form.pJPlevel != 0:
                #     pJplevel = 'NULL'
        note = query[0][4]
        if len(form.note) > 0:
            note_blank = form.note.strip(' ') 
            note = re.sub("\s+", " ", note_blank)
        status = 0
        if form.status != 0:
            status = 1
        
        s = f'''update JPLevel set Name = N'{name}',Status = {status},pJPLevel = NULL,Note = N'{note}'
                where JPLevelID = {form.jplevelID}'''
        fn.commit_data(s)
        return {'rCode':1,'rData':{},'rMsg':'cập nhật chức danh thành công'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'ID cấp độ vị trí công việc không tồn tại (JPlevelID)'}

@app.delete('/delete-jplevel',tags=['JobTitle'],summary='xóa chức danh')
async def delete_jplevel(jplevelID: int,state: int = 0):
    s = f'''select * from jplevel where JPLevelID = {jplevelID}'''
    query = fn.get_data(s)
    print(len(query))
    if len(query) > 0:
        if state == 1:
            s = f'''delete JPLevel where JPLevelID = {jplevelID}'''
            # fn.commit_data(s)
            return {'rCode': 1,'rData':{},'rMsg':'Xóa thành công'}
        else:
            return {'rCode':0,'rData':{},'rMsg': 'cancel thao tác xóa'}
    else:
        return {'rCode': 0,'rData':{},'rMsg':'Mã chức danh không tồn tại'}


@app.get('/get-jobPosition',tags=['JobPosition'],summary='lấy danh sách vị trí công việc')
async def get_jobPosition():
    s = f'''select * from JobPosition'''
    query = fn.get_data(s,1)
    if len(query)>0:
        return {'rCode':1,'rData': query,'rMsg':'lấy danh sách vị trí công việc thành công'}
    
@app.get('/get-JPname',tags=['JobPosition'],summary='lấy danh sách tên công việc')
async def get_jpname():
    s = f'''select * from JPName'''
    query = fn.get_data(s,1)
    if len(query)>0:
        return {'rCode':1,'rData': query,'rMsg':'lấy danh sách tên công việc thành công'}

    #--------------------------------Sửa lại---------------------------------------------------------
@app.post('/import-jobPosition',tags=['JobPosition'],summary='thêm vị trí công việc')
async def import_jobPosition(form: Import_JobPosition):
    # if len(form.name)>0:
        # is_alpha_numeric = all(c.isalnum() 
        #     or unicodedata.category(c) == 'Zs' 
        #     or unicodedata.category(c) == 'Ll'
        #     or unicodedata.category(c) == 'Lu' 
        #     or unicodedata.category(c) == 'Lt' 
        #     or unicodedata.category(c) == 'Pd'
        #     for c in form.name)
        # if is_alpha_numeric:
            # remove_blank = form.name.strip(' ')
            # name = re.sub("\s+", " ", remove_blank)
    #-----------------------------------------------------------------------------------------
            # s = f'''select * from JPLevel'''
            # query = fn.get_data(s,1)
            # name_jplevel = 1 
            # for i in query:
            #     if form.jplevel == i['JPLevelID']:
            #         name_jplevel = i['Name']
            # if name_jplevel == 1:
            #     return {'rCode':0,'rData':{},'rMsg':'mã chức vụ không tồn tại'}
            
            s = f'''select * from JPLevel where JPLevelID = {form.jplevel}'''
            query = fn.get_data(s)
            if len(query)>0:
                name_jplevel = query[0][1]
                print(name_jplevel)
            else:  
                return {'rCode':0,'rData':{},'rMsg':'(jplevel) mã chức vụ không tồn tại'}
            
            
            # s1 = f'''select * from JPName'''
            # query1 = fn.get_data(s1,1)
            # name_jpName = 1
            # for i1 in query1:
            #     if form.jpname == i1['JPNameID']:
            #         name_jpName = i1['Name']
            # if name_jpName == 1:
            #     return {'rCode': 0,'rData':{},'rMsg':'mã tên vị trí công việc không tồn tại'}

            s1 = f'''select * from JPName where JPNameID = {form.jpname}'''
            query1 = fn.get_data(s1)
            if len(query1)>0:
                name_jpname = query1[0][1]
                print(name_jpname)
            else:
                return {'rCode': 0,'rData':{},'rMsg':'(JPNameID) mã tên vị trí công việc không tồn tại'}
            
            # s2 = f'''select * from Department'''
            # query2 = fn.get_data(s2,1)
            # name_deptID = 1
            # for i2 in query2:
            #     if form.deptID == i2['DeptID']:
            #         name_deptID = i2['Name']
            #         s3 = f''''''

            # return {'rCode':0,'rData':{},'rMsg':'ID phòng ban không tồn tại'}

            s2 = f'''select * from Department where DeptID = '{form.deptID}' '''
            query2 = fn.get_data(s2)
            if len(query2)>0:
                name_deptID = query2[0][1]
                print(name_deptID)
                s3 = f'''select * from DeptLevel where DLvlCode = {query2[0][2]}'''
                query3 = fn.get_data(s3)
                if len(query3)>0:
                    name_deptlevel = query3[0][1]
                    print(name_deptlevel)
                else:
                    return {'rCode': 0,'rData':{},'rMsg':'(deptlevel) mã cấp độ phòng ban không tồn tại'}
            else:
                return {'rCode': 0,'rData':{},'rMsg':'(deptID) mã phòng ban không tồn tại'}
            
            status = 0
            # if form.status != 0:
            #     status = 1
            note = ''
            if len(form.note)>0:
                note_blank = form.note.strip(' ') 
                note = re.sub("\s+", " ", note_blank)

           
            name = name_jplevel + ' ' + name_jpname + ' ' + name_deptlevel + ' ' + name_deptID
            print(name)
            s4 = f'''insert into JobPosition (Name,JPLevel,JPName,DeptID,Status,Note) 
                    values(N'{name}',{form.jplevel},{form.jpname},'{form.deptID}',{status},N'{note}') '''
            fn.commit_data(s4)

            return {'rCode':1,'rData':{'name': name, 'status':status},'rMsg':'thêm vị trí công việc thành công'}
        # else:
        #     return {'rCode':0,'rData':{},'rMsg':'tên vị trí công việc không hợp lệ'}
    # else:
    #     return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập tên vị trí công việc'}







@app.put('/update-jobPosition',tags=['JobPosition'],summary='cập nhật vị trí công việc')
async def update_jobPosition(form: Update_JobPosition):
    s = f'''select * from JobPosition where JobPosID = {form.jobPosID}'''
    result = fn.get_data(s)
    if len(result)>0:
        name = result[0][2]
        if len(form.name)>0:
            is_alpha_numeric = all(c.isalnum() 
                or unicodedata.category(c) == 'Zs' 
                or unicodedata.category(c) == 'Ll'
                or unicodedata.category(c) == 'Lu' 
                or unicodedata.category(c) == 'Lt' 
                or unicodedata.category(c) == 'Pd'
                for c in form.name)
            if is_alpha_numeric:
                remove_blank = form.name.strip(' ')
                name = re.sub("\s+", " ", remove_blank)
            else:
                return {'rCode':0,'rData':{},'rMsg':'tên vị trí công việc không hợp lệ'}
            
        jplevel = result[0][3]
        if form.jplevel is not None:
            s = f'''select * from JPLevel'''
            query = fn.get_data(s)
            jplevelID = []
            for i in query:
                jplevelID.append(i[0])
            if form.jplevel not in jplevelID:
                return {'rCode':0,'rData':{},'rMsg':'mã chức vụ không tồn tại'}
            else:
                jplevel = form.jplevel

        jpname = result[0][4]
        if form.jpname is not None:
            s1 = f'''select * from JPName'''
            query1 = fn.get_data(s1)
            jpNameID = []
            for i1 in query1:
                jpNameID.append(i1[0])
            if form.jpname not in jpNameID:
                return {'rCode':0,'rData':{},'rMsg':'ID tên vị trí công viêc không tồn tại'}
            else:
                jpname = form.jpname

        dept = result[0][5]
        if len(form.deptID)>0:
            s2 = f'''select * from Department'''
            query2 = fn.get_data(s2)
            deptID = []
            for i2 in query2:
                deptID.append(i2[0])
            if form.deptID not in deptID:
                return {'rCode':0,'rData':{},'rMsg':'ID phòng ban không tồn tại'}
            else:
                dept = form.deptID

        status = 0
        if form.status != 0:
            status = 1
        note = ''
        if len(form.note)>0:
            note_blank = form.note.strip(' ') 
            note = re.sub("\s+", " ", note_blank)
        s3 = f'''update JobPosition set Name=N'{name}',JPLevel = {jplevel},JPName = {jpname},DeptID = '{dept}',Status = {status},Note=N'{note}'
                where JobPosID = {form.jobPosID} '''
        fn.commit_data(s3)
        return {'rCode':1,'rData':{'status':status},'rMsg':'cập nhật vị trí công việc thành công'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'ID vị trí công việc không tồn tại'}


@app.delete('/delete-jobPosition',tags=['JobPosition'],summary='xóa vị trí làm việc')
async def delete_jobPosition(jobPosID: int = None, state: int = 0):
    s = f'''select * from JobPosition where JobPosID = {jobPosID}'''
    query = fn.get_data(s)
    if len(query)>0:
        if state == 1:
            s = f'''delete JobPosition where JobPosID = {jobPosID}'''
            return {'rCode':1,'rData':{},'rMsg':'xóa vị trí công việc thành công'}
        else:
            return {'rCode':0,'rData':{},'rMsg':'cancel thao tác hủy'}
    else:
        return {'rCode':0, 'rData':{},'rMsg':'vị trí công việc không tồn tại'}
# @app.post('/test')
# async def test(form: HRM.Tinhluong):
#     t = form.a + form.b
#     return t       

@app.get('/get-jpname',tags=['JobPosition'],summary='lấy danh sách tên công việc')
async def get_jpname():
    s= f'''select * from jpname'''
    query = fn.get_data(s,1)
    if len(query)>0:
        return {'rCode':0,'rData': query,'rMsg':'lấy danh sách thành công'}
    return {'rCode':1,'rData':{},'rMsg':'lấy danh sách thất bại'}









#------------viết update theo yêu cầu 1------------------------------------------------------------------------------------------------------

#chức năng thu hồi đơn,
@app.put('/recall',tags=['Recall'],summary='Thu hồi đơn nghĩ phép, với điều kiện đơn chưa duyệt',)
async def recall(regID:int = None,emplid: str = Depends(validate_token)):
    if regID:
        s = f'''select a.Approver,o.*,e.FirstName,e.LastName,e.ZoneID,e.DeptID,e.PosID from OffRegister o
                inner join Employee e on o.empID = e.empID
                left join Approval a on o.regID = a.regID
                where o.regID = {regID}'''
        query = fn.get_data(s)
        print(query)
        
        if len(query)>0:
            # if query[0][2]==emplid:
                if query[0][0]:#đơn đã được phê duyệt
                    return {'rCode':0,'rData':{},'rMsg':'Đơn đã được phê duyệt'}
                elif query[0][7]:# trường hợp đơn đã gửi
                    update = f'''update OffRegister set RegDate = Null where regID = {regID}'''
                    fn.commit_data(update)
                    return {'rCode':1,'rData':{},'rMsg':'Thu hồi đơn thành công'}
                else:#đơn chưa gửi
                    print(query[0][7])
                    return {'rCode':0,'rData':{},'rMsg':'Đơn chưa được gửi'}
            # return{'rCode':0,'rData':{},'rMsg':'Thu hồi đơn không thành công, mã nhân viên không hợp lệ'}
        return {'rCode':0,'rData':{},'rMsg':'Đơn không tồn tại'}
    return {'rCode':0,'rData':{},'rMsg':'Vui lòng truyền ID đơn nghĩ phép'}
    


# @app.post("/day-off-letter", tags=['OffRegister'],summary='đăng ký nghỉ phép - gửi mail',dependencies=[Depends(validate_token)])#,dependencies=[Depends(validate_token)]
async def offDayRegister(form: Offregister,emplid: str = Depends(validate_token)): #Done
    note = {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
    note1 = {'rCode': 0,'rMsg':'EmpID chưa được tạo Users'}
    offtypeId = []
    s = f'''SELECT OffTypeID FROM dbo.OffType'''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))
    if form.type in offtypeId:
        if form.period > 0:
            #if form.startdate >= datetime.date.today() + timedelta(days=2) and form.startdate.isoweekday() != 7: #isoweekday lấy số nguyên theo thứ trong tuần (7 là ngày chủ nhật)
            #trường hợp lưu lại: regdate = NULL #comment là trạng thái 0: lưu , 1: gửi đơn
            s = f'''select IDWorkingTIme from Employee where EmpID = {emplid}'''
            query = fn.get_data(s)
            print(query)
            if len(query)>0:
                endDate = form.startdate + timedelta(days=form.period-1) # lấy ngày kết thúc
                print(endDate)
                daysList =[] #lấy list ngày ngày nghĩ, để phân tích
                for i in range(0,form.period):
                    day=form.startdate + timedelta(days=i)
                    daysList.append(day)
                print(daysList)
                
                period = form.period
                if query[0][0] == 0:
                    print('123')
                    if form.period >= 7 and form.period <= 13:
                        period = form.period - 1
                    elif form.period >= 14:
                        return {'rCode':0,'rData':{},'rMsg':'Vui lòng liên hệ nhân sự'}
                elif query[0][0] == 2:
                    for e in daysList:
                        weekday = datetime.datetime.isoweekday(e)
                        if weekday == 7 or weekday == 6:#ngày chủ nhật hoặc thứ 7
                            period -= 1
                else: #query[0][0] == 1
                    for e in daysList:
                        weekday = datetime.datetime.isoweekday(e)
                        if weekday == 7:
                            period -= 1

                if period < 1:
                    return {'rCode':0,'rData':{},'rMsg':'Vui lòng chọn lại NGÀY nghĩ phép khác'}

                print(period)
                warning = []
                # warning_2 = []
                if period < 3:
                    if form.startdate < datetime.date.today() + timedelta(days=2):
                        warning = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
                elif period < 7:
                    if form.startdate < datetime.date.today() + timedelta(days=5):
                        warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 5 ngày cho lần sau']
                elif period >= 7:
                    if form.startdate < datetime.date.today() + timedelta(days=10):
                        warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 10 ngày cho lần sau']
                # if form.startdate.isoweekday() == 7:
                #     warning_2 = ['Ngày nghỉ phép là ngày chủ nhật']


                if form.command == 0:
                    c = 'NULL'
                    rMsg = ['Đơn đã lưu']
                    # email_notifi = ['Đơn chưa được gửi mail']
                elif form.command == 1:
                    c = 'SYSDATETIME()'
                    rMsg = ['Đơn đã gửi']
                    # email_notifi = []
                    if form.reason == "":
                        return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}  
                else:
                    return note
                #code cải tiến (viết lần 2)
                if fn.checkEmplIDUser(emplid):
                    s = f'''INSERT INTO dbo.OffRegister(EmpID,Type,Reason,Startdate,Period,RegDate,AnnualLeave,Address,EndDate) 
                        VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{period}',{c},0,N'{form.address}','{endDate}')''' 
                    fn.commit_data(s)
                    #gửi mail nếu như trạng thái gửi đơn là gửi
                    # if form.command == 1:
                    #     receiver_mails_manag = fn.get_receiver_email_manag(emplid)
                    
                    #     print(receiver_mails_manag)
                    #     if len(receiver_mails_manag)>0:
                    #         fn.sentMail(receiver_mails_manag,0)


                    if warning == []: #and warning_2 == []   and email_notifi == []
                        return {'rCode':1,'rMsg': rMsg,'rData':{'endDate':endDate, 'period':period}}
                    return {'rCode':1,'rMsg': rMsg,'rData':{'endDate':endDate, 'period':period},'rError':{'startdate': warning}}#+ warning_2, + email_notifi
                else:
                    return note1
            return {'rCode':0,'rData':{},'rMsg':'Mã nhân viên không hợp lệ'}
        return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
    return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID (loại phép)'}


#approve
# @app.post("/approve",tags=['Approve'],summary='Phê duyệt đơn')
async def approve(form: Approve,approver: str = Depends(validate_token)): #form: Approve
    # kiểm tra regID có tồn tại hay ko
    s = f"""
            select 
            CASE WHEN max(a.approrder) IS NULL THEN 0 ELSE max(a.apprOrder)   END as aOrder,o.Period from OffRegister o
            left join Approval a on o.regID = a.regID
            where o.regID = {form.regid} and o.RegDate is not null
            group by o.Period     
        """
    result = fn.get_data(s)
    
    #kiểm nếu có đơn thì kiểm tra duyệt chưa, không có đơn trả về lỗi
    if len(result)>0:
        # kiểm tra regID đã được phê duyệt chưa
        # s = f"""
        #         SELECT CASE WHEN max(apprOrder) IS NULL THEN 0   ELSE max(apprOrder)   END as aOrder 
        #         FROM dbo.Approval
        #         WHERE regID = '{form.regid}'      
        #     """
        # result = fn.get_data(s)
        
        aOrder = result[0][0]
        period = result[0][1]
        if aOrder == 0: #chưa phê duyệt
            aOrder += 1
            #lấy thông tin người approve
            s1 = f"""select e.PosID,j.JPLevel from Employee e inner join JobPosition j on e.PosID = j.JobPosID where EmpID = '{approver}' """
            query = fn.get_data(s1)
            if len(query)>0:
                jobposid = query[0][0]
                jplevel = query[0][1]
                r = {'rCode':0,'rData':{},'rMSg':'Bạn chưa được phân quyền phê duyệt theo quy định SỐ NGÀY NGHỈ CỦA ĐƠN'}
                if period < 3:
                    if jplevel > 50:
                        return r
                elif period >= 3 and period < 7:
                    if jplevel > 49:
                        return r
                elif period >= 7:
                    s2 = f"""select * from Employee where (DeptID = 'LOG' or DeptID = 'NS') and (PosID = 100 or PosID <= 91)"""
                    query2 = fn.get_data(s2)
                    if len(query2) <= 0:
                        Log_Ns = []
                        for i in query2:
                            Log_Ns.append(i)
                        if approver not in Log_Ns:
                            return r
                #------------------------------------------------------------------------------------
                if form.state != 1:
                    form.state = 0
                    if form.comment == '':
                        return {'rCode':0,'rMsg':'vui lòng nhập lý do phê duyệt'}
                
                s = f'''
                INSERT INTO dbo.Approval(regID,ApprOrder,Approver,JobPosID,adjType,adjStartDate,adjPeriod,Comment,ApprovalState,ApprovalDate)
                VALUES
                ('{form.regid}','{aOrder}','{approver}','{jobposid}',0,SYSDATETIME(),0,N'{form.comment}','{form.state}',SYSDATETIME())
                ''' 
                fn.commit_data(s)
                return {'rCode':1,'rData':{},'rMsg':'Phê duyệt thành công'}
            return{'rCode':0,'rData':{},'rMsg':'không xác định được vị trí công việc (jobposID) và chức vụ (jplevel) của người phê duyệt , phê duyệt không thành công'}
        return {'rCode':0,'rData':{},'rMsg':'Phê duyệt không thành công, đơn đã được phê duyệt trước đó'}
    return{'rCode':0,'rdata': {},'rMsg':'Regid không tồn tại'}

# @app.put("/adjust-day-off",tags=['OffRegister'],summary='Điều chỉnh đơn nghỉ phép')   
async def adjust(form: AdjustDayOff, emplid: int = Depends(validate_token)):
    offtypeId = []
    s = f'''SELECT OffTypeID FROM dbo.OffType'''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))
    s1 = f"""SELECT EmpID  FROM dbo.OffRegister WHERE regID = '{form.regid}' AND RegDate IS NULL"""
    result_1 = fn.get_data(s1)
    # if emplid == 
    if len(result_1) > 0:
        if int(emplid) == result_1[0][0]:
            if form.offtype in offtypeId:
                if form.period > 0:
                    s = f'''select IDWorkingTIme from Employee where EmpID = {emplid}'''
                    query = fn.get_data(s)
                    print(query)
                    if len(query)>0:
                        endDate = form.startdate + timedelta(days=form.period-1) # lấy ngày kết thúc
                        print(endDate)
                        
                        daysList = []
                        for i in range(0,form.period):
                            day=form.startdate + timedelta(days=i)
                            daysList.append(day)
                        print(daysList)

                        period = form.period		
                        if query[0][0] == 0:		
                            print('123')		
                            if form.period >= 7 and form.period <= 13:		
                                period = form.period - 1		
                            elif form.period >= 14:		
                                return {'rCode':0,'rData':{},'rMsg':'Vui lòng liên hệ nhân sự'}		
                        elif query[0][0] == 2:		
                            for e in daysList:		
                                weekday = datetime.datetime.isoweekday(e)		
                                if weekday == 7 or weekday == 6:#ngày chủ nhật hoặc thứ 7		
                                    period -= 1		
                        else: #query[0][0] == 1		
                            for e in daysList:		
                                weekday = datetime.datetime.isoweekday(e)		
                                if weekday == 7:		
                                    period -= 1		
                        if period<1:
                            return {'rCode':0,'rData':{},'rMsg':'Vui lòng chọn lại NGÀY nghĩ phép khác'}

                        print(period)
                        warning = []
                        # warning_2 = []


                        if period < 3:
                            if form.startdate < datetime.date.today() + timedelta(days=2):
                                warning = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
                        elif period < 7:
                            if form.startdate < datetime.date.today() + timedelta(days=5):
                                warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 5 ngày cho lần sau']
                        elif period >= 7:
                            if form.startdate < datetime.date.today() + timedelta(days=10):
                                warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 10 ngày cho lần sau']
                        # if form.startdate.isoweekday() == 7:
                        #     warning_2 = ['Ngày nghĩ phép là ngày chủ nhật']
                        if form.command == 0:
                            c = 'NULL'
                            rMsg = ['Chỉnh sửa đơn thành công, đơn đã được lưu']
                            # email_notifi = ['Đơn chưa được gửi mail']
                        elif form.command == 1:
                            c = 'SYSDATETIME()'
                            rMsg = ['Chỉnh sửa đơn thành công, đơn đã được gửi']
                            # email_notifi = []
                            if form.reason == "":
                                return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}
                        else:
                            return {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
                        s = f'''UPDATE dbo.OffRegister 
                                SET Type = '{form.offtype}', Reason = N'{form.reason}',StartDate = '{form.startdate}',Period = '{period}',RegDate = {c},Address = N'{form.address},EndDate = '{endDate}'
                                WHERE regID = {form.regid}''' 
                        fn.commit_data(s)
                        #gửi mail nếu như đã phê duyệt đồng ý
                        # if form.command == 1:
                        #     receiver_mails_manag = fn.get_receiver_email_manag(emplid)
                        #     print(receiver_mails_manag)
                        #     if len(receiver_mails_manag)>0:
                        #         fn.sentMail(receiver_mails_manag,0)
                        if warning == []: #and warning_2 == []  and email_notifi == []
                            # return {'rCode':1,'rMsg': rMsg}
                            return {'rCode':1,'rMsg': rMsg,'rData':{'endDate':endDate, 'period':period}}
                        # return {'rCode':1,'rMsg': rMsg + email_notifi,'rError':{'startdate': warning}}# + warning_2
                        return {'rCode':1,'rMsg': rMsg,'rData':{'endDate':endDate, 'period':period},'rError':{'startdate': warning}}#+ warning_2  + email_notifi
                    
                    return{'rCode':0,'rData':{},'rMsg':'Mã nhân viên không tồn tại'}
                return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
            return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID'}
        return {'rCode':0, 'rData': {},'rMsg':'Bạn không được điều chỉnh đơn'}
    return {'rCode':0,'rData':{},'rMsg':'regId không tồn tại hoặc regId đã gửi đơn'}



#-------------------------viết theo yêu cầu 2---------------------------------------------------------------------------

# @app.post("/day-off-letter", tags=['OffRegister'],summary='đăng ký nghỉ phép, tham số emplID: mã nhân viên được đăng ký nghỉ phép hộ, nếu không có thì đăng ký theo emplID token',dependencies=[Depends(validate_token)])#,dependencies=[Depends(validate_token)]
async def offDayRegister(form: Offregister,emplid: str = Depends(validate_token)): #Done
    note = {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
    # note1 = {'rCode': 0,'rMsg':'EmpID chưa được tạo Users'}
    offtypeId = []
    s = f'''SELECT OffTypeID FROM dbo.OffType'''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))
    if form.type in offtypeId:
        if form.period > 0:
            #if form.startdate >= datetime.date.today() + timedelta(days=2) and form.startdate.isoweekday() != 7: #isoweekday lấy số nguyên theo thứ trong tuần (7 là ngày chủ nhật)
            #trường hợp lưu lại: regdate = NULL #comment là trạng thái 0: lưu , 1: gửi đơn
            #---------------------------------------------------------------------------------------------------
            s = f'''select e.IDWorkingTIme,j.JPLevel,e.DeptID from Employee e 
                    inner join jobposition j on e.PosID = j.JobPosID
                    where e.EmpID = {emplid} and j.JPLevel <= 71'''
            query = fn.get_data(s)
            print(query)
                #------------------------------------------------------------------------------------------------
            if len(query)>0:
                jplevel_Manager = query[0][1]
                deptid_Manager = query[0][2]
                if form.otherRegis == 1:
                    if jplevel_Manager == 50:
                        s1 = f'''select e.IDWorkingTIme,j.JPLevel,e.DeptID from Employee e
                                inner join JobPosition j on e.PosID = j.JobPosID 
                                where j.JPLevel = 72 and e.EmpID = {form.emplid}'''
                        query = fn.get_data(s1)
                        if len(query)>0: #
                            if query[0][2] == deptid_Manager:
                                emplid = form.emplid
                            else:
                                return {'rCode':0,'rMsg':'Mã nhân viên được đăng ký nghỉ phép hộ, không cùng phòng ban(hoặc nhóm) với nhân viên điều chỉnh'}
                        else:
                            return {'rCode':0,'rMsg':'Mã nhân viên được đăng ký nghỉ phép hộ, không hợp lệ'}
                    else:
                        return {'rCode':0,'rMsg':'Bạn không được phân quyền đăng ký nghỉ phép hộ'}
                    
                
                #-------------------------------------------------------------------------------------------------
                endDate = form.startdate + timedelta(days=form.period-1) # lấy ngày kết thúc
                print(endDate)
                daysList =[] #lấy list ngày ngày nghĩ, để phân tích
                for i in range(0,form.period):
                    day=form.startdate + timedelta(days=i)
                    daysList.append(day)
                print(daysList)


                period = form.period
                if query[0][0] == 0:
                    print('123')
                    if form.period >= 7 and form.period <= 13:
                        period = form.period - 1
                    elif form.period >= 14:
                        return {'rCode':0,'rData':{},'rMsg':'Vui lòng liên hệ nhân sự'}
                elif query[0][0] == 2:
                    for e in daysList:
                        weekday = datetime.datetime.isoweekday(e)
                        if weekday == 7 or weekday == 6:#ngày chủ nhật hoặc thứ 7
                            period -= 1
                else: #query[0][0] == 1
                    for e in daysList:
                        weekday = datetime.datetime.isoweekday(e)
                        if weekday == 7:
                            period -= 1

                if period < 1:
                    return {'rCode':0,'rData':{},'rMsg':'Vui lòng chọn lại NGÀY nghĩ phép khác'}
                print(period)
                warning = []
                # warning_2 = []
                if period < 3:
                    if form.startdate < datetime.date.today() + timedelta(days=2):
                        warning = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
                elif period < 7:
                    if form.startdate < datetime.date.today() + timedelta(days=5):
                        warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 5 ngày cho lần sau']
                elif period >= 7:
                    if form.startdate < datetime.date.today() + timedelta(days=10):
                        warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 10 ngày cho lần sau']
                # if form.startdate.isoweekday() == 7:
                #     warning_2 = ['Ngày nghỉ phép là ngày chủ nhật']


                if form.command == 0:
                    c = 'NULL'
                    rMsg = ['Đơn đã lưu']
                    # email_notifi = ['Đơn chưa được gửi mail']
                elif form.command == 1:
                    c = 'SYSDATETIME()'
                    rMsg = ['Đơn đã gửi']
                    # email_notifi = []
                    if form.reason == "":
                        return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}  
                else:
                    return note
                #code cải tiến (viết lần 2)
                # if fn.checkEmplIDUser(emplid):
                s = f'''INSERT INTO dbo.OffRegister(EmpID,Type,Reason,Startdate,Period,RegDate,AnnualLeave,Address,EndDate) 
                    VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{period}',{c},0,N'{form.address}','{endDate}')''' 
                fn.commit_data(s)
                print(s)
                #gửi mail nếu như trạng thái gửi đơn là gửi
                # if form.command == 1:
                #     receiver_mails_manag = fn.get_receiver_email_manag(emplid)
                
                #     print(receiver_mails_manag)
                #     if len(receiver_mails_manag)>0:
                #         fn.sentMail(receiver_mails_manag,0)


                if warning == []: #and warning_2 == []   and email_notifi == []
                    return {'rCode':1,'rMsg': rMsg,'rData':{'endDate':endDate, 'period':period}}
                return {'rCode':1,'rMsg': rMsg,'rData':{'endDate':endDate, 'period':period},'rError':{'startdate': warning}}#+ warning_2, + email_notifi
                # else:
                #     return note1
                #---------------------------------------------------------------------------------------------------------------------
            return {'rCode':0,'rData':{},'rMsg':'Mã nhân viên không hợp lệ'}
        return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
    return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID (loại phép)'}



# @app.put("/adjust-day-off",tags=['OffRegister'],summary='Điều chỉnh đơn nghỉ phép')   
async def adjust(form: AdjustDayOff,emplid: int = Depends(validate_token)): #, emplid: int = Depends(validate_token)
    offtypeId = []
    s = f'''SELECT OffTypeID FROM dbo.OffType'''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))
    s = f"""SELECT  e.IDWorkingTIme,j.JPLevel,e.DeptID,o.regID,o.EmpID  FROM dbo.OffRegister o
            inner join Employee e on o.EmpID = e.EmpID
            inner join JobPosition j on e.PosID = j.JobPosID
            WHERE o.regID = {form.regid} AND RegDate IS NULL"""
    query = fn.get_data(s)
    
    if len(query) > 0:
        # if int(emplid) == result_1[0][0]:
            if form.offtype in offtypeId:
                if form.period > 0:
                    # s1 = f'''select j.JPLevel,e.DeptID from Employee e
                    #         inner join JobPosition j on e.PosID = j.JobPosID
                    #         where e.EmpID = {emplid}'''
                    # query1 = fn.get_data(s1)
                    
                    # if len(query1) <= 0:
                    #     return {'rCode':0,'rData':{},'rMsg':'token không hợp lệ'}
                    # if (query1[0][1] != query[0][2]):#emplid != query[0][4] and query1[0][0] != 50 and query[0][1] != 72
                    #     return {'rCode':0,'rData':{},'rMsg':'Điều chỉnh đơn không thành công'}
                    
                    #     if query[0][1] == 72 and query[0][0] == 50 and query[0][2] == query1[0][1]:

                        
                    #câu lệnh viết cho 2 trường hợp
                    # s = f'''select e.IDWorkingTIme,j.JPLevel,e.DeptID from Employee e 
                    # inner join jobposition j on e.PosID = j.JobPosID
                    # where e.EmpID = {result_1[0][0]} ''' #and j.JPLevel <= 71
                    # query = fn.get_data(s) 
                    # print(query)

                    # if len(query)>0:
                        # jplevel_Manager = query[0][1]
                        # deptid_Manager = query[0][2]
                        # if jplevel_Manager == 50:
                        #     if form.emplid:#lấy mã nhân viên đăng ký hộ
                        #         s1 = f'''select e.IDWorkingTIme,j.JPLevel,e.DeptID from Employee e 
                        #                 inner join JobPosition j on e.PosID = j.JobPosID 
                        #                 where j.JPLevel = 72 and e.EmpID = {form.emplid}'''
                        #         query = fn.get_data(s1)
                        #         if len(query)>0:
                        #             if form.emplid == result_1[0][0]: #so sánh emplID truyền vào và emplID của đơn 
                        #                 if query[0][2] != deptid_Manager:
                        #                     # emplid = form.emplid
                        #                     return {'rCode':0,'rMsg':'Mã nhân viên được điều chỉnh đơn nghỉ phép hộ, không cùng phòng ban(hoặc nhóm) với nhân viên điều chỉnh'}

                    endDate = form.startdate + timedelta(days=form.period-1) # lấy ngày kết thúc
                    print(endDate)
                    
                    daysList = []
                    for i in range(0,form.period):
                        day=form.startdate + timedelta(days=i)
                        daysList.append(day)
                    print(daysList)

                    period = form.period		
                    if query[0][0] == 0:		
                        print('123')		
                        if form.period >= 7 and form.period <= 13:		
                            period = form.period - 1		
                        elif form.period >= 14:		
                            return {'rCode':0,'rData':{},'rMsg':'Vui lòng liên hệ nhân sự'}		
                    elif query[0][0] == 2:		
                        for e in daysList:		
                            weekday = datetime.datetime.isoweekday(e)		
                            if weekday == 7 or weekday == 6:#ngày chủ nhật hoặc thứ 7		
                                period -= 1		
                    else: #query[0][0] == 1		
                        for e in daysList:		
                            weekday = datetime.datetime.isoweekday(e)		
                            if weekday == 7:		
                                period -= 1		
                    if period<1:
                        return {'rCode':0,'rData':{},'rMsg':'Vui lòng chọn lại NGÀY BẮT ĐẦU nghĩ phép khác'}
                    print(period)
                    warning = []
                    # warning_2 = []

                    if period < 3:
                        if form.startdate < datetime.date.today() + timedelta(days=2):
                            warning = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
                    elif period < 7:
                        if form.startdate < datetime.date.today() + timedelta(days=5):
                            warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 5 ngày cho lần sau']
                    elif period >= 7:
                        if form.startdate < datetime.date.today() + timedelta(days=10):
                            warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 10 ngày cho lần sau']
                    # if form.startdate.isoweekday() == 7:
                    #     warning_2 = ['Ngày nghĩ phép là ngày chủ nhật']
                    if form.command == 0:
                        c = 'NULL'
                        rMsg = ['Chỉnh sửa đơn thành công, đơn đã được lưu']
                        # email_notifi = ['Đơn chưa được gửi mail']
                    elif form.command == 1:
                        c = 'SYSDATETIME()'
                        rMsg = ['Chỉnh sửa đơn thành công, đơn đã được gửi']
                        # email_notifi = []
                        if form.reason == "":
                            return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}
                    else:
                        return {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
                    s = f'''UPDATE dbo.OffRegister 
                            SET Type = '{form.offtype}', Reason = N'{form.reason}',StartDate = '{form.startdate}',Period = {period},RegDate = {c},Address = N'{form.address}',EndDate = '{endDate}'
                            WHERE regID = {form.regid}''' 
                    a = fn.commit_data(s)
                    print(a)
                    #gửi mail nếu như đã phê duyệt đồng ý
                    # if form.command == 1:
                    #     receiver_mails_manag = fn.get_receiver_email_manag(emplid)
                    #     print(receiver_mails_manag)
                    #     if len(receiver_mails_manag)>0:
                    #         fn.sentMail(receiver_mails_manag,0)
                    if warning == []: #and warning_2 == []  and email_notifi == []
                        # return {'rCode':1,'rMsg': rMsg}
                        return {'rCode':1,'rMsg': rMsg,'rData':{'endDate':endDate, 'period':period}}
                    # return {'rCode':1,'rMsg': rMsg + email_notifi,'rError':{'startdate': warning}}# + warning_2
                    return {'rCode':1,'rMsg': rMsg,'rData':{'endDate':endDate, 'period':period},'rError':{'startdate': warning}}#+ warning_2  + email_notifi
                
                    
                return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
            return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID'}
        # return {'rCode':0, 'rData': {},'rMsg':'Bạn không được điều chỉnh đơn'}
    return {'rCode':0,'rData':{},'rMsg':'regId không tồn tại hoặc regId đã gửi đơn'}




#approve
@app.post("/approve",tags=['Approve'],summary='Phê duyệt đơn')
async def approve(form: Approve,approver: str = Depends(validate_token)): #form: Approve
    # kiểm tra regID có tồn tại hay ko
    s = f"""
            select 
            CASE WHEN max(a.approrder) IS NULL THEN 0 ELSE max(a.apprOrder)   END as aOrder,o.Period,e.PosID,j.JPLevel from OffRegister o
            left join Approval a on o.regID = a.regID
            inner join Employee e on o.EmpID = e.EmpID
            inner join JobPosition j on e.PosID = j.JobPosID
            where o.regID = {form.regid} and o.RegDate is not null
            group by o.Period,e.PosID,j.JPLevel    
        """
    result = fn.get_data(s)
    
    #kiểm nếu có đơn thì kiểm tra duyệt chưa, không có đơn trả về lỗi
    if len(result)>0:
        aOrder = result[0][0]
        period = result[0][1]
        jplevel_Regis = result[0][3]
        if aOrder == 0: #chưa phê duyệt
            aOrder += 1
            #lấy thông tin người approve
            s1 = f"""select e.PosID,j.JPLevel from Employee e inner join JobPosition j on e.PosID = j.JobPosID where EmpID = '{approver}' """
            query = fn.get_data(s1)
            if len(query)>0:
                jobposid_Approver = query[0][0]
                jplevel_Approver = query[0][1]

                r = {'rCode':0,'rData':{},'rMSg':'Bạn chưa được phân quyền phê duyệt (hoặc theo quy định SỐ NGÀY NGHỈ CỦA ĐƠN cần Giám Đốc điều hành phê duyệt)'}
                if jplevel_Approver > 49:
                    return r
                if period >= 3:
                    if jplevel_Regis < 50 and jplevel_Regis >= 41: #phó bộ phân nghĩ trên 3 ngày
                        if jplevel_Approver == 40: # từ cấp trưởng bộ phân không được duyệt
                            return r
                #------------------------------------------------------------------------------------
                if form.state != 1:
                    form.state = 0
                    if form.comment == '':
                        return {'rCode':0,'rMsg':'vui lòng nhập lý do phê duyệt'}
                
                s = f'''
                INSERT INTO dbo.Approval(regID,ApprOrder,Approver,JobPosID,adjType,adjStartDate,adjPeriod,Comment,ApprovalState,ApprovalDate)
                VALUES
                ('{form.regid}','{aOrder}','{approver}','{jobposid_Approver}',0,SYSDATETIME(),0,N'{form.comment}','{form.state}',SYSDATETIME())
                ''' 
                fn.commit_data(s)
                return {'rCode':1,'rData':{},'rMsg':'Phê duyệt thành công'}
            return{'rCode':0,'rData':{},'rMsg':'không xác định được vị trí công việc (jobposID) và chức vụ (jplevel) của người phê duyệt , phê duyệt không thành công'}
        #-------------------------------------------------------------------------
        return {'rCode':0,'rData':{},'rMsg':'Phê duyệt không thành công, đơn đã được phê duyệt trước đó'}
    return{'rCode':0,'rdata': {},'rMsg':'Regid không tồn tại'}


@app.put('/recall-approved-leave',tags=['Recall'],summary='Thu hồi đơn đã phê duyệt đồng ý')
async def recall_Approved(regid:int=None,approver:int = Depends(validate_token)):
    s = f'''select sum(approvalstate),Approver from Approval where regID = {regid} group by Approver'''
    result = fn.get_data(s)

    if len(result) <= 0:
        return{'rCode':0,'rMsg':'Đơn nghỉ phép chưa được phê duyệt duyệt hoặc không tồn tại'}

    if int(approver) != result[0][1]:
        return {'rCode':0,'rMsg':'Hủy đơn không thành công, Bạn không phải là người duyệt trước đó'}
    if result[0][0] == 1:
        s1 = f'''select j.JPLevel,e.PosID from Employee e inner join JobPosition j on e.PosID = j.JobPosID where e.EmpID ={approver}'''
        result1 = fn.get_data(s1)
        if len(result1)>0:
            if result1[0][0] < 50: #trườn hợp viết thêm có thể cancel
                # s = f'''update Approval set 
                #         ApprOrder = 2,Approver = {approver},JobPosID = {result1[0][1]},adjType = 0,adjStartDate = null,adjPeriod = 0,
                #         Comment = N'Đơn đã được hủy sau khi duyệt',ApprovalState = 2,ApprovalDate = SYSDATETIME()
                #         where regID = {regid}'''
                print()
                s2 = f'''insert into Approval(regID,ApprOrder,Approver,JobPosID,adjType,adjStartDate,adjPeriod,Comment,ApprovalState,ApprovalDate)
                        values({regid},2,{approver},{result1[0][1]},0,Null,0,N'Đơn đã được hủy sau khi duyệt',2,SYSDATETIME())'''
                
                print(s)
                fn.commit_data(s2)
                return {'rCode':1,'rMsg':'Đơn đã hủy thành công'}
            return {'rCode':0,'rMsg':'Đơn hủy không thành công, cấp bậc vị trí công việc của anh/chị không được phép Hủy'}
        return {'rCode':0,'rMsg':'Mã nhân viên từ token không tồn tại'}
    else:
        return{'rCode':0,'rMsg':'Đơn đã duyệt từ chối, hoặc đơn đã được hủy'}





#lấy danh sách nhân viên trực thuộc quản lý , với cấp leader hiện trường đăng phép hộ công nhân viên hiện trường
@app.get('/list-of-subordinates',tags=['GetEmpInfo'],summary='lấy danh sách nhân viên trực thuộc')
async def list_Subordinates(emplID:str = Depends(validate_token)):
    s = f'''select j.JPLevel,e.DeptID from Employee e
            inner join JobPosition j on e.PosID = j.JobPosID
            where e.EmpID = {emplID}'''
    query = fn.get_data(s)
    if len(query) <= 0:
        return {'rCode':0,'rMsg':'Mã nhân viên không tồn tại'}
    

    if query[0][0] != 50 and query[0][1] not in ('H01','H03','H05','H06','H07','HST'):
        return {'rCode':0,'rMsg':'Anh,chị chưa được phân quyền lấy danh sách nhân viên đăng ký phép hộ (nhân viên trực thuôc quản lý)'}
    # if query[0][0] == 50:
    s1 = f'''select e.*,j.Name,j.JPLevel from Employee e
            inner join JobPosition j on e.PosID = j.JobPosID
            where e.DeptID in
            (select DeptID from Employee where EmpID = {emplID}) and e.EmpID <> {emplID} and j.JPLevel > {query[0][0]}'''
    query1 = fn.get_data(s1,1)
    # elif query[0][0] in range(40,50):
    #     s1 =f'''select e.*,j.Name,j.JPLevel from Employee e
    #             inner join JobPosition j on e.PosID = j.JobPosID
    #             where e.DeptID in
    #             (select deptid from department
    #             where pdeptID = (select DeptID from Employee where EmpID = {emplID}))'''
    #     query1 = fn.get_data(s1,1)
    # else
    if len(query1)>0:
        return {'rCode':1,'rData':query1,'rMsg':'Lấy danh sách thành công'}
    else:
        return {'rCode':0,'rData':query1,'rMsg':'Không có danh sách nhân viên có sẳn'}
    


# @app.get('/day-off-total',summary='Lấy tổng số ngày nghĩ phép')
async def sum(date: datetime.date):
    # endDate = form.startdate + timedelta(days=form.period-1) # lấy ngày kết thúc
    #             print(endDate)
    #             daysList =[] #lấy list ngày ngày nghĩ, để phân tích
    #             for i in range(0,form.period):
    #                 day=form.startdate + timedelta(days=i)
    #                 daysList.append(day)
    #             print(daysList)

    m = date.month
    y = date.year
    print(m-1)
    #lấy đơn của tháng trước đã duyệt
    s = f'''select o.*,ot.Name from offregister o
            inner join OffType ot on o.Type = ot.OffTypeID
            where month(startdate) = {m-1} and year(startdate) = {y} and regid in
            (select regid from Approval --sum(approvalstate)
            group by regID
            having SUM(approvalstate) = 1)'''
    query = fn.get_data(s,1)
    # print(query)
    # print('--------------------------------------------------')
    regID_lastMonth = []
    # print('nhat')
    if len(query) > 0:
        index = 0
        for i in query:
            numberDays = 0
            # print(type(i['StartDate']))
            split_ = str(i['StartDate']).split(".")
            str_ = split_[0] 
            startdate = datetime.datetime.strptime(str_,"%Y-%m-%d %H:%M:%S") #.%f #%H:%M:%S
            endDate = startdate + timedelta(days=i['Period']-1)
            # print(endDate)
            if endDate.month == m: #nếu bằng tháng đơn đăng ký nghỉ ngày của tháng trước qua ngày của tháng sau
                s1 = f'''select IDWorkingTime from Employee where EmpID = {i['EmpID']}'''
                IDWorkingTime = fn.get_data(s1)
                if len(IDWorkingTime)<=0:
                    return{'rCode':0,'rMsg':'something went wrong, empID not found'}
                
                
                for x in range(0,i['Period']):
                    day = startdate + timedelta(days=x)
                    print(day)
                    if day.month == m:
                        numberDays += 1# lấy tổng ngày nghĩ ở nằm giữa 2 tháng


                        
                if IDWorkingTime[0][0] == 0:
                    if numberDays >= 7 and numberDays <= 13:
                        numberDays -= 1
                    elif numberDays >= 14:
                        numberDays -= 2
                elif IDWorkingTime[0][0] == 2:
                    for x in range(0,i['Period']):
                        day = startdate + timedelta(days=x)
                        if day.month == m:
                            weekday = datetime.datetime.isoweekday(day)
                            if weekday == 7 or weekday == 6:#ngày chủ nhật hoặc thứ 7
                                numberDays -= 1
                else: #query[0][0] == 1
                    for x in range(0,i['Period']):
                        day = startdate + timedelta(days=x)
                        if day.month == m:
                            weekday = datetime.datetime.isoweekday(day)
                            if weekday == 7:
                                numberDays -= 1
                i['Note'] = ''
                if numberDays > 0:
                    i['Period'] = numberDays
                    i['Note'] = f'Đơn nghỉ phép của tháng {m-1} có số ngày nghĩ qua tháng {m}'


            regID_lastMonth.append(i)
            index +=1 
                # print(numberDays)
                # print(regID_lastMonth)

    #-----Lấy đơn của tháng hiện tại--------------------------------------------------------------------------------------------
    s = f'''select o.*,ot.Name from offregister o
            inner join OffType ot on o.Type = ot.OffTypeID
            where month(startdate) = {m} and year(startdate) = {y} and regid in
            (select regid from Approval --sum(approvalstate)
            group by regID
            having SUM(approvalstate) = 1)'''
    
    query = fn.get_data(s,1)
    # print(query)

    if len(query)>0:
        index = 0
        for i in query:
            numberDays = 0
            split_ = str(i['StartDate']).split(".")
            str_ = split_[0]
            startdate = datetime.datetime.strptime(str_,"%Y-%m-%d %H:%M:%S")
            endDate = startdate + timedelta(days=i['Period']-1)

            if endDate.month == m +1:
                #-----------------------------------------------------------------------------------------------
                s1 = f'''select IDWorkingTime from Employee where EmpID = {i['EmpID']}'''
                IDWorkingTime = fn.get_data(s1)
                if len(IDWorkingTime)<=0:
                    return{'rCode':0,'rMsg':'something went wrong, empID not found'}
                
                period = fn.numberDays(startDate=startdate,endDate=endDate,emplID=i['EmpID'])

               #lấy số ngày nghỉ phép, trong 1 đơn có số ngày nằm trong 2 tháng (lấy tháng đang tính phép và loại trừ ngày nghĩ hằng tuần)
                for x in range(0,i['Period']):
                    day = startdate + timedelta(days=x)
                    if day.month == m:
                        numberDays += 1


                if IDWorkingTime[0][0] == 0:
                    if numberDays >= 7 and numberDays <= 13:
                        numberDays -= 1
                    elif numberDays >= 14:
                        numberDays -= 2

                elif IDWorkingTime[0][0] == 2:
                    for x in range(0,i['Period']):
                        day = startdate + timedelta(days=x)
                        if day.month == m:
                            weekday = datetime.datetime.isoweekday(day)
                            if weekday == 7 or weekday == 6:#ngày chủ nhật hoặc thứ 7
                                numberDays -= 1
                else: #query[0][0] == 1
                    for x in range(0,i['Period']):
                        day = startdate + timedelta(days=x)
                        if day.month == m:
                            weekday = datetime.datetime.isoweekday(day)
                            if weekday == 7:
                                numberDays -= 1
                     

                #-----------------------------------------------------------------------------
          
                # print(numberDays)
                query[index]['Note'] = ''
                if numberDays > 0:
                    # print('nhat')
                    query[index]['Period'] = numberDays
                    print(query[index]['Period'])
                    query[index]['Note'] = f'Đơn nghỉ phép của tháng {m}  có số ngày nghĩ qua tháng {m+1}'
            index +=1 
    # print(query)
        
   
            # regID_lastMonth.append(i)
    # print(regID_lastMonth)
        
    return query





#viết lại lần 3------------------------------------------------------------------------------------------------------------------------------
@app.get('/workingDays',tags=['OffRegister'],summary='Tính số ngày nghĩ của đơn nghĩ phép (có ngày bắt đầu và kết thúc)')
async def working_Days(emplID:int = None,startDate: datetime.date = None,endDate: datetime.date = None):
    period = fn.numberDays(emplID=emplID,startDate=startDate,endDate=endDate)
    # return fn.HTTP_RETURN(status_code=1,messange='Số ngày nghỉ phép của bạn',data=period)
    return period






@app.post("/day-off-letter", tags=['OffRegister'],summary='đăng ký nghỉ phép, tham số emplID: mã nhân viên được đăng ký nghỉ phép hộ, nếu không có thì đăng ký theo emplID token',dependencies=[Depends(validate_token)])#,dependencies=[Depends(validate_token)]
async def offDayRegister(form: Offregister,emplid: str = Depends(validate_token)): #Done
    note = {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
    # note1 = {'rCode': 0,'rMsg':'EmpID chưa được tạo Users'}
    offtypeId = []
    s = f'''SELECT OffTypeID FROM dbo.OffType'''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))
    if form.type not in offtypeId:
        return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID (loại phép)'}
    
    
    #trường hợp lưu lại: regdate = NULL #comment là trạng thái 0: lưu , 1: gửi đơn
    #---------------------------------------------------------------------------------------------------
    s = f'''select e.IDWorkingTIme,j.JPLevel,e.DeptID from Employee e 
            inner join jobposition j on e.PosID = j.JobPosID
            where e.EmpID = {emplid} and j.JPLevel <= 71'''
    query = fn.get_data(s)
    print(query)
    #------------------------------------------------------------------------------------------------
    if len(query)<=0:
        return {'rCode':0,'rData':{},'rMsg':'Mã nhân viên từ token không hợp lệ'}
    jplevel_Manager = query[0][1]
    deptid_Manager = query[0][2]
    createdBy = emplid #người tạo đơn lấy theo token
    if form.otherRegis == 1:
        if jplevel_Manager == 50:
            s1 = f'''select e.IDWorkingTIme,j.JPLevel,e.DeptID from Employee e
                    inner join JobPosition j on e.PosID = j.JobPosID 
                    where j.JPLevel = 72 and e.EmpID = {form.emplid}'''
            query = fn.get_data(s1)
            if len(query)>0: #
                if query[0][2] == deptid_Manager:
                    emplid = form.emplid
                else:
                    return {'rCode':0,'rMsg':'Mã nhân viên được đăng ký nghỉ phép hộ, không cùng phòng ban(hoặc nhóm) với nhân viên điều chỉnh'}
            else:
                return {'rCode':0,'rMsg':'Mã nhân viên được đăng ký nghỉ phép hộ, không hợp lệ'}
        else:
            return {'rCode':0,'rMsg':'Bạn không được phân quyền đăng ký nghỉ phép hộ'}
    #-------------------------------------------------------------------------------------------------
    # endDate = form.startdate + timedelta(days=form.period-1) # lấy ngày kết thúc

    result = fn.numberDays(emplID=emplid,startDate=form.startdate,endDate=form.endDate)
    if result['rData']:
        period = result['rData']['period']
    else:
        return result
    
    
    DaysList_Registered = [] # lấy tất cả các ngày đã đăng ký phép (đã được duyệt)
    regID_List = fn.daysList_Registered(emplid,form.startdate.month-1) + fn.daysList_Registered(emplid,form.startdate.month) #lấy sách đơn nghỉ phép regIDs
    if len(regID_List) >0:
        for row in regID_List:
            start_Date = row['StartDate']
            end_Date = row['EndDate']
            convert_startDate = datetime.datetime.date(datetime.datetime.strptime(start_Date[0:start_Date.find(" ")],"%Y-%m-%d"))
            convert_endDate = datetime.datetime.date(datetime.datetime.strptime(end_Date[0:end_Date.find(" ")],"%Y-%m-%d"))
            query = fn.numberDays(emplid,convert_startDate,convert_endDate)
            if query['rData']:
                # numberDays = query['rData']['period']
                regID_listDays = query['rData']['listDays'] #danh sach ngày nghỉ của 1 đơn
                # for e in regID_listDays:
                    # day = datetime.datetime.date(datetime.datetime.strptime(e[0:e.find(" ")],"%Y-%m-%d"))
                DaysList_Registered += regID_listDays
            else:
                return query

    print(DaysList_Registered)

    #lấy list ngày đăng ký nghỉ kiểm tra, có trùng với những ngày đã đăng ký trước đó không
    for e in result['rData']['listDays']:
        if e in DaysList_Registered:
            return {'rCode':0,'rMsg':'Ngày nghỉ phép của bạn đã tồn tại, vui lòng chọn lại ngày'}

    if period < 1:
        return {'rCode':0,'rData':{},'rMsg':'Vui lòng chọn lại NGÀY nghĩ phép khác'}
    print(period)
    warning = []
    # warning_2 = []
    if period < 3:
        if form.startdate < datetime.date.today() + timedelta(days=2):
            warning = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
    elif period < 7:
        if form.startdate < datetime.date.today() + timedelta(days=5):
            warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 5 ngày cho lần sau']
    elif period >= 7:
        if form.startdate < datetime.date.today() + timedelta(days=10):
            warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 10 ngày cho lần sau']
    # if form.startdate.isoweekday() == 7:
    #     warning_2 = ['Ngày nghỉ phép là ngày chủ nhật']


    if form.command == 0:
        c = 'NULL'
        rMsg = ['Đơn đã lưu']
        # email_notifi = ['Đơn chưa được gửi mail']
    elif form.command == 1:
        c = 'SYSDATETIME()'
        rMsg = ['Đơn đã gửi']
        # email_notifi = []
        if form.reason == "":
            return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}  
    else:
        return note
    #code cải tiến (viết lần 2)
    # if fn.checkEmplIDUser(emplid):
    s = f'''INSERT INTO dbo.OffRegister(EmpID,Type,Reason,Startdate,Period,RegDate,AnnualLeave,Address,EndDate,CreatedBy) 
        VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{period}',{c},0,N'{form.address}','{form.endDate}',{createdBy})''' 
    fn.commit_data(s)
    print(s)
    #gửi mail nếu như trạng thái gửi đơn là gửi
    # if form.command == 1:
    #     receiver_mails_manag = fn.get_receiver_email_manag(emplid)
    
    #     print(receiver_mails_manag)
    #     if len(receiver_mails_manag)>0:
    #         fn.sentMail(receiver_mails_manag,0)


    if warning == []: #and warning_2 == []   and email_notifi == []
        return {'rCode':1,'rMsg': rMsg,'rData':{'period':period}}
    return {'rCode':1,'rMsg': rMsg,'rData':{'period':period},'rError':{'startdate': warning}}#+ warning_2, + email_notifi

        
    
@app.put("/adjust-day-off",tags=['OffRegister'],summary='Điều chỉnh đơn nghỉ phép')   
async def adjust(form: AdjustDayOff,emplid: int = Depends(validate_token)): #, emplid: int = Depends(validate_token)
    offtypeId = []
    s = f'''SELECT OffTypeID FROM dbo.OffType'''
    result = fn.get_data(s)
    for row in result:
        offtypeId.append(int(row[0]))
    if form.offtype not in offtypeId:
        return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID'}
    
    s = f"""SELECT  e.IDWorkingTIme,j.JPLevel,e.DeptID,o.regID,o.EmpID  FROM dbo.OffRegister o
            inner join Employee e on o.EmpID = e.EmpID
            inner join JobPosition j on e.PosID = j.JobPosID
            WHERE o.regID = {form.regid} AND RegDate IS NULL"""
    query = fn.get_data(s)
    
    if len(query) <= 0:
        return {'rCode':0,'rData':{},'rMsg':'regId không tồn tại hoặc regId đã gửi đơn'}

    result = fn.numberDays(startDate=form.startdate,endDate=form.endDate,emplID=query[0][4])        
    if result['rData']:
        period = result['rData']['period']
    else:
        return result
    
    DaysList_Registered = [] # lấy tất cả các ngày đã đăng ký phép (đã được duyệt)
    regID_List = fn.daysList_Registered(query[0][4],form.startdate.month-1) + fn.daysList_Registered(query[0][4],form.startdate.month) #lấy sách đơn nghỉ phép regIDs
    if len(regID_List) >0:
        for row in regID_List:
            start_Date = row['StartDate']
            end_Date = row['EndDate']
            convert_startDate = datetime.datetime.date(datetime.datetime.strptime(start_Date[0:start_Date.find(" ")],"%Y-%m-%d"))
            convert_endDate = datetime.datetime.date(datetime.datetime.strptime(end_Date[0:end_Date.find(" ")],"%Y-%m-%d"))
            query = fn.numberDays(query[0][4],convert_startDate,convert_endDate)
            if query['rData']:
                # numberDays = query['rData']['period']
                regID_listDays = query['rData']['listDays'] #danh sach ngày nghỉ của 1 đơn
                # for e in regID_listDays:
                    # day = datetime.datetime.date(datetime.datetime.strptime(e[0:e.find(" ")],"%Y-%m-%d"))
                DaysList_Registered += regID_listDays
            else:
                return query

    print(DaysList_Registered)
    #lấy list ngày đăng ký nghỉ kiểm tra, có trùng với những ngày đã đăng ký trước đó không
    for e in result['rData']['listDays']:
        if e in DaysList_Registered:
            return {'rCode':0,'rMsg':'Ngày nghỉ phép của bạn đã tồn tại, vui lòng chọn lại ngày'}

    if period < 1:
        return {'rCode':0,'rData':{},'rMsg':'Vui lòng chọn lại NGÀY nghĩ phép khác'}
    print(period)
    

    warning = []
    # warning_2 = []
    if period < 3:
        if form.startdate < datetime.date.today() + timedelta(days=2):
            warning = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
    elif period < 7:
        if form.startdate < datetime.date.today() + timedelta(days=5):
            warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 5 ngày cho lần sau']
    elif period >= 7:
        if form.startdate < datetime.date.today() + timedelta(days=10):
            warning = ['Anh/chị vui lòng đăng ký ngày nghỉ phép trước 10 ngày cho lần sau']
    # if form.startdate.isoweekday() == 7:
    #     warning_2 = ['Ngày nghĩ phép là ngày chủ nhật']
    if form.command == 0:
        c = 'NULL'
        rMsg = ['Chỉnh sửa đơn thành công, đơn đã được lưu']
        # email_notifi = ['Đơn chưa được gửi mail']
    elif form.command == 1:
        c = 'SYSDATETIME()'
        rMsg = ['Chỉnh sửa đơn thành công, đơn đã được gửi']
        # email_notifi = []
        if form.reason == "":
            return {'rCode': 0,'rMsg':'Vui lòng nhập lý do nghĩ phép'}
    else:
        return {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
    s = f'''UPDATE dbo.OffRegister 
            SET Type = '{form.offtype}', Reason = N'{form.reason}',StartDate = '{form.startdate}',Period = {period},RegDate = {c},Address = N'{form.address}',EndDate = '{form.endDate}'
            WHERE regID = {form.regid}''' 
    fn.commit_data(s)
    # print(a)
    #gửi mail nếu như đã phê duyệt đồng ý
    # if form.command == 1:
    #     receiver_mails_manag = fn.get_receiver_email_manag(emplid)
    #     print(receiver_mails_manag)
    #     if len(receiver_mails_manag)>0:
    #         fn.sentMail(receiver_mails_manag,0)
    if warning == []: #and warning_2 == []  and email_notifi == []
        # return {'rCode':1,'rMsg': rMsg}
        return {'rCode':1,'rMsg': rMsg,'rData':{'period':period}}
    # return {'rCode':1,'rMsg': rMsg + email_notifi,'rError':{'startdate': warning}}# + warning_2
    return {'rCode':1,'rMsg': rMsg,'rData':{'period':period},'rError':{'startdate': warning}}#+ warning_2  + email_notifi
    
        
@app.get('/day-off-summary',tags=['statistics'],summary='Lấy tổng số ngày nghĩ phép')
async def sum(date: datetime.date,token: int = Depends(validate_token)):
    s = f'''select e.DeptID,j.JPLevel,e.EmpID,e.PosID from Employee e
            inner join JobPosition j on e.PosID = j.JobPosID
            where e.EmpID = {token}'''
    check = fn.get_data(s)
    print(check)
    if len(check)<=0:
        df = pd.DataFrame([{'rCode':0,'Msg':'Token không hợp lệ'}])
        df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
        return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx')
    if check[0][1]>50:
        if check[0][3] != 100:
            df = pd.DataFrame([{'rCode':0,'Msg':'Anh,chị không được phân quyền để lấy đơn nghỉ phép'}])
            df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
            return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx') 
    


    m = date.month
    y = date.year
    #lấy đơn của tháng trước đã duyệt
    query = fn.getDaysOff_Month(m-1,y,check[0][0])
    # print(query)
    regID_lastMonth = []
    if len(query) > 0:
        # index = 0
        for i in query:
            numberDays = 0
            # print(type(i['StartDate']))
            split_StartDate = str(i['StartDate']).split(".")
            str_StartDate = split_StartDate[0] 
            startdate = datetime.datetime.strptime(str_StartDate,"%Y-%m-%d %H:%M:%S") #.%f #%H:%M:%S
           
            split_EndDate = str(i['EndDate']).split(".")
            str_EndDate = split_EndDate[0]
            endDate = datetime.datetime.strptime(str_EndDate,"%Y-%m-%d %H:%M:%S")#hệ thống sqlserver lưu dang datetime2
            # print(endDate)
            result = fn.numberDays(startDate=startdate,endDate=endDate,emplID=i['EmpID'])#lấy số ngày nghĩ và list ngày
            if result['rData']:
                numberDays = result['rData']['period']
                listDays = result['rData']['listDays']
            else:
                df = pd.DataFrame([result])
                # return result
                df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
                return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx')
            i['Note'] = ''
            if endDate.month == m: #nếu đơn của tháng trước, có số ngày nghĩ nằm trong tháng hiện tại
                listDays_filter = []
                for e in listDays:
                    # day = datetime.datetime.strptime(e,"%Y-%m-%d")

                    if e.month != m:
                        numberDays -= 1
                    else:
                        listDays_filter.append(e)
                if numberDays > 0:
                    i['Period'] = numberDays
                    i['Note'] = f'Đơn nghỉ phép của tháng {m-1} có số ngày nghĩ qua tháng {m}'
                i['listDays'] = listDays_filter
                regID_lastMonth.append(i)
            # index +=1 

    #-----Lấy đơn của tháng hiện tại--------------------------------------------------------------------------------------------
    query = fn.getDaysOff_Month(m,y,check[0][0])
    regID_CurrentMonth = []
    if len(query)>0:
        index = 0
        for i in query:
            numberDays = 0
            # print(type(i['StartDate']))
            split_StartDate = str(i['StartDate']).split(".")
            str_StartDate = split_StartDate[0] 
            startdate = datetime.datetime.strptime(str_StartDate,"%Y-%m-%d %H:%M:%S") #.%f #%H:%M:%S
            split_EndDate = str(i['EndDate']).split(".")
            str_EndDate = split_EndDate[0]
            endDate = datetime.datetime.strptime(str_EndDate,"%Y-%m-%d %H:%M:%S")#hệ thống sqlserver lưu dang datetime2 --> chuyển định dạng của python
            # print(endDate)
            result = fn.numberDays(startDate=startdate,endDate=endDate,emplID=i['EmpID'])
            if result['rData']:
                numberDays = result['rData']['period']
                listDays = result['rData']['listDays']
            else:
                df = pd.DataFrame([result])
                df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
                return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx')
                # return result
            query[index]['Note'] = ''
            listDays_filter = listDays #gán biến trước điều kiện if, nếu if không thỏa thì lấy biến đã gán trước đó
            if endDate.month == m +1:
                # num = 0
                listDays_filter = []
                for e in listDays:
                    # day = datetime.datetime.strptime(e,"%Y-%m-%d")
                    if e.month == m + 1:
                        numberDays -= 1
                        # del listDays[num]
                    else:
                        listDays_filter.append(e)
                if numberDays > 0:
                    # print('nhat')
                    query[index]['Period'] = numberDays
                    # print(query[index]['Period'])
                    query[index]['Note'] = f'Đơn nghỉ phép của tháng {m}  có số ngày nghĩ qua tháng {m+1}'
            
            query[index]['listDays'] = listDays_filter
            index +=1
        regID_CurrentMonth = query
        
    total = regID_lastMonth + regID_CurrentMonth
    # print(total)
    
    if len(total) <= 0:
        df = pd.DataFrame([{'rCode':0,'rMsg':'Không có đơn nghỉ phép'}])
        df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
        return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx')
        # return {'rCode':0,'rMsg':'Không có đơn nghỉ phép'}
   
    sumPeriod_Type_EmplID = []
    list_key=[]
    for i in total:
        key = str(i['EmpID']) + '-' + i['OffTypeName']
        if key not in list_key:
            list_key.append(key)
            sumPeriod_Type_EmplID.append(i)
        else:
            num = 0
            for e in sumPeriod_Type_EmplID:
                if key == str(e['EmpID']) + '-' + e['OffTypeName']:
                    sumPeriod_Type_EmplID[num]['Period'] += i['Period']
                    sumPeriod_Type_EmplID[num]['listDays'] += i['listDays']
                num +=1

     #-------------------------------------------- lấy số ngày trong tháng ------------------------------
    # month = datetime.now().month
    # year = datetime.now().year
    day_In_Month = []
    number_of_days = calendar.monthrange(y, m)[1]
    firstDay = datetime.datetime.date(datetime.datetime(y,m,1))
    for i in range(0,number_of_days):
        day = firstDay + timedelta(days=i)
        day_In_Month.append(day)
    # print(day_In_Month)
    #----------------------------------------------------------------------------------------------------


    for i in sumPeriod_Type_EmplID: #chạy từng phần tử trong list chỉnh sửa, cuối cùng return list thêm dữ liệu
        for e in day_In_Month:
            i[e.day] = '' 
    

    # # layout = []
    # key = ''
    # # listKey = []
    # for i in sumPeriod_Type_EmplID:
    #     i[i['OffTypeName']] = i['Period']
    #     for e in i['listDays']:
    #         if e.day in i:
    #             i[e.day] = (i['OffTypeName'][0] + i['OffTypeName'][(i['OffTypeName'].find(" ") + 1)]).upper()
    #             # print(i)
    #     # key = i['EmpID']
    #     # if key not in listKey:
    #     #     listKey.append(key)


    layout = []
    key = ''
    listKey = []
    for i in sumPeriod_Type_EmplID:
        key = i['EmpID']
        if key not in listKey:
            listKey.append(key)
            i[i['OffTypeName']] = i['Period']
            for e in i['listDays']:
                if e.day in i:
                    i[e.day] = (i['OffTypeName'][0] + i['OffTypeName'][(i['OffTypeName'].find(" ") + 1)]).upper()
            layout.append(i)
        else:
            for x in layout:
                if key == x['EmpID']:
                    x[i['OffTypeName']] = i['Period']
                    for e in i['listDays']:
                        if e.day in x:
                            x[e.day] = (i['OffTypeName'][0] + i['OffTypeName'][(i['OffTypeName'].find(" ") + 1)]).upper()
            # print(layout)
  

    s1 = f"""SELECT Name FROM dbo.OffType"""
    result_query1 = fn.get_data(s1)
    # headers = []
    offtype = []
    for row in result_query1:
        offtype.append(row[0])
    for i in layout:
        for e in offtype:
            if e not in i:
                i[e] = ''
   
    # df = pd.DataFrame(total)
    df = pd.DataFrame(layout)
    del df['StartDate'],df['EndDate'],df['Period'],df['RegDate'],df['Address'],df['IDWorkingTime'],df['OffTypeName'],df['Note'],df['listDays']


    #--------------test-------------------
    #--------------kiểm tra lại từ đoạn này---------------------    
    # if len(total)>0:
    #     key = ''
    #     list_key=[]
    #     output_result = []
    #     for e in total:
    #         key = str(e['EmpID']) + '-' + str(e['OffTypeName'])
    #         # print(key)
            
    #         if key not in list_key:
    #             list_key.append(key)
    #             e[e['OffTypeName']] = e['Period']

    #             del e['OffTypeName'],e['Period'],e['StartDate'],e['EndDate'],e['RegDate'],e['Address'],e['IDWorkingTime'],e['Note']
    #             output_result.append(e)
    #     # print(output_result)
    #         else:
    #             number = 0
    #             for i in output_result:
    #                 if e['OffTypeName'] in i:
    #                     if key == str(i['EmpID']) + '-' + str(e['OffTypeName']):
    #                         output_result[number][e['OffTypeName']] += e['Period']
    #                 number += 1
    # else:
    #     return fn.HTTP_RETURN(status_code=0,messange='Không có đơn nghỉ phép')

    df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
    return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx')
    # print(output_result)
    # return output_result
    # return {'lastMonth':regID_lastMonth,'currentMonth':regID_CurrentMonth} 

  
  
    




#----------------------------------------------------------khu vực test--------------------------------------------------------------------------------------------------------------------------

# truy vấn
# @app.post("/hello")
# def index(formdata : CheckLogin,  db: Session = Depends(get_db)):

#     # print(formdata.username)
#     # print(formdata.password)
#     check = db.query(models.Users.UserName).all()
#     print(check)
#     return check

# chen du lieu
# @app.post("/insert")
# def chen(user,id,passw,email,db: Session = Depends(get_db)):
#     chen1 = models.Users(
#         UserName = user,
#         EmpID = id,
#         Password= passw,
#         # UserType= usertype,
#         Email = email,
#         # Status = status,
#         # LastModify = lastmodify,
#         # Modifier = modifier,
#         )
#     db.add(chen1)
#     kt = db.commit()

#     return "success"
# -------------------------------------------------------------------------------------------------------------
# Hiện token lên web
# @app.get('/')
async def home():
    return f"Đây là FastAPI token: {fn.generate_token('kieu.pham',30)}"

# @app.get('/',tags=['test'])
# async def test():
#     return f"Đây là FastAPI token: {fn.generate_token('1111111',30)}"

# lấy token
# @app.post("/getToken-kieu.pham-123", tags=['HRM'])
def getToken(formdata: CheckLogin):
    if fn.verify_password(username=formdata.username, password=formdata.password):
        return fn.generate_token(username=formdata.username, days=30) #days=30
    else:
        return {'rCode': 0,
                'msg': "sai userName hoặc Password"}


# tạo Username/Password theo form đầy đủ thông tin
# @app.post("/CreatedUser/password", tags=['HRM'])
def taouser(form: Created):
    if fn.checkuser(form.username) == False:
        if fn.checkEmplID(form.empID) == True:
            if fn.checkEmplIDUser(form.empID) == False:
                if fn.checkEmail(form.email) == False:

                    cursor = cn.cursor()
                    # s = f'''
                    #     insert into Users(UserName, EmpID, Password, Email ) values (?, ?, ?, ?)
                    #     '''
                    s = f'''
                        insert into Users(UserName, EmpID, Password, Email ) values ('{form.username}', '{form.empID}', '{fn.hashpw(form.password)}', '{form.email}')
                        '''

                    # cursor.execute(s,form.Username,form.EmpID,fn.hashpw(form.Password),form.Email)
                    # print('Nhat')
                    # print(s)
                    cursor.execute(s)

                    cn.commit()
                    return ('Đã tạo tài khoản')
                else:
                    return ('Mail đã tồn tại')

            else:
                return ('EmplID đã tồn tại trong Bảng users')

        else:
            return ('EmplID không thuộc danh sách')
    else:
        return ('Username đã tồn tại')

# lấy danh sách nhân viên
# @app.get('/dsNhanVien', dependencies=[Depends(validate_token)],tags=['HRM'])
async def dsChucDanh():
    s = f"""
                SELECT * FROM Employee
            """
    cursor = cn.cursor()
    rows = cursor.execute(s).fetchall()
    # print(rows)
    df = pd.DataFrame([tuple(t) for t in rows], columns=['EmpID', 'FirstName', 'LastName',
                      'ComeDate', 'ZoneID', 'DeptID', 'PosID', 'Gender', 'Tel', 'Status', 'DirectlyMng'])
    # print(df)
    return (df.to_dict('records'))     # trả về dạng json (bắt buộc)


# @app.post('/getEmplIDByUsername',dependencies=[Depends(validate_token)], tags=['HRM'])
async def getEmplIDByUser(form: Username):
    s = f"""
           SELECT EmpID FROM Users WHERE UserName = ?
            """
    cursor = cn.cursor()
    rows = cursor.execute(s, form.username).fetchall()
    if len(rows) > 0:
        return {'EmpID':rows[0][0]}
    else:
        return {'EmpID':'Không tìm thấy EmpID'}


# @app.post("/CheckUsername/EmpID", tags=['CreatedUser'])
async def CheckUsernameByEmpID(form: CheckUsername):
    if fn.checkEmplID(form.EmpID) == True:
        return {'EmpID tồn tại trong Employee'}
    else:
        return 'EmpID không tồn tại trong bảng Employee'

# def login ():
#     if checklogin(username, password):
#         return OK
#     else:
#         if(autoGen=1):
#             createAcount()
#         else:
#             return Error

# def checklogin:

# def createAcount:


# @app.post("/CreatedByEmpID", tags=['CreatedUser'])
async def createdByEmpID(form: CreatedByEmpID):
    if fn.checkEmplID(form.EmpID) == True:
        if fn.checkEmplIDUser(form.EmpID) == False:
            chuoi = string.ascii_letters + string.digits
            kq_chuoi = ''.join((random.choice(chuoi) for i in range(8)))
            cursor = cn.cursor()
            # s = f'''
            #     insert into Users(UserName, EmpID, Password, Email ) values (?, ?, ?, ?)
            #     '''
            # '{fn.hashpw(form.Password)}'
            s = f'''
                INSERT INTO dbo.Users(UserName,EmpID,Password,UserType,Email,Status,LastModify,Modifier) values ('{form.EmpID}','{form.EmpID}','{fn.hashpw(kq_chuoi)}',0,'{form.Gmail}',0,SYSDATETIME(),0) 
                ''' 
            # cursor.execute(s,form.Username,form.EmpID,fn.hashpw(form.Password),form.Email)

            cursor.execute(s)
            cn.commit()
            return {'password':kq_chuoi, 'Lưu ý':'anh/chị nhớ lưu lại password'}
        else:
            return 'EmpID đã tồn tại trong bảng User'   
    else:
        return {'statusCode': 0,
                'note':'EmpID không tồn tại trong bảng Employee'}


# @app.get('/getannualleave', tags=['OffRegister'])
async def getannualleave(empid: str = None): #Done
    if empid == None:
        return 'vui lòng nhập empid'
    elif empid.isnumeric() == False:
        return 'vui lòng nhập đúng mã empid'
    else:
        s = f"""
                SELECT AnnualLeave FROM AnnualLeave
                where EmpID = '{empid}'
                """
        cursor = cn.cursor()
        rows = cursor.execute(s).fetchall()
        if rows != []:
            df = pd.DataFrame([tuple(t) for t in rows], columns=[
                            'Ngày phép còn lại'])
            # print(df)
            return (df.to_dict('records')[0])
        else:
            return 'sai mã EmpID'

# @app.get("/day-off-letter",tags=['OffRegister'], summary="")
# no parametter: return emp info, no d-o-letter details người đang đăng nhập(có token)
# regID=xxx: return full(emp info + d-o-letter details) 
#           đảm bao regID la 1 trong những regID 
#              của người đang đăng nhập(có token) hoặc người đang đăng nhập(có token) có quyền phê duyệt
async def getlistOffByRegID(regid: None):
    s = f"""
            
                """
        
    cursor = cn.cursor()
    rows = cursor.execute(s).fetchall()
    results = []
    # columns = [column[0] for column in cursor.description]
    columns = [column[0] for column in cursor.description]
    columns[10]= 'regid2'
    print(cursor.description)
    for row in rows:
        results.append(dict(zip(columns, row)))
    return results


#-lấy đơn nghĩ phép theo mã nhân viên - (chưa có status: tạo mới, đã gửi, duyệt, chưa duyệt,...)
# @app.get("/day-off-letters", tags=['OffRegister'])
async def getlistoff(username: str = Depends(validate_token)):
        s = f"""
                SELECT o.*,a.* FROM dbo.OffRegister AS o
                LEFT JOIN dbo.Approval AS a ON a.regID = o.regID
                WHERE o.EmpID = '{username}'
                ORDER BY o.RegDate ASC
                """
        
        cursor = cn.cursor()
        rows = cursor.execute(s).fetchall()
    
        results = []
        # columns = [column[0] for column in cursor.description]
        columns = [column[0] for column in cursor.description]
        columns[10]= 'regid2'
        print(cursor.description)
        # print('nhat')
        # print(columns.count)
        for row in rows:
            results.append(dict(zip(columns, row)))
        # fs = pd.DataFrame(data=results,columns=columns)

        # fs["weqwe"] = 1 if fs["StartDate"] != None else 0
        # print(fs)
        return results
        # # df = pd.DataFrame([tuple(t) for t in rows], columns=[
        # #                   'regID','EmpID','Type','Reason','StartDate','Period','RegDate',
        # #                   'AnnualLeave','ApprovalID','regID2','ApprOrder','Approver','JobPosID',
        # #                   'adjType','adjStartDate','adjPeriod','Comment','ApprovalState','ApprovalDate'])   
    
 
# Cách 1 --------------------------
# @app.get("/votes", tags=['OffRegister'])
# async def votes(needAppr:int = None, username: str = Depends(validate_token)):
#     if needAppr == 1:
#         get_underMe()
#     else:
#         get_Mine()
# 
# def get_Mine():
#
# def get_underMe():
#
#Cách 2 --------------------------
# @app.get("/mine", tags=['OffRegister'])
# async def get_Mine():
#
# @app.get("/underMe", tags=['OffRegister'])
# async def get_underMe():
#



# lấy EmpID từ token
# @app.get('/getPosition', tags=['pending'])
async def getPosition(token: str = Depends(validate_token)):
    # print(token)
    return token

# @app.get('/get', tags=['pending'])
async def getlistOff():
    s = f"""
            SELECT * FROM OffRegister
            """
    cursor = cn.cursor()
    rows = cursor.execute(s).fetchall()
    df = pd.DataFrame([tuple(t) for t in rows], columns=[
                      'regID', 'EmpID', 'Type', 'Reason','StartDate','Period','RegDate','AnnualLeave'])
    # print(df)
    return (df.to_dict('records'))


#------------------------------------------------------------------------------------------------------------------------------
    # if regid == "": #nếu chưa phê duyệt thì....
    #     #lấy thông tin người nghĩ phép
    #     s = f"""
    #         select e.DeptID, p.JPLevel, d.pDeptID, e.EmpID from OffRegister o 
    #         join Employee e on o.EmpID = e.EmpID 
    #         join JobPosition p on e.PosID = p.JobPosID
    #         join Department d on d.DeptID = e.DeptID
    #         where o.regID=?       
    #         """
    #     cursor = cn.cursor()
    #     rows = cursor.execute(s,form.regid).fetchall() # rows trả về dạng list [], có nhiều dòng trong list

    #     for i in rows:
    #         deptid = i[0]
    #         jplevel = i[1]
    #         empid = i[3] #empid của người đăng ký nghĩ phép (sử dụng để lấy số ngày nghĩ phép hiện có)
    #     # rows empty => mã đơn ko tồn tại
    #     # rows length >= 1 => đon tồn tại => lấy dept ID, level, pdept
    #     #--------------------------------------------------------------------------------------------------
    #     s = f"""
    #         select e.EmpID, p.JPLevel,p.JobPosID from Employee e 
    #         join JobPosition p on e.PosID = p.JobPosID  
    #         where e.DeptID = '{deptid}' and p.JPLevel <= 50 -- lấy các cấp QL 
    #         and p.JPLevel < '{jplevel}' -- người duyệt là 1 trong nhưng người QL
    #         and e.EmpID = '{form.approver}'       
    #         """
    #     cursor = cn.cursor()
    #     dong = cursor.execute(s).fetchall() # rows trả về dạng list [], có nhiều dòng trong list
    #     if dong == []:
    #         return ('EmplID không thể duyệt đơn này')
    #     else:
    #         # #submit phê duyệt vào SQL
    #         dong1= dong[0] # lấy phần tử đầu tiên trong list trả về
    #         emplid = dong1[0]
    #         JobPosID = dong1[2]
    #         cursor = cn.cursor()
    #         s = f'''
    #             INSERT INTO dbo.Approval(regID,ApprOrder,Approver,JobPosID,adjType,adjStartDate,adjPeriod,Comment,ApprovalState,ApprovalDate)
    #             VALUES
    #             ('{form.regid}',1,'{emplid}','{JobPosID}',0,SYSDATETIME(),0,N'{form.comment}','{form.state}',SYSDATETIME())
    #             ''' 
    #         cursor.execute(s)   
    #         cn.commit()
    #         #---------------------------------------------------------------------------------------------------------------------
    #         # lấy số ngày nghĩ của nhân viên (số ngày đăng ký)
    #         s = f"""
    #                 SELECT Period FROM dbo.OffRegister
    #                 WHERE regID = '{form.regid}'
    #             """
    #         cursor = cn.cursor()
    #         rows = cursor.execute(s).fetchall()
    #         for i in rows:
    #             Period = i[0]

    #         #lấy số ngày nghĩ phép hiện có
    #         s = f"""
    #                 SELECT AnnualLeave FROM dbo.AnnualLeave
    #                 WHERE EmpID = '{empid}'
    #             """
    #         cursor = cn.cursor()
    #         rows = cursor.execute(s).fetchall()
    #         for i in rows:
    #             annual = i[0]
    #         songaynghiconlai = annual - Period
    #         print(songaynghiconlai)

    #         #update số ngày phép còn lại cho mã nhân viên đó
    #         s = f"""
    #                 UPDATE dbo.AnnualLeave SET AnnualLeave = '{songaynghiconlai}'
    #                 WHERE EmpID =  '{empid}'
    #             """
    #         cursor = cn.cursor()
    #         cursor.execute(s)
    #         cn.commit

    #         return('Đã phê duyệt thành công')
    # else:
    #     return('Đơn đã được phê duyệt trước đó')


    # -------------------------------------------------------------------------------------------------------------------------------------------
    # df = pd.DataFrame([tuple(t) for t in rows], columns=['Password'])
    # return (df.to_dict('dict'))     # trả về dạng json (bắt buộc)
    # --------------------------------------------------------------
    # a = db.query(models.Users).with_entities.filter(or_(models.Users.UserName==formdata.username,models.Users.EmpID==formdata.username)).first()
    # if a:
    #     return a
    # else:
    #     return 'User chưa được tạo'

    # --------------------------------------------------------
    # print(db.query(models.Users.UserName).where(models.Users==formdata.username).all())
    # print(formdata.username)
    # print(formdata.password)
    # check = db.query(models.Users.UserName).where(models.Users==formdata.username)
    # print(check)
    # return check
    #-----------------------------------------------------------------tham khảo code--------------------------------------------------------------
    # tìm đơn nghĩ phép theo regID
#@app.get("/day-off-letter",tags=['OffRegister'])
async def dayoffregID3(regid = None): #Done
    if str(regid).isnumeric():
        s = f"""
                SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.Type,
                    case 
                        when o.RegDate is null then 0 --N'chưa gửi' 
                        --đơn đó duyệt thì trường regdate phải có data
                        when sum(a.ApprovalState) is null then 1 --N'Chờ Duyệt' 
                        when sum(a.ApprovalState) = 1 then 2 --N'Đã Duyệt'
                        when sum(a.ApprovalState) = 0 then 3 --N'Từ Chối'
                        when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận'
                        when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
                    ELSE 'Error!' end as aStatus 
                FROM dbo.OffRegister o
                LEFT JOIN dbo.Approval a ON a.regID = o.regID
                WHERE o.regID = '{regid}'
                group by o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.type
                ORDER BY o.RegDate ASC  
                """
        result = fn.get_data(s,1)
        
        if len(result)>0:
            return {'rCode': 1,'rData':result[0],'rMsg':'Lấy đơn nghĩ phép thành công'}
        else:
            return {'rCode':0,'rMsg':'regid không tồn tại'}
    else:
        return {'rCode': 0,'rMsg': 'vui lòng nhập mã regID'}
   

# tìm đơn nghĩ phép theo regID viết lần 2
# @app.get("/day-off-letter1",tags=['OffRegister'])
async def dayoffregID1(regid = None):
    if str(regid).isnumeric():
        s = f'''
                SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,
                a.ApprOrder,a.Approver,a.JobPosID,a.Comment,a.ApprovalState,a.ApprovalDate,
				e.FirstName AS 'ApproverName',e.LastName AS 'ApproverLastName',e.DeptID AS 'ApproverDeptID',
				j.Name AS 'PositionName'
				 FROM dbo.OffRegister AS o
                LEFT JOIN dbo.Approval AS a ON a.regID = o.regID
				LEFT JOIN dbo.Employee AS e ON e.EmpID = a.Approver
				LEFT JOIN dbo.JobPosition AS j ON j.JobPosID = a.JobPosID
                WHERE o.regID = '{regid}'
                ORDER BY a.ApprOrder ASC
                '''
        result = fn.get_data(s,1)
        aStatus = {'aStatus':''}
        note = {'Note':''}
        rMsg = 'Lấy đơn thành công'
        list_kq = []
        # print(result)
        # print(len(result))
        if len(result) > 0:
            if result[0]['RegDate'] == None:    
                # aStatus = {'aStatus':0}
                aStatus['aStatus'] = 0
                note['Note'] = 'Đơn mới'
                concat_dict ={**result[0],**aStatus,**note} #nối nhiều cái dict ------------ # 
                return {'rCode': 1,'rData':concat_dict,'rMsg':rMsg}
            
            if result[0]['ApprovalState'] == None:
                aStatus['aStatus'] = 1
                note['Note'] = 'Chờ duyệt'
                concat_dict = {**result[0],**aStatus,**note}
                return {'rCode': 1,'rData':concat_dict,'rMsg':rMsg}
                
            for i in result:
                
                aStatus = {'aStatus':''}
                note = {'Note':''}
                if i['ApprOrder'] == 1:
                    aStatus['aStatus'] = 2
                    note['Note'] = 'Đã duyệt'
                    if i['ApprovalState'] == 0:
                        aStatus['aStatus'] = 3
                        note['Note'] = 'Từ chối'
                        concat_dict = {**i,**aStatus,**note}                      
                        return {'rCode': 1,'rData':concat_dict,'rMsg':rMsg}

                    concat_dict = {**i,**aStatus,**note}
                    
                if i['ApprOrder'] == 2:
                    aStatus = {'aStatus':4}
                    note = {'Note':'Nhân sự tiếp nhận'}
                    concat_dict = {**i,**aStatus,**note}
                if i['ApprOrder'] == 4:
                    aStatus = {'aStatus':5}
                    note = {'Note':'Giám đốc kiểm soát'}
                    concat_dict = {**i,**aStatus,**note}

                list_kq.append(concat_dict) #nối nhiều dict vào list 
            return {'rCode': 1,'rData':list_kq,'rMsg':rMsg}
        else:
            return {'rCode':0,'rData':{},'rMsg':'Đơn không tồn tại'}
                # return {'rCode': 1,'rData':concat_dict,'rMsg':rMsg}
    else:
        return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập regID'}

               


            



        # a = {"aaaa":"bbbbb"}
        
        # a['aaaa'] = 222
        
        # concat_dict = {**result[0],**a}
        
# tìm đơn nghĩ phép theo regID viết lần 3
# @app.get("/day-off-letter1",tags=['OffRegister'])
async def dayoffregID2(regid = None):
    apprInf = []
    if str(regid).isnumeric():
        s = f"""
                SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.Type,
                    case 
                        when o.RegDate is null then 0 --N'chưa gửi' 
                        --đơn đó duyệt thì trường regdate phải có data
                        when sum(a.ApprovalState) is null then 1 --N'Chờ Duyệt' 
                        when sum(a.ApprovalState) = 1 then 2 --N'Đã Duyệt'
                        when sum(a.ApprovalState) = 0 then 3 --N'Từ Chối'
                        when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận'
                        when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
                    ELSE 'Error!' end as aStatus 
                FROM dbo.OffRegister o
                LEFT JOIN dbo.Approval a ON a.regID = o.regID
                WHERE o.regID = '{regid}'
                group by o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.type
                """
        result = fn.get_data(s,1)
        # print(result[0]['aStatus'])
        # if result[0]['aStatus'] == 0:
        # if result[0]['aStatus'] == 1:
        if len(result)>0: # kết quả của câu truy vấn lần 1 lấy status (trường hợp có data)
            s1 = f"""
                        SELECT a.ApprovalID,a.regID,a.ApprOrder,a.Approver,a.JobPosID AS 'ApproJobposID',a.Comment,a.ApprovalState,a.ApprovalDate,
                        e.DeptID AS 'ApproDeptID',e.LastName AS 'ApproLastName',e.FirstName AS 'ApproFirstName',j.Name AS 'ApproJobName'
                        FROM dbo.Approval AS a
                        LEFT JOIN dbo.Employee AS e ON e.EmpID = a.Approver
                        LEFT JOIN dbo.JobPosition AS j ON j.JobPosID = a.JobPosID
                        WHERE regID = '{regid}'
                        ORDER BY a.ApprOrder ASC
                        """
            result_1 = fn.get_data(s1,1)
            for row in result_1: #result_1 kết quả truy vấn lần 2
                if result[0]['aStatus'] == 3: #result kết quả truy vấn ban đầu
                    row['aStatus'] = 3
                    row['Note'] = 'Từ chối'
                if result[0]['aStatus'] == 2:
                    row['aStatus'] = 2
                    row['Note'] = 'Đã duyệt'
                if result[0]['aStatus'] == 4:
                    if row['ApprOrder'] == 1:
                        row['aStatus'] = 2
                        row['Note'] = 'Đã duyệt'
                    elif row['ApprOrder'] == 2:
                        row['aStatus'] = 4
                        row['Note'] = 'Nhân Sự đã tiếp nhận'
                if result[0]['aStatus'] == 5:
                    if row['ApprOrder'] == 1:
                        row['aStatus'] = 2
                        row['Note'] = 'Đã duyệt'
                    elif row['ApprOrder'] == 2:
                        row['aStatus'] = 4
                        row['Note'] = 'Nhân Sự đã tiếp nhận'
                    elif row['ApprOrder'] == 4:
                        row['aStatus'] = 5
                        row['Note'] = 'Ban giám đốc kiểm soát'
                apprInf.append(row)
            
            result[0]['apprInf'] = apprInf


            return {'rCode': 1,'rData':result[0],'rMsg':'Lấy đơn thành công'}
       
    return {'rCode': 0,'rData':result[0],'rMsg':'Đơn không tồn tại'}

            # if result[0]['aStatus'] == 3: #từ chối
            #     result_1[0]['Note'] = 'từ chối'
            # if result[0]['aStatus'] == 2:
            #     result_1[0]['Note'] = 'Đã duyệt'
            # if result[0]['aStatus'] == 4:
            #     for row in result_1:
            #         row['note'] = 'Đã duyệt'

            
                



                # for row in result1:
                #     if row['ApprOrder'] == 1:

                #         row['sta'] = ''
                

# xuất file excel (số ngày PN còn lại, số ngày PN sử dụng trong tháng - số ngày phép việc riêng(bệnh ốm,thai sản,tai nạn,chờ việc,hiếu hỉ-tang lễ) sử dụng trong tháng ) của mỗi nhân viên
# @app.get("/summary",tags=['Plus'])
async def sum_OffType_employee():
    s = f'''
            SELECT e.EmpID,e.FirstName,e.LastName,e.ComeDate,e.Sex,
            j.Name as JobPositionName,
            a.AnnualLeave,
            d.Name AS departmentName,
            ot.Note,
            o.Type,o.Period,SUM(ap.ApprovalState) AS 'ApprovalState' --o.regID,o.RegDate,
            FROM dbo.Employee AS e
            LEFT JOIN dbo.JobPosition AS j ON j.JobPosID = e.PosID
            LEFT JOIN dbo.AnnualLeave AS a ON a.EmpID = e.EmpID
            LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
            INNER JOIN dbo.OffRegister AS o ON o.EmpID = e.EmpID
            INNER JOIN dbo.OffType AS ot ON ot.OffTypeID = o.Type
            INNER JOIN dbo.Approval AS ap ON ap.regID = o.regID
            WHERE ap.ApprovalState >= 1
            GROUP BY e.EmpID,e.FirstName,e.LastName,e.ComeDate,e.Sex,
                    j.Name,
                    a.AnnualLeave,
                    d.Name,
                    o.regID,o.RegDate,
                    ot.Note,
                    o.Type,o.Period
            ORDER BY o.Type,e.EmpID ASC
            '''
    query_result = fn.get_data(s,1)
  
    if len(query_result)>0:
        output_result = []
        list_key = []
        for row in query_result:
            # empid = row['EmpID']
            # offtype = row['Type']
            # # key = empid + "-" + offtype
            key = str(row['EmpID']) + "-" + row['Type']
            if key not in list_key:
                list_key.append(key)
                output_result.append(row)
                number = 0
                for i in output_result: #test
                    if i['AnnualLeave'] == None:#test
                        output_result[number]['AnnualLeave'] = 0 #test
                    number += 1 #test

            else:
                number = 0
                for i in output_result:
                    if str(i['EmpID']) + "-" + i['Type'] == key:
                        output_result[number]['Period'] = output_result[number]['Period'] + row['Period']
                    if i['AnnualLeave'] == None: #test
                        output_result[number]['AnnualLeave'] = 0 #test
                    number +=1
        print(len(output_result))
        df = pd.DataFrame(output_result)
        
        table = pd.pivot_table(df,values='Period',index=["EmpID","FirstName","LastName","ComeDate","departmentName","JobPositionName"],columns=["Note"],aggfunc=np.sum) #,"AnnualLeave"
        
        print(table)
        # table.to_excel(r'D:\data.xlsx')
        return {'rCode':1,'rData': {},'rMsg':'Tải file thành công'}
    else:
        return {'rCode': 0,'rData':{},'rMsg':'Không có đơn nghỉ phép'}
    

# @app.get("/get-period",tags=['Plus'])#response_class=FileResponse
async def sum_period():
    s = f'''
            SELECT empID,Firstname,LastName,ComeDate,JobPositionName,departmentName,[Bệnh Ốm],[Việc Riêng],[Phép Năm],[Thai Sản],[Tai Nạn]
            FROM
            (SELECT o.EmpID,ot.Name AS 'OffTypeName',SUM(o.Period) AS 'Period',
                        e.FirstName,e.LastName,FORMAT(e.ComeDate,'yyyy-MM-dd') AS ComeDate,
                        j.Name AS 'JobPositionName',
                        d.Name AS 'departmentName'
                FROM dbo.OffRegister o
                INNER JOIN dbo.Approval a ON a.regID = o.regID
                INNER JOIN dbo.OffType ot ON ot.OffTypeID = o.Type
                INNER JOIN dbo.Employee e ON e.EmpID = o.EmpID
                INNER JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                INNER JOIN dbo.Department d ON d.DeptID = e.DeptID
                WHERE a.ApprOrder = 1 AND a.ApprovalState = 1
                GROUP BY o.EmpID,o.Type,
                        ot.Name,
                        e.FirstName,e.LastName,e.DeptID,e.PosID,ComeDate,
                        j.Name,
                        d.Name) AS BangNguon
            PIVOT
            (
            SUM(Period)
            FOR OffTypeName IN ([Bệnh Ốm],[Việc Riêng],[Phép Năm],[Thai Sản],[Tai Nạn])
            ) AS BangPivot;    
            ''' 
    query_result = fn.get_data(s,1)
    print(query_result)
    df = pd.DataFrame(query_result)
    # df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
    print(df)
    # return FileResponse('file.xlsx',filename='Data.xlsx')
    return True

#viết lần 1 (lấy đơn theo status: tạo mới, đã gửi, duyệt, chưa duyệt,...)
# @app.post("/day-off-letters",tags=['OffRegister'],summary='truyền vào số 1: lấy đơn quản lý, còn lại: lấy đơn chính mình')
async def getsListoffstatus(form: Getlist,emplid: int = Depends(validate_token)): #, astatus: list = None,
# no parametter: lấy các d-o-letters của người đang đăng nhập(có token)     
# needAppr = 1:  lấy các d-o-letters cần người đang đăng nhập(có token) phê duyệt
    if form.needAppr == 1:
        s = f"""
                SELECT e.DeptID,j.JPLevel FROM dbo.Employee e
                LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                WHERE e.EmpID = '{emplid}'
                    """
        result = fn.get_data(s)
        for i in result:
            depid = i[0]
            jplevel = i[1]
        #lấy mã jplevel của TP,PP của phòng ban, trực thuộc quản lý  
        jplevel_TP_PP = ((int(jplevel/10)+1)*10)+9
        if jplevel <= 50:
            query = fn.depart_manager(emplid,jplevel_TP_PP) + fn.roommates(depid,jplevel)
            if len(form.astatus)>0:
                ketqua = [] #kết quả đầu ra
                for i in query:
                    if i['aStatus'] in form.astatus:#i['aStatus']: lấy value của key, kiểm tra xem có nằm trong list đầu vào không
                        ketqua.append(i)
                return {'rCode':1,'rData': ketqua,'rMsg': 'Lấy danh sách quản lý (filter astutus) thành công'}
            return {'rCode':1,'rData': query,'rMsg':'lấy danh sách quản lý (ALL) thành công'} 
        else:
            return{'rCode':0,'rData':[],'rMsg':''}  
    else:
        #lấy của chính mình
        query = fn.myself(emplid)#kết quả truy vấn
        if len(form.astatus)>0:
            ketqua= [] #kết quả đầu ra
            for i in query:
                if i['aStatus'] in form.astatus: #i['aStatus']: lấy value của key, kiểm tra xem có nằm trong list đầu vào không
                    ketqua.append(i) 
            return {'rCode':1,'rData': ketqua,'rMsg': 'Lấy danh sách myself (filter astutus) thành công'}
        return {'rCode':1,'rData': query,'rMsg': 'lấy danh sách myself (ALL) thành công'}

#hàm lấy đơn viết lần 1
# @app.get("/day-off-letters",tags=['OffRegister'],summary='truyền vào số 1: lấy đơn quản lý, còn lại: lấy đơn chính mình')
async def getsListoffstatus(needAppr: int = "",astatus:str = "",emplid: int = Depends(validate_token)): #, astatus: list = None,
# no parametter: lấy các d-o-letters của người đang đăng nhập(có token)     
# needAppr = 1:  lấy các d-o-letters cần người đang đăng nhập(có token) phê duyệt
    list_astatus = []
    if astatus != "":
        split_ = astatus.split(",") #tách phần tử --> trả về list
        for i in range(0, len(split_)):
            if split_[i].isnumeric(): # kiểm tra phẩn tử phải là số không
                list_astatus.append(int(split_[i]))
    if needAppr == 1:
        s = f"""
                SELECT e.DeptID,j.JPLevel FROM dbo.Employee e
                LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                WHERE e.EmpID = '{emplid}'
                    """
        result = fn.get_data(s)
        for i in result:
            depid = i[0]
            jplevel = i[1]
        #lấy mã jplevel của TP,PP của phòng ban, trực thuộc quản lý  
        jplevel_TP_PP = ((int(jplevel/10)+1)*10)+9
        if jplevel <= 50:
            query = fn.depart_manager(emplid,jplevel_TP_PP) + fn.roommates(depid,jplevel)
            if len(list_astatus)>0:
                ketqua = [] #kết quả đầu ra
                for i in query:
                    if i['aStatus'] in list_astatus:#i['aStatus']: lấy value của key, kiểm tra xem có nằm trong list đầu vào không
                        ketqua.append(i)
                return {'rCode':1,'rData': ketqua,'rMsg': 'Lấy danh sách quản lý (filter astutus) thành công'}
            return {'rCode':1,'rData': query,'rMsg':'lấy danh sách quản lý (ALL) thành công'} 
        else:
            return{'rCode':0,'rData':[],'rMsg':''}  
    elif needAppr == 0:
        #lấy của chính mình
        query = fn.myself(emplid)#kết quả truy vấn
        if len(list_astatus)>0:
            ketqua= [] #kết quả đầu ra
            for i in query:
                if i['aStatus'] in list_astatus: #i['aStatus']: lấy value của key, kiểm tra xem có nằm trong list đầu vào không
                    ketqua.append(i) 
            return {'rCode':1,'rData': ketqua,'rMsg': 'Lấy danh sách myself (filter astutus) thành công'}
        return {'rCode':1,'rData': query,'rMsg': 'lấy danh sách myself (ALL) thành công'}
    else:
        query = fn.depart_staff_manager(emplid)
        if len(list_astatus)>0:
            ketqua = []
            for i in query:
                if i['aStatus'] in list_astatus:
                    ketqua.append(i)
            return {'rCode':1, 'rData': ketqua,'rMsg': 'lấy danh sách nhân viên nghĩ phép (được chỉ định) thành công'}
        return {'rCode':1,'rData': query,'rMsg': 'lấy danh sách tất cả các đơn thành công'}