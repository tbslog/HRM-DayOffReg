from fastapi import Depends,HTTPException,status
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
from fastapi.middleware.cors import CORSMiddleware
from  projects.setting import  app
import random
import string, math
from pandas import DataFrame
from datetime import timedelta
import json


# ------------------------------------------------------------------------------------------------------------
cn = fn.cn




# @app.post("/dangnhapUsernamePass", tags=['HRM'], dependencies=[Depends(validate_token)])
@app.post("/Login", tags=['Login']) #done
def index(formdata: CheckLogin): 
    s = ''
    if formdata.username.isnumeric():
        s = f"""
                    SELECT top 1 EmpID, Password FROM Users WHERE EmpID = '{formdata.username}'
                """
    else:
        s = f"""
                    SELECT top 1 EmpID, Password FROM Users WHERE UserName = '{formdata.username}' 
                """
   
    result = fn.get_data(s)
    if len(result) > 0:
        # -- a Thái
        if (fn.check_pw(formdata.password,result[0][1])):
            return  {
                        'rCode': 3,
                        'rData':{'token':fn.generate_token(username=formdata.username,days=30),
                                'empid':result[0][0]},
                        'rMsg': 'Đăng nhập thành công'
                        }
        else:
            return {'rCode': 0,
                    'rMsg': 'Tài khoản hoặc mật khẩu không đúng'
                    }

        # -- a Thái
    elif len(result) == 0:
    
        
        if fn.checkEmplID(formdata.username) == True:
                
            if formdata.autogen == 1:
                    chuoi = string.ascii_letters + string.digits
                    kq_chuoi = ''.join((random.choice(chuoi) for i in range(8)))
                    s = f'''
                    INSERT INTO dbo.Users(UserName,EmpID,Password,UserType,Email,Status,LastModify,Modifier) values ('{formdata.username}','{formdata.username}','{fn.hashpw(kq_chuoi)}',0,'{formdata.username+"@tbslogistics.com"}',0,SYSDATETIME(),0) 
                    ''' 
                    fn.insert_data(s)
                    return {'rCode': 2,
                            'rData':{'token':fn.generate_token(username=formdata.username,days=30),'password':kq_chuoi},
                            'rMsg':'Anh/chị nhớ lưu lại password'
                            }
            else:
                return {'rCode' : 1, 'rMsg' : "Đăng nhập không thành công, EmpID tồn tại"}
        else:
            return {'rCode': 0,'rMsg': 'Đăng nhập không thành công'}

#đổi password
@app.post('/changePass',tags=['Login'])
async def change(form:ChangePass):
    s = ''
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
            if form.newPassword == form.confirmPass and form.newPassword != '':
                s = f"""
                    UPDATE dbo.Users SET Password = '{fn.hashpw(form.confirmPass)}'
                    WHERE EmpID = '{result[0][0]}'
                    """
                fn.insert_data(s)
                
                return {'rCode':1,'rMsg':'Thay đổi password thành công'}
            else:
                return{'rCode':0,'rMsg':'Xác nhận password không đúng hoặc password mới đang rỗng'}

    return {'rCode': 0,
            'rMsg': 'tài khoản hoặc mật khẩu không đúng'
            }



