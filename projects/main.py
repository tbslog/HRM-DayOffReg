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
# cn = fn.cn
#thi văn nhât

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
@app.post('/changePass',tags=['Login'],summary='Thay đổi password')
async def change(form:ChangePass,username: str = Depends(validate_token)):
    if username.isnumeric():
        s = f"""SELECT top 1 EmpID, Password FROM Users WHERE EmpID = '{username}'"""
    else:
        s = f"""SELECT top 1 EmpID, Password FROM Users WHERE UserName = '{username}'"""
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
                            jp.JobPosID,JPL.JPLevelID, DP.DeptID,AL.AnnualLeave,JP.Name,JPN.Name,JPL.Name,DP.Name,Emp.EmpID FROM Employee AS Emp
                            LEFT JOIN dbo.Zone AS Z ON Emp.ZoneID = Z.ZoneID
                            LEFT JOIN dbo.JobPosition AS JP	ON Emp.PosID = JP.JobPosID
                            LEFT JOIN dbo.JPLevel AS JPL ON JP.JPLevel = JPL.JPLevelID
                            LEFT JOIN dbo.Department AS DP ON Emp.DeptID = DP.DeptID
                            LEFT JOIN dbo.AnnualLeave AS AL ON Emp.EmpID = AL.EmpID
                            LEFT JOIN dbo.JPName AS JPN ON jp.JPName = JPN.JPNameID
                            WHERE Emp.EmpID  = '{token}'
                        """
                result = fn.get_data(s)
                df = pd.DataFrame([tuple(t) for t in result], columns=[
                                'FirstName','LastName','ComeDate','ZoneID','ZoneName','JobPosID','JPLevelID',
                                'DeptID','AnnualLeave','JobpositionName','JPName','JPLevelName','DepartmentName','EmpID'])
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
                        jp.JobPosID,JPL.JPLevelID, DP.DeptID,AL.AnnualLeave,JP.Name,JPN.Name,JPL.Name,DP.Name,Emp.EmpID FROM Employee AS Emp

                        LEFT JOIN dbo.Zone AS Z ON Emp.ZoneID = Z.ZoneID
                        LEFT JOIN dbo.JobPosition AS JP	ON Emp.PosID = JP.JobPosID
                        LEFT JOIN dbo.JPLevel AS JPL ON JP.JPLevel = JPL.JPLevelID
                        LEFT JOIN dbo.Department AS DP ON Emp.DeptID = DP.DeptID
                        LEFT JOIN dbo.AnnualLeave AS AL ON Emp.EmpID = AL.EmpID
                        LEFT JOIN dbo.JPName AS JPN ON jp.JPName = JPN.JPNameID
                        WHERE Emp.EmpID = '{empId}'
                    """
            result = fn.get_data(s)
            df = pd.DataFrame([tuple(t) for t in result], columns=[
                            'FirstName','LastName','ComeDate','ZoneID','ZoneName','JobPosID','JPLevelID',
                            'DeptID','AnnualLeave','JobpositionName','JPName','JPLevelName','DepartmentName','EmpID'])
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





# tìm đơn nghĩ phép thep regID viết lần 4
@app.get("/day-off-letter",tags=['OffRegister'],summary='lấy đơn nghỉ phép theo regID (mã đơn)')
async def dayoffregID(regid = None):
    if str(regid).isnumeric():
        
        s = f"""
                SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.Type,o.EndDate,
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
                group by o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.type,o.EndDate,
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
    



#approve
@app.post("/approve",tags=['Approve'],summary='Phê duyệt đơn')
async def approve(form: Approve,approver: int = Depends(validate_token)): #form: Approve
    # kiểm tra regID có tồn tại hay ko
    s = f"""
            select 
            CASE WHEN max(a.approrder) IS NULL THEN 0 ELSE max(a.apprOrder)   END as aOrder,o.Period,e.PosID,j.JPLevel,e.DeptID from OffRegister o
            left join Approval a on o.regID = a.regID
            inner join Employee e on o.EmpID = e.EmpID
            inner join JobPosition j on e.PosID = j.JobPosID
            where o.regID = {form.regid} and o.RegDate is not null
            group by o.Period,e.PosID,j.JPLevel,e.DeptID    
        """
    result = fn.get_data(s)
    
    #kiểm nếu có đơn thì kiểm tra duyệt chưa, không có đơn trả về lỗi
    if len(result)>0:
        aOrder = result[0][0]
        period = result[0][1]
        jplevel_Regis = result[0][3]
        deptID_Regis = result[0][4] #chưa sử dụng
        if aOrder == 0: #chưa phê duyệt
            aOrder += 1
            #lấy thông tin người approve
            s1 = f"""select e.PosID,j.JPLevel,e.DeptID from Employee e inner join JobPosition j on e.PosID = j.JobPosID where EmpID = '{approver}' """
            query = fn.get_data(s1)
            if len(query)>0:
                jobposid_Approver = query[0][0]
                jplevel_Approver = query[0][1]
                deptID_Approver = query[0][2] #chưa sử dụng
                r = {'rCode':0,'rData':{},'rMSg':'Bạn chưa được phân quyền phê duyệt (hoặc theo quy định SỐ NGÀY NGHỈ CỦA ĐƠN cần Giám Đốc điều hành phê duyệt)'}
                if jplevel_Approver > 49:
                    if int(approver) not in fn.approvalOrder:
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
    
    r = {'rCode':0,'rMsg':'Anh,chị chưa được phân quyền lấy danh sách nhân viên đăng ký phép hộ (nhân viên trực thuôc quản lý)'}
    if query[0][0] != 50:#('VT','HST','BX_NM2','H05','BT','H03','H01','H07','H06','KST','BD','QTM','BCT'):#('H01','H03','H05','H06','H07','HST','BD','BT'):
        return r
    if query[0][1] not in fn.authorDeptRegis():
        return r
    # if query[0][0] == 50:
    s1 = f'''select e.*,j.Name,j.JPLevel from Employee e
            inner join JobPosition j on e.PosID = j.JobPosID
            where e.DeptID in
            (select DeptID from Employee where EmpID = {emplID}) and j.JPLevel > {query[0][0]}''' #and e.EmpID <> {emplID}
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
    







#viết lại lần 3------------------------------------------------------------------------------------------------------------------------------



#dang sử dụng trên server
@app.post("/day-off-letter", tags=['OffRegister'],summary='đăng ký nghỉ phép, tham số emplID: mã nhân viên được đăng ký nghỉ phép hộ, nếu không có thì đăng ký theo emplID token',dependencies=[Depends(validate_token)])#,dependencies=[Depends(validate_token)]
async def offDayRegister(form: Offregister,emplid: int = Depends(validate_token)): #Done
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
            where e.EmpID = {emplid} ''' #and j.JPLevel <= 71
    query = fn.get_data(s)
    print(query)
    #------------------------------------------------------------------------------------------------


    if len(query)<=0:
        return {'rCode':0,'rData':{},'rMsg':'Mã nhân viên từ token không hợp lệ'}
    jplevel_Manager = query[0][1]
    deptid_Manager = query[0][2]
    createdBy = emplid #người tạo đơn lấy theo token
    if form.emplid:
        if form.emplid != int(emplid):
            if jplevel_Manager == 50 and deptid_Manager in fn.authorDeptRegis():
                s1 = f'''select e.IDWorkingTIme,j.JPLevel,e.DeptID from Employee e
                        inner join JobPosition j on e.PosID = j.JobPosID 
                        where j.JPLevel >= 71 and e.EmpID = {form.emplid}'''
                query = fn.get_data(s1)
                if len(query)>0: #
                    if query[0][2] == deptid_Manager:
                        emplid = form.emplid
                    else:
                        return {'rCode':0,'rMsg':'Mã nhân viên được đăng ký nghỉ phép hộ, không cùng phòng ban(hoặc nhóm) với nhân viên đăng ký hộ'}
                else:
                    return {'rCode':0,'rMsg':'Mã nhân viên được đăng ký nghỉ phép hộ, không hợp lệ'}
            else:
                return {'rCode':0,'rMsg':'Bạn không được phân quyền đăng ký nghỉ phép hộ'}
    #-------------------------------------------------------------------------------------------------

    if form.period < 0.5:
        return {'rCode':0,'rData':{},'rMsg':'Vui lòng nhập số ngày nghĩ'}

    period = round(form.period*10/5,0)/2
    hour = period * 23.99
    startDate = datetime.datetime.combine(form.startdate,datetime.time())
    endDate = startDate + datetime.timedelta(hours=hour)
    
    # print(period)
    # print(endDate)

    r = {'rCode':0,'rMsg':'Ngày nghỉ phép của bạn đã tồn tại, vui lòng chọn lại ngày'}
    regID_List = fn.daysList_Registered(emplid,startDate.month-1) + fn.daysList_Registered(emplid,startDate.month) #lấy sách đơn nghỉ phép regIDs
    if len(regID_List) >0:
        for row in regID_List:
            start_Date = row['StartDate']
            end_Date = row['EndDate']
            convert_startDate = datetime.datetime.strptime(start_Date[0:start_Date.find(" ")],"%Y-%m-%d")
            convert_endDate = datetime.datetime.strptime(end_Date[0:end_Date.find(" ")],"%Y-%m-%d")
          
            if convert_startDate <= startDate <= convert_endDate:
                return r
            # if convert_startDate == endDate and convert_endDate:
            #     return r
            if convert_startDate <= startDate and endDate <= convert_endDate:
                return r
            if convert_startDate <= endDate <= convert_endDate:
                return r
 
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
        VALUES ('{emplid}','{form.type}',N'{form.reason}','{startDate}','{period}',{c},0,N'{form.address}','{endDate}',{createdBy})''' 
    fn.commit_data(s)
    print(s)
    #gửi mail nếu như trạng thái gửi đơn là gửi
    # if form.command == 1:
    #     receiver_mails_manag = fn.get_receiver_email_manag(emplid)
    
    #     print(receiver_mails_manag)
    #     if len(receiver_mails_manag)>0:
    #         fn.sentMail(receiver_mails_manag,0)


    if warning == []: #and warning_2 == []   and email_notifi == []
        return {'rCode':1,'rMsg': rMsg,'rData':{}}
    return {'rCode':1,'rMsg': rMsg,'rData':{},'rError':{'startdate': warning}}#+ warning_2, + email_notifi

        
    
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



    if form.period < 0.5:
        return {'rCode':0,'rData':{},'rMsg':'Vui lòng nhập số ngày nghĩ'}

    period = round(form.period*10/5,0)/2
    hour = period * 23.99
    startDate = datetime.datetime.combine(form.startdate,datetime.time())
    endDate = startDate + datetime.timedelta(hours=hour)

    r = {'rCode':0,'rMsg':'Ngày nghỉ phép của bạn đã tồn tại, vui lòng chọn lại ngày'}
    regID_List = fn.daysList_Registered(emplid,startDate.month-1) + fn.daysList_Registered(emplid,startDate.month) #lấy sách đơn nghỉ phép regIDs
    if len(regID_List) >0:
        for row in regID_List:
            start_Date = row['StartDate']
            end_Date = row['EndDate']
            convert_startDate = datetime.datetime.strptime(start_Date[0:start_Date.find(" ")],"%Y-%m-%d")
            convert_endDate = datetime.datetime.strptime(end_Date[0:end_Date.find(" ")],"%Y-%m-%d")
       
            if convert_startDate <= startDate <= convert_endDate:
                return r
            # if convert_startDate == endDate and convert_endDate:
            #     return r
            if convert_startDate <= startDate and endDate <= convert_endDate:
                return r
            if convert_startDate <= endDate <= convert_endDate:
                return r

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
            SET Type = '{form.offtype}', Reason = N'{form.reason}',StartDate = '{startDate}',Period = {period},RegDate = {c},Address = N'{form.address}',EndDate = '{endDate}'
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
    m = date.month
    y = date.year
    layout = [{'EmpID':'','FirstName':'','LastName':'','DeptID':'','JobPositionName':'','DepartmentName':''}]
    day_In_Month = fn.daysInMonth(y,m)
    offtype = fn.nameOffType()
    for i in day_In_Month:
        layout[0][i.day] = ''
    for i in offtype:
        layout[0][i] = ''


    s = f'''select e.DeptID,j.JPLevel,e.EmpID,e.PosID from Employee e
            inner join JobPosition j on e.PosID = j.JobPosID
            where e.EmpID = {token}'''
    check = fn.get_data(s)
    print(check)
    if len(check)<=0:
        print({'rCode':0,'Msg':'Token không hợp lệ'})
        df = pd.DataFrame(layout)
        df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
        return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx')
    if check[0][1]>50:
        if check[0][0] != 'NS':
            print({'rCode':0,'Msg':'Anh,chị không được phân quyền để lấy đơn nghỉ phép'})
            df = pd.DataFrame(layout)
            df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
            return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx') 
    
    #lấy đơn của tháng trước đã duyệt
    query = fn.getDaysOff_Month(m-1,y,check[0][0])
  
    regID_lastMonth = []
    if len(query) > 0:
        # index = 0
        for i in query:
            numberDays = i['Period']
            
            startdate = datetime.datetime.strptime(i['StartDate'],"%Y-%m-%d %H:%M:%S.%f") #.%f #%H:%M:%S
            endDate = datetime.datetime.strptime(i['EndDate'],"%Y-%m-%d %H:%M:%S.%f")#hệ thống sqlserver lưu dang datetime2
         
            result = fn.numberDays(startDate=startdate,endDate=endDate)#lấy số ngày nghĩ và list ngày
            if len(result)>0:
                listDays = result
            else:
                print('kiểm tra ngày bắt đầu và kết thúc của đơn trên hệ thống')
                df = pd.DataFrame([layout])
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
    # print(query)
    if len(query)>0:
        index = 0
        for i in query:
            numberDays = i['Period']
            startdate = datetime.datetime.strptime(i['StartDate'],"%Y-%m-%d %H:%M:%S.%f") #.%f #%H:%M:%S
            endDate = datetime.datetime.strptime(i['EndDate'],"%Y-%m-%d %H:%M:%S.%f")#hệ thống sqlserver lưu dang datetime2 --> chuyển định dạng của python
            result = fn.numberDays(startDate=startdate,endDate=endDate)
            if len(result)>0:
                listDays = result
            else:
                print('kiểm tra ngày bắt đầu và kết thúc của đơn trên hệ thống')
                df = pd.DataFrame([layout])
                df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
                return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx')
                # return result

            query[index]['Note'] = ''
            listDays_filter = listDays #gán biến trước điều kiện if, nếu if không thỏa thì lấy biến đã gán trước đó
            if endDate.month == m +1:
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
        print(regID_CurrentMonth)  
    total = regID_lastMonth + regID_CurrentMonth
    print(total)
    
    if len(total) <= 0:
        print({'rCode':0,'rMsg':'Không có đơn nghỉ phép'})
        df = pd.DataFrame(layout)
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

    for i in sumPeriod_Type_EmplID: #chạy từng phần tử trong list đã sum số ngày phép theo nhân viên/loại phép, cuối cùng return list thêm dữ liệu
        for e in day_In_Month:
            i[e.day] = '' 
    
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
    for i in layout:
        for e in offtype:
            if e not in i:
                i[e] = ''
    df = pd.DataFrame(layout)
    del df['StartDate'],df['EndDate'],df['Period'],df['RegDate'],df['Address'],df['IDWorkingTime'],df['OffTypeName'],df['Note'],df['listDays']

    df.to_excel(excel_writer='file.xlsx',sheet_name='summary',index= False)
    return FileResponse('file.xlsx',filename='Data_DaysOf.xlsx')
 

  
  