# getEmpInfo -lấy thông tin nhân viên
@app.get('/getEmpInfo',dependencies=[Depends(validate_token)], tags=['GetEmpInfo'])
async def getEmpInfo(empId: str = None,token: str = Depends(validate_token)): #Done
    note = {'statusCode': 0,'note': 'EmpID chưa được tạo Users'}
    note1 = {'statusCode': 0,'note':'Anh/Chị hãy nhập mã nhân viên'}
    if empId == None:
        if str(token).isnumeric(): #and len(str(EmpId)) > 0
            if fn.checkEmplIDUser(token) == True:
                s = f"""
                        SELECT U.UserName,U.Email,U.EmpID,U.Status,FORMAT(U.LastModify,'yyyy-MM-dd hh:mm:ss') AS lastModify,Emp.FirstName,Emp.LastName,Emp.ComeDate,Emp.ZoneID,Z.ZoneName,
                            jp.JobPosID,JPL.JPLevelID, DP.DeptID,AL.AnnualLeave,JP.Name,JPN.Name,JPL.Name,DP.Name FROM dbo.Users AS U
                            LEFT JOIN Employee AS Emp ON U.EmpID = Emp.EmpID 
                            LEFT JOIN dbo.Zone AS Z ON Emp.ZoneID = Z.ZoneID
                            LEFT JOIN dbo.JobPosition AS JP	ON Emp.PosID = JP.JobPosID
                            LEFT JOIN dbo.JPLevel AS JPL ON JP.JPLevel = JPL.JPLevelID
                            LEFT JOIN dbo.Department AS DP ON jp.DeptID = DP.DeptID
                            LEFT JOIN dbo.AnnualLeave AS AL ON Emp.EmpID = AL.EmpID
                            LEFT JOIN dbo.JPName AS JPN ON jp.JPName = JPN.JPNameID
                            WHERE U.EmpID = '{token}'
                        """
                result = fn.get_data(s)
                df = pd.DataFrame([tuple(t) for t in result], columns=[
                                'UserName', 'Email', 'EmpID', 'Status','LastModify','FirstName','LastName','ComeDate','ZoneID','ZoneName','JobPosID','JPLevelID',
                                'DeptID','AnnualLeave','JobpositionName','JPName','JPLevelName','DepartmentName'])
                return {'rCode':1,
                        'rData': df.to_dict('Records')[0], #trả về dữ liệu: Dict kiểu 'Records'
                        'rMsg': 'Lấy thông tin thành công'
                        }
            else:
                return note
        else:
            return note1
    elif str(empId).isnumeric():
        # if str(empId).isnumeric(): #and len(str(EmpId)) > 0
        if fn.checkEmplIDUser(empId) == True:
            s = f"""
                    SELECT U.UserName,U.Email,U.EmpID,U.Status,FORMAT(U.LastModify,'yyyy-MM-dd hh:mm:ss') AS lastModify,Emp.FirstName,Emp.LastName,Emp.ComeDate,Emp.ZoneID,Z.ZoneName,
                        jp.JobPosID,JPL.JPLevelID, DP.DeptID,AL.AnnualLeave,JP.Name,JPN.Name,JPL.Name,DP.Name FROM dbo.Users AS U
                        LEFT JOIN Employee AS Emp ON U.EmpID = Emp.EmpID 
                        LEFT JOIN dbo.Zone AS Z ON Emp.ZoneID = Z.ZoneID
                        LEFT JOIN dbo.JobPosition AS JP	ON Emp.PosID = JP.JobPosID
                        LEFT JOIN dbo.JPLevel AS JPL ON JP.JPLevel = JPL.JPLevelID
                        LEFT JOIN dbo.Department AS DP ON jp.DeptID = DP.DeptID
                        LEFT JOIN dbo.AnnualLeave AS AL ON Emp.EmpID = AL.EmpID
                        LEFT JOIN dbo.JPName AS JPN ON jp.JPName = JPN.JPNameID
                        WHERE U.EmpID = '{empId}'
                    """
            result = fn.get_data(s)
            df = pd.DataFrame([tuple(t) for t in result], columns=[
                            'UserName', 'Email', 'EmpID', 'Status','LastModify','FirstName','LastName','ComeDate','ZoneID','ZoneName','JobPosID','JPLevelID',
                            'DeptID','AnnualLeave','JobpositionName','JPName','JPLevelName','DepartmentName'])
            return {'rCode':1,
                    'rData': df.to_dict('Records')[0], #trả về dữ liệu: Dict kiểu 'Records'
                    'rMsg': 'Lấy thông tin thành công'
                    }
        else:
            return note
        # else:
        #     return note1
    else:
        return note1
        



# lấy list typyoff
@app.get("/dayOffType", tags=['OffRegister']) #dependencies=[Depends(validate_token)], 
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
@app.post("/day-off-letter", tags=['OffRegister'],dependencies=[Depends(validate_token)])
# async def offDayRegister(empID:int,type:int,reason:str,period:int,startDate:datetime.date | None = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y%m%d")):
async def offDayRegister(form: Offregister,emplid: str = Depends(validate_token)): #Done
    note = {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
    note1 = {'rCode': 0,'rMsg':'EmpID chưa được tạo Users'}
    offtypeId = [1,2,3,4,5,6]
    if form.type in offtypeId: 
        if form.period > 0:
            #if form.startdate >= datetime.date.today() + timedelta(days=2) and form.startdate.isoweekday() != 7: #isoweekday lấy số nguyên theo thứ trong tuần (7 là ngày chủ nhật)
            #trường hợp lưu lại: regdate = NULL #comment là trạng thái 0: lưu , 1: gửi đơn
            a = []
            b = []
            if form.startdate < datetime.date.today() + timedelta(days=2):
                a = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
            if form.startdate.isoweekday() == 7:
                b = ['Ngày nghĩ phép là ngày chủ nhật']

            if form.command == 0:
                c = 'NULL'
                d = 'Đơn đã lưu'
            elif form.command == 1:
                c = 'SYSDATETIME()'
                d = 'Đơn đã gửi'
            else:
                return note
            #code cải tiến (viết lần 2)
            if fn.checkEmplIDUser(emplid):
                s = f'''
                    INSERT INTO dbo.OffRegister(EmpID,Type,Reason,Startdate,Period,RegDate,AnnualLeave,Address) 
                    VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{form.period}',{c},0,N'{form.address}')           
                    ''' 
                fn.insert_data(s)
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
            #         fn.insert_data(s)
            #         return {'rCode':1,'rData':{},'rMsg':{'notification':'Đơn đã lưu','startdate':a + b}}
            #     else:
            #         return note1
            # #trường hợp gửi đơn: regdate = ngày đăng ký
            # elif form.command == 1:
            #     if fn.checkEmplIDUser(emplid):
            #         s = f'''
            #             INSERT INTO dbo.OffRegister(EmpID,Type,Reason,StartDate,Period,RegDate,AnnualLeave,Address) VALUES ('{emplid}','{form.type}',N'{form.reason}','{form.startdate}','{form.period}',SYSDATETIME(),0,'{form.address}')
            #             ''' 
            #         fn.insert_data(s)

            #         return {'rCode':1,'rData':{},'rMsg':{'notification':'Đơn đã gửi','startdate':a + b}}
            #     else:
            #         return note1
            # else:
            #     return note
        else:
            return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID'}


#(lấy đơn theo status: tạo mới, đã gửi, duyệt, chưa duyệt,...)
@app.post("/day-off-letters",tags=['OffRegister'],summary='truyền vào số 1: lấy đơn quản lý, còn lại: lấy đơn chính mình')
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

@app.post("/adjust-day-off",tags=['OffRegister'])   
async def adjust(form: AdjustDayOff):
    offtypeId = [1,2,3,4,5,6]
    s = f"""
            SELECT COUNT(*)  FROM dbo.OffRegister
            WHERE regID = '{form.regid}' AND RegDate IS NULL
        """
    result = fn.get_data(s)
    
    if result[0][0] > 0:
        if form.offtype in offtypeId:
            if form.period > 0:
                a = []
                b = []
                if form.startdate < datetime.date.today() + timedelta(days=2):
                    a = ['Vui lòng đăng ký ngày nghỉ phép trước 2 ngày cho lần sau']
                if form.startdate.isoweekday() == 7:
                    b = ['Ngày nghĩ phép là ngày chủ nhật']

                if form.command == 0:
                    c = 'NULL'
                    d = 'Đơn đã lưu'
                elif form.command == 1:
                    c = 'SYSDATETIME()'
                    d = 'Đơn đã gửi'
                else:
                    return {'rCode': 0,'rMsg':'anh chị vui lòng chọn lưu đơn (nhập số 0) hoặc gửi đơn (nhập số 1)'}
                 #----------------------------------------------------   

                s = f'''
                        UPDATE dbo.OffRegister 
                        SET Type = '{form.offtype}', Reason = N'{form.reason}',StartDate = '{form.startdate}',Period = '{form.period}',RegDate = {c},Address = N'{form.address}'
                        WHERE regID = {form.regid}	      
                    ''' 
                fn.insert_data(s)
                if a == [] and b == []:
                    return {'rCode':1,'rMsg': d}
                return {'rCode':1,'rMsg': d,'rError':{'startdate': a + b}}
            else:
                return {'rCode':0,'rData':{},'rMsg':'vui lòng nhập số ngày nghĩ'}
        else:
            return {'rCode':0,'rData':{},'rMsg':'chưa chọn typeID'}
    else:
        return {'rCode':0,'rData':{},'rMsg':'regId không tồn tại hoặc regId đã gửi đơn'}


        


    
# tìm đơn nghĩ phép theo regID
@app.get("/day-off-letter",tags=['OffRegister'])
async def dayoffregID(regid = None): #Done
    if str(regid).isnumeric():
        s = f"""
                SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address, 
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
                group by o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address
                ORDER BY o.RegDate ASC
                """
        result = fn.get_data(s,1)
        if len(result)>0:
            return {'rCode': 1,'rData':result[0],'rMsg':'Lấy đơn nghĩ phép thành công'}
        else:
            return {'rCode':0,'rMsg':'regid không tồn tại'}
    else:
        return {'rCode': 0,'rMsg': 'vui lòng nhập mã regID'}
   


# phê duyệt
@app.post("/approve",tags=['Approve'])
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
        print(aOrder)
        if aOrder == 0: #chưa phê duyệt
            aOrder += 1
            #lấy thông tin người approve
            s = f"""
                select PosID from Employee 
                where EmpID = '{approver}'
                """
            result = fn.get_data(s)

            jobposid = ''
            if len(result) >0:
                jobposid = result[0][0]
            
            
            if form.state != 0:
                form.state = 1
            
            s = f'''
            INSERT INTO dbo.Approval(regID,ApprOrder,Approver,JobPosID,adjType,adjStartDate,adjPeriod,Comment,ApprovalState,ApprovalDate)
            VALUES
            ('{form.regid}','{aOrder}','{approver}','{jobposid}',0,SYSDATETIME(),0,N'{form.comment}','{form.state}',SYSDATETIME())
            ''' 
            fn.insert_data(s)
            return {'rCode':1,'rData':{},'rMsg':'Phê duyệt thành công'}
        else:
            return {'rCode':0,'rData':{},'rMsg':'Phê duyệt không thành công, đơn đã được phê duyệt trước đó'}
    else:
        return{'rCode':0,'rdata': {},'rMsg':'Regid không tồn tại'}
   




    
        






   





#----------------------------------------------------------khu vực test--------------------------------------------------------------------

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
    if fn.checkuser(form.Username) == False:
        if fn.checkEmplID(form.EmpID) == True:
            if fn.checkEmplIDUser(form.EmpID) == False:
                if fn.checkEmail(form.Email) == False:

                    cursor = cn.cursor()
                    # s = f'''
                    #     insert into Users(UserName, EmpID, Password, Email ) values (?, ?, ?, ?)
                    #     '''
                    s = f'''
                        insert into Users(UserName, EmpID, Password, Email ) values ('{form.Username}', '{form.EmpID}', '{fn.hashpw(form.Password)}', '{form.Email}')
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