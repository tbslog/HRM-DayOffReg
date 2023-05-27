from datetime import datetime, timedelta
import pyodbc
import jwt
import json
import bcrypt
from fastapi import Depends, HTTPException
from projects.security import validate_token
from numpy import random
#gửi mail
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from socket import gaierror
from typing import  Union
import calendar
import math

# with open('projects/config.json') as f:
with open('projects/config.json') as f:
    data = json.load(f)
# Lấy password kết nối
server=data['server']
database=data['database']
uid=data['uid']
pwd = data['password']
SECRET_KEY = data['SECRET_KEY']
SECURITY_ALGORITHM = data['SECURITY_ALGORITHM']

# kết nối đến Databse -- viết lần 1
def connect_db(server,database,uid,pwd):
    # driver = "{SQL Server Native Client 11.0}"
    # driver = "{ODBC Driver 17 for SQL Server}"
    driver = "{SQL Server}"
    trust = "yes"
    cnstr = f"Driver={driver};Server={server};Database={database};UID={uid};PWD={pwd};"
    # cnstr = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+uid+';PWD=' + pwd
    try:
        cn = pyodbc.connect(cnstr, autocommit=True)
        # cn.autocommit = True
        return cn
    except pyodbc.Error as e:
        print(e, "error")
    return cn




# kết nối đến Databse -- viết lần 2 đang sử dụng
def connect_db1():
    # driver = "{SQL Server Native Client 11.0}"
    # driver = "{ODBC Driver 17 for SQL Server}"
    driver = "{SQL Server}"
    trust = "yes"
    cnstr = f"Driver={driver};Server={server};Database={database};UID={uid};PWD={pwd};"
    # cnstr = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+uid+';PWD=' + pwd
    try:
        cn = pyodbc.connect(cnstr, autocommit=True)
        # cn.autocommit = True
        # return cn
    except pyodbc.Error as e:
        print(e, "error")
    # cmd 
    return cn


#hàm kết nối - truy vấn - đóng kết nối - get data
def get_data(query,option = None):
    if option == 1:
        try:
            cn = connect_db1()
            cursor = cn.cursor()
            rows = cursor.execute(query).fetchall() #fetches all the rows of a query result
            cn.close()
            # print(cursor.description)
            if len(rows) > 0:
                results = []
                columns = [column[0] for column in cursor.description]#cursor.description lấy miêu tả cột dữ liệu (loại dữ liệu, độ dài,...)
                for row in rows:
                    results.append(dict(zip(columns, row)))
                return results
            else:
                return [] #{'detail':'Lỗi'}
        except:
            return []
    else:
        try:
            cn = connect_db1()
            cursor = cn.cursor()
            rows = cursor.execute(query).fetchall() #fetches all the rows of a query result
            cn.close()
            return rows
        except:
            return []

#hàm kết nối - truy vấn - đóng kết nối - insert data - update - delete
def commit_data(query):
    try:
        cn = connect_db1()
        cursor = cn.cursor()
        # print('nhat')
        cursor.execute(query)
        
        cn.commit
        cn.close()
        return [{'note': 'Insert thành công'}]
    except:
        return []



#chỉ kết nối database 1 lần
# cn = connect_db1()


#A.thái-----------------------------------------------------------------------------
# def getDBConnection():
    # cách 1
    # check cn still is connecting
    # if not -> reconnect => cn = connect_db(server, database, uid, pwd)
    # else -> return cn

    # cách 2
    # return connect_db(server, database, uid, pwd)
    # sử dụng xong thì phải disconnect
    # a = None

#A.thái----------------------------------------------------------------------------





# Kiểm tra password với hash_password có khớp với nhau
# hashpw password đã băm (lưu trên server) - pw password bình thường (người dùng nhập)
def check_pw(pw:str,hashpw:str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashpw.encode())
# print(check_pw('Tbs@2021','$2b$12$ANdzXoj.qCcOqjsMcGgpkue7umJOh3D4JplpJoE1rKWxaImI2WwDO')) # --> True

# Băm password
def hashpw(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
# print(hashpw('Tbs@2021')) # --> $2b$12$ANdzXoj.qCcOqjsMcGgpkue7umJOh3D4JplpJoE1rKWxaImI2WwDO

# Tạo token dựa vào username và số ngày
def generate_token(username: str, days: int = 3) -> str:
    if str(username).isnumeric():
        empid = username
    else:
        s = f"""
                        SELECT top 1 EmpID FROM Users WHERE UserName = '{username}' 
                    """
        result = get_data(s)
        for i in result:
            empid = i[0]
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * days  # Expired after 3 days
    )
    if days==0:  # thời hạn mãi mái
        to_encode = {"username": empid}
    else:
        to_encode = {"exp": expire, "username": empid}

    # Tạo token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt

# kiểm tra username, password
def verify_password(username:str, password:str) ->bool:
    s = ''
    if username.isnumeric():
        s = f"""
                SELECT Password FROM Users WHERE EmpID='{username}'
            """
    else:
        s = f"""
                SELECT Password FROM Users WHERE UserName='{username}'
            """
    result = get_data(s)
    if result:
        hpw_server = result[0][0]  # lấy hàng đầu tiên, ô đầu tiên
        # print(hpw_server)
        return check_pw(password,hpw_server)
    else:
        return False


# # def verify_password(username:str, password:str) ->bool:
#     hash_pw = hashpw(password)
#     s = f"""
#             SELECT Password FROM dbo.qtUsers WHERE Username=?
#         """
#     cursor = cn.cursor()
#     rows = cursor.execute(s,username).fetchall()
#     if rows:
#         hpw_server = rows[0][0]  # lấy hàng đầu tiên, ô đầu tiên
#         return check_pw(password,hpw_server)
#     else:
#         return False
def checkuser(username):
    s = f"""
            SELECT count(*) FROM Users WHERE Username= '{username}'
        """
    result = get_data(s)
    if result:
        count = result[0][0]  # lấy hàng đầu tiên, ô đầu tiên
        if count > 0:
            return True
        else:
            return False
    else:
        return False
    


def checkEmplID(EmpID: str):
    if EmpID.isnumeric():
        s = f"""
                SELECT count(*) FROM Employee WHERE EmpID='{EmpID}'
            """
        result = get_data(s)
        
        if len(result) > 0:
            count = result[0][0]  # lấy hàng đầu tiên, ô đầu tiên
            if count > 0:
                return True
            else:
                return False
        else:
            return False
    else:
        False
   

def checkEmplIDUser(EmpID):
    s = f"""
            SELECT count(*) FROM Users WHERE EmpID='{EmpID}'
        """
    result = get_data(s)
    if result:
        count = result[0][0]  # lấy hàng đầu tiên, ô đầu tiên
        
        if count > 0:
            return True
        else:
            return False
    else:
        return False 
    
def checkEmail(Email):
    s = f"""
            SELECT count(*) FROM Users WHERE Email='{Email}'
        """
    result = get_data(s)
    if result:
        count = result[0][0]  # lấy hàng đầu tiên, ô đầu tiên
        if count > 0:
            return True
        else:
            return False
    else:
        return False 

#hàm lấy đơn nghĩ phép những phòng ban quản lý trực tiếp
def TPPP_manager(emplid,jplevel_TP_PP):
    s = f"""
        --trước khi thực thi câu lệnh này thì: jplevel <= 50

            SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,o.EndDate,
                    e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,
                    j.JPLevel,j.Name as JobPositionName,
                    d.Name AS departmentName,
                    jpl.Name AS Position,
                    al.AnnualLeave,
                    sum(a.ApprOrder) as apprOrder, sum(a.ApprovalState) as apprState,
                case 
                    when o.RegDate is null then 0 --N'chưa gửi' 
                    --đơn đó duyệt thì trường regdate phải có data
                    when sum(a.ApprovalState) is null then 1 --N'Chờ Duyệt' 
                    when sum(a.ApprovalState) = 1 then 2 --N'Đã Duyệt'
                    when sum(a.ApprovalState) = 0 then 3 --N'Từ Chối'
                    --when sum(a.ApprovalState) = 1 THEN 2 --N'Đã Duyệt'
                    when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận' --update bản sau, trường hợp đơn đã duyệt đồng ý sau đó hủy đơn 
                    when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
                ELSE 'Error!' end as aStatus
            FROM dbo.OffRegister o
            LEFT JOIN dbo.Approval a ON a.regID = o.regID
            LEFT JOIN dbo.Employee e ON e.EmpID = o.EmpID
            LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
            LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
            LEFT JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
            LEFT JOIN dbo.AnnualLeave al ON al.EmpID = o.EmpID 
            WHERE o.RegDate IS NOT NULL -- lấy những đơn đã gửi
            AND j.JPLevel <= '{jplevel_TP_PP}' -- lấy Trưởng Phòng,Phó Phòng
            -- lấy danh sách nhân viên trong depID con 
            AND	 o.EmpID IN (
            SELECT EmpID FROM dbo.Employee
            -- lấy danh sách depID con
            WHERE DeptID IN (
                            SELECT d.DeptID AS cDeptID
                            FROM dbo.Employee e
                            JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                            JOIN dbo.Department d ON d.pDeptID = e.DeptID
                            WHERE e.EmpID = '{emplid}' AND j.JPLevel <= 50
                            )
                            )
            GROUP BY o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,
            o.Address,o.EndDate,e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,j.JPLevel,j.Name,d.Name,jpl.Name,al.AnnualLeave
            ORDER BY aStatus ASC, o.StartDate ASC
                    """
    result = get_data(s,1)
    return result
    

#hàm lấy đơn nghĩ phép cùng phòng ban
def roommates(depid,jplevel,option:int = None):
    
    jpName = f'AND j.JPName in {idRegisteredJobName()} '
    print(jpName)
    condition = ''
    if option == 1:
        condition = 'AND o.RegDate IS NOT NULL'
        jpName = ''
        if depid in authorDeptRegis():#('VT','HST','BX_NM2','H05','BT','H03','H01','H07','H06','KST','BD','QTM','BCT'):#('H01','H03','H05','H06','H07','HST','BD'):
            return []
    s = f"""
            SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,o.EndDate,
                e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,
                j.JPLevel,j.Name as JobPositionName,
                d.Name AS departmentName,
                jpl.Name AS Position,
                al.AnnualLeave,
                sum(a.ApprOrder) as apprOrder, sum(a.ApprovalState) as apprState,
                case 
                    when o.RegDate is null then 0 --N'chưa gửi' 
                    --đơn đó duyệt thì trường regdate phải có data
                    when sum(a.ApprovalState) is null then 1 --N'Chờ Duyệt' 
                    when sum(a.ApprovalState) = 1 then 2 --N'Đã Duyệt'
                    when sum(a.ApprovalState) = 0 then 3 --N'Từ Chối'
                    when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận' --update bản sau, trường hợp đơn đã duyệt đồng ý sau đó hủy đơn 
                    when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
                    else 'Error!' end as aStatus
            FROM dbo.OffRegister o
            LEFT JOIN dbo.Approval a ON a.regID = o.regID
            LEFT JOIN dbo.Employee e ON e.EmpID = o.EmpID
            LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
            LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
            LEFT JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
            LEFT JOIN dbo.AnnualLeave al ON al.EmpID = o.EmpID 
            WHERE  e.DeptID = '{depid}' AND	j.JPLevel > '{jplevel}' {condition} {jpName}
            group by o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,o.EndDate,
                e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,j.JPLevel,J.Name,d.Name,jpl.Name,al.AnnualLeave
            ORDER BY aStatus ASC, o.StartDate ASC
            """
    # cursor = cn.cursor()
    # rows = cursor.execute(s).fetchall()
    # results = []

    # if len(rows)>0:
    #     # columns = [column[0] for column in cursor.description]
    #     columns = [column[0] for column in cursor.description]
    #     for row in rows:
    #         results.append(dict(zip(columns, row)))

    # return results
    result = get_data(s,1)
    return result
   

#lấy đơn nghĩ phép của mình
def myself(emplid): #filter
    # sFilter = ''
    # afilter = [1,2,4,8,16,32,64,128]
    # for a in afilter:
    #     if filter & a: # đơn mới
    #         if len(sFilter)>0:
    #             sFilter = 'OR ' + sFilter
    #         sFilter = sFilter + ' (aStatus = {a})'
        
    
    # if len(sFilter)>0:
    #         sFilter = 'AND (' + sFilter + ')'
    s = f"""
                select r.EmpID,r.regID,r.Period,r.StartDate,r.RegDate,r.Type,r.Address,r.Reason,r.EndDate,
                e.FirstName,e.LastName,e.ComeDate,e.DeptID,e.PosID,
                j.JPLevel,j.Name as JobPositionName,
                d.Name AS departmentName,
                jpl.Name AS Position,
                al.AnnualLeave,
                sum(a.ApprOrder) as apprOrder, sum(a.ApprovalState) as apprState,
                    case 
                        when r.RegDate is null then 0 --N'chưa gửi' 
                        --đơn đó duyệt thì trường regdate phải có data
                        when sum(a.ApprovalState) is null then 1 --N'Chờ Duyệt' 
                        when sum(a.ApprovalState) = 1 then 2 --N'Đã Duyệt'
                        when sum(a.ApprovalState) = 0 then 3 --N'Từ Chối'
                        when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận' --update bản sau, trường hợp đơn đã duyệt đồng ý sau đó hủy đơn 
                        when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
                        else 'Error!' end as aStatus
                from [dbo].[OffRegister] r 
                LEFT join [dbo].[Approval] a on r.regID = a.regid
                LEFT JOIN dbo.Employee e ON e.EmpID = r.EmpID
                LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
                LEFT JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
                LEFT JOIN dbo.AnnualLeave al ON al.EmpID = r.EmpID 
                WHERE r.EmpID = '{emplid}'--trường hợp lấy empid trong bảng offregister
                group by r.EmpID,r.regID,r.Period,r.StartDate,r.RegDate,r.Type,r.Address,r.Reason,r.EndDate,e.FirstName,e.LastName,
                e.ComeDate,e.DeptID,e.PosID,j.JPLevel,j.Name,d.Name,jpl.Name,al.AnnualLeave
                ORDER BY aStatus ASC, r.StartDate ASC
                    """
    result = get_data(s,1)
    return result

#lấy danh sách phê duyệt được chỉ định depart_staff_manager
def entrust(EmpID):
    s = f'''
            SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.EndDate,
                    e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,
                    j.JPLevel,j.Name as JobPositionName,
                    d.Name AS departmentName,
                    jpl.Name AS Position,
                    al.AnnualLeave,
                    sum(a.ApprOrder) as apprOrder, sum(a.ApprovalState) as apprState,
            case 
                when o.RegDate is null then 0 --N'chưa gửi' 
                --đơn đó duyệt thì trường regdate phải có data
                when sum(a.ApprovalState) is null then 1 --N'Chờ Duyệt' 
                when sum(a.ApprovalState) = 1 then 2 --N'Đã Duyệt'
                when sum(a.ApprovalState) = 0 then 3 --N'Từ Chối'
                --when sum(a.ApprovalState) = 1 THEN 2 --N'Đã Duyệt'
                when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận' --update bản sau, trường hợp đơn đã duyệt đồng ý sau đó hủy đơn 
                when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
            ELSE 'Error!' end as aStatus
            FROM dbo.Employee e
            LEFT JOIN dbo.OffRegister o ON o.EmpID = e.EmpID
            LEFT JOIN	dbo.Approval a ON a.regID = o.regID
            LEFT JOIN dbo.JobPosition j ON	j.JobPosID = e.PosID
            LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
            LEFT JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
            LEFT JOIN dbo.AnnualLeave al ON al.EmpID = e.EmpID
            --AND j.JPLevel >=50
            WHERE o.RegDate IS NOT NULL AND e.DeptID IN (
            SELECT DeptID FROM dbo.ApprovalOrder
            WHERE Approver = '{EmpID}')
            GROUP BY o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,o.EndDate,
                        e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,
                        j.JPLevel,j.Name,
                        d.Name,
                        jpl.Name,
                        al.AnnualLeave
            ORDER BY aStatus ASC, o.StartDate ASC
            '''
    result = get_data(s,1)
    return result

def genPass():
  keys = ['Mat troi','Mat trang','chem chep','Bach tuoc','Ca da bo','Ca map xam','Ca ngat','Ca nheo',
            'Ca chim trang','Ca mat trang','Ca hoi nuong ','Ca keo kho','Ca tram co','Ca chep giòn',
            'Ca nuc kho ca','Ca nuc hap','Ca dao den','Ca trang','Trung ca hoi ','Dan ca heo','Tom the vang',
            'Tom xu xanh','Tom hum alaska','Tom kho nho','Muc ong','Muc nang','Muc trung','Con bo nau','Con bo rung',
            'Con bo den','Con bo sua','Ga dong tao','Con ga mai','Con ga trong','Con vit bau','Con vit co','Con ngan',
            'Con ngong','Con cho muc','Con cho vang','Con meo Con','Con meo muop','Con meo den','Con meo vang','Con de den',
            'Con de trang','Con de nui','Con ho xam','Con gau trang','Gau bac cuc','Con gau nau']

  return keys[random.randint(len(keys))].title().replace(" ","")

def sentMail(receiver_email,state):
    if state == 0:#gửi đơn đến quản lý
        a = "Anh/Chị có đơn nghỉ phép cần phê duyệt! (vui lòng truy cập vào web để kiểm tra):"
    elif state == 1:#gửi mail đến người xin nghỉ phép
        a = "Đơn nghỉ phép của bạn đã được phê duyệt thành công! (vui lòng truy cập vào web để kiểm tra)"
    elif state == 2:#gửi đơn đến nhân sự
        a = "Có đơn nghỉ phép đã được duyệt (Đồng ý)! (vui lòng truy cập vào web để kiểm tra)"
    port = 465
    smtp_server = "pro201.emailserver.vn" #
    login = "its@tbslogistics.com" # paste your login generated by Mailtrap
    password = "i)$sdH(c9O,M" # paste your password generated by Mailtrap
    sender_email = "its@tbslogistics.com"
    receiver_email = receiver_email #['nhat.thivan.hcm@gmail.com', 'nhat.thi@tbslogistics.com']
    message = MIMEMultipart("alternative")
    message["Subject"] = "TBS Logistics Auto Mailer - Đơn nghỉ phép"
    message["From"] = sender_email

    receiver_email_filter = []
    for i in receiver_email:
        if isinstance(i,str) and i != '':
            receiver_email_filter.append(i)
    print(receiver_email_filter)

    message["To"] = ';'.join(receiver_email_filter)
    # write the text/plain part
    text = f"""\
    Hi,
    {a}
    http://hrm-dor.tbslogistics.com.vn/
    Feel free to let us know what content would be useful for you!"""
    # write the HTML part
    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        {a}</p>
        <p><a href="http://hrm-dor.tbslogistics.com.vn/">link web nghỉ phép.</a></p>
        <p> Feel free to <strong>let us</strong> know what content would be useful for you!</p>
    </body>
    </html>
    """
    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    # send your email
    #with smtplib.SMTP(smtp_server, port) as server:

    context = ssl.create_default_context()

    try:
        #send your message with credentials specified above
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(login, password)
            server.sendmail(
                sender_email, receiver_email_filter, message.as_string()
            )
        # tell the script to report if your message was sent or which errors need to be fixed 
        print('Sent')
    except (gaierror, ConnectionRefusedError):
        print('Failed to connect to the server. Bad connection settings?')
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))

# viết đơn nghĩ phép gửi mail cho sếp
def get_receiver_email_manag(emplId):
    s1 = f'''
            SELECT u.Email,e.DeptID,j.JPLevel  FROM dbo.Users u
            INNER JOIN	dbo.Employee e ON e.EmpID = u.EmpID
            INNER JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
            WHERE u.EmpID = '{emplId}'
        ''' #lấy thông tin nhân viên nghĩ phép
    query_sender = get_data(s1)
    receiver_email = []
    if len(query_sender)>0:
        email = query_sender[0][0] #chưa sử dụng biến này
        deptID = query_sender[0][1]
        jplevel = query_sender[0][2]
        #nếu là nhân viên gửi
        a = 'd.DeptID'
        if jplevel > 50:
            b = '<=50'
        elif jplevel == 50 or jplevel == 40 or jplevel == 30:
            a = "d.pDeptID"
            b = f'<{jplevel}'
        elif jplevel > 40:
            b = '= 40'
        elif jplevel > 30:
            b = '= 30'
        #lấy mail người quản lý trực tiếp
        s = f'''
                SELECT {a},e.FirstName,j.JPLevel,u.Email FROM dbo.Department d
                LEFT JOIN dbo.Employee e ON e.DeptID = {a}
                LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                LEFT JOIN dbo.Users u ON u.EmpID = e.EmpID
                WHERE d.DeptID = '{deptID}' AND j.JPLevel {b}
                '''
        result_s = get_data(s)
        if len(result_s)>0:
            for row in result_s:
                receiver_email.append(row[3])
        #lấy mail người approve được chỉ định
        s2 = f'''
                DECLARE @deptID AS VARCHAR(10);
                SELECT @deptID = DeptID FROM dbo.Employee
                WHERE EmpID = '{emplId}'
                SELECT a.Approver,u.Email,e.FirstName,e.LastName,e.DeptID FROM dbo.ApprovalOrder a
                LEFT JOIN dbo.Users u ON u.EmpID = a.Approver
                LEFT JOIN dbo.Employee e ON e.EmpID = a.Approver
                WHERE a.DeptID = @deptID
                '''
        result_s2 = get_data(s2)
        if len(result_s2)>0:
            for row in result_s2:
                receiver_email.append(row[1])
    return receiver_email

# def get_email_ApprovalOder(empID): 
#     s = f'''
#     DECLARE @deptID AS VARCHAR(10);
#     SELECT @deptID = DeptID FROM dbo.Employee
#     WHERE EmpID = '{empID}'
#     SELECT a.Approver,u.Email,e.FirstName,e.LastName,e.DeptID FROM dbo.ApprovalOrder a
#     LEFT JOIN dbo.Users u ON u.EmpID = a.Approver
#     LEFT JOIN dbo.Employee e ON e.EmpID = a.Approver
#     WHERE a.DeptID = @deptID
#     '''
#     result = get_data(s)
#     email_ApprovalOder = []
#     if len(result)>0:
#         for row in result:
#             email_ApprovalOder.append(row[1])
#     return email_ApprovalOder

# def get_receiver_email_manag2(emplId):
#     s = f'''
#             SELECT u.Email,e.DeptID,j.JPLevel FROM dbo.Users u
#             INNER JOIN dbo.Employee e ON e.EmpID = u.EmpID
#             INNER JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
#             WHERE u.EmpID = {emplId}
#             '''
#     query_sender = get_data(s)
#     receiver_mail = []
#     if 

def deptlevel():
    dept_level = []
    s = f'''SELECT DLvlCode FROM dbo.DeptLevel'''
    result = get_data(s)
    for row in result:
        dept_level.append(row[0])
    return dept_level

def deptID_list():
    s = f'''SELECT DeptID FROM dbo.Department'''
    query = get_data(s)
    deptID_list = []
    for i in query:
        deptID_list.append(i[0])
    return deptID_list

def department_deptID(deptID):
    s = f'''SELECT d.DeptID,d.Name,d.DeptLevel,d.pDeptID,d.DeptMng,d.Status,d.Note,
            dl.DLvlName 
            FROM dbo.Department d
            INNER JOIN dbo.DeptLevel dl ON dl.DLvlCode = d.DeptLevel
            WHERE DeptID = '{deptID}' '''
    result = get_data(s,1)
    return result
    
def department_pdeptID(pdeptID):
    s = f'''SELECT d.DeptID,d.Name,d.DeptLevel,d.pDeptID,d.DeptMng,d.Status,d.Note,
            dl.DLvlName  FROM dbo.Department d
            INNER JOIN dbo.DeptLevel dl ON dl.DLvlCode = d.DeptLevel
            WHERE pDeptID = '{pdeptID}' '''
    result = get_data(s,1)
    return result


#------------------------------------------update theo yêu cầu mới
#lấy đơn phòng ban con
def depart_manager(emplid):#,jplevel_TP_PP
    s = f"""
        --trước khi thực thi câu lệnh này thì: jplevel <= 50

            SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,o.EndDate,
                    e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,
                    j.JPLevel,j.Name as JobPositionName,
                    d.Name AS departmentName,
                    jpl.Name AS Position,
                    al.AnnualLeave,
                    sum(a.ApprOrder) as apprOrder, sum(a.ApprovalState) as apprState,
                case 
                    when o.RegDate is null then 0 --N'chưa gửi' 
                    --đơn đó duyệt thì trường regdate phải có data
                    when sum(a.ApprovalState) is null then 1 --N'Chờ Duyệt' 
                    when sum(a.ApprovalState) = 1 then 2 --N'Đã Duyệt'
                    when sum(a.ApprovalState) = 0 then 3 --N'Từ Chối'
                    --when sum(a.ApprovalState) = 1 THEN 2 --N'Đã Duyệt'
                    when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận' --update bản sau, trường hợp đơn đã duyệt đồng ý sau đó hủy đơn 
                    when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
                ELSE 'Error!' end as aStatus
            FROM dbo.OffRegister o
            LEFT JOIN dbo.Approval a ON a.regID = o.regID
            LEFT JOIN dbo.Employee e ON e.EmpID = o.EmpID
            LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
            LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
            LEFT JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
            LEFT JOIN dbo.AnnualLeave al ON al.EmpID = o.EmpID 
            WHERE o.RegDate IS NOT NULL -- lấy những đơn đã gửi
            --AND j.JPLevel <= 'jplevel_TP_PP' -- lấy Trưởng Phòng,Phó Phòng --jplevel_TP_PP: do công thức tính ra
            -- lấy danh sách nhân viên trong depID con 
            AND	 o.EmpID IN (
            SELECT EmpID FROM dbo.Employee
            -- lấy danh sách depID con
            WHERE DeptID IN (
                            SELECT d.DeptID AS cDeptID
                            FROM dbo.Employee e
                            JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
                            JOIN dbo.Department d ON d.pDeptID = e.DeptID
                            WHERE e.EmpID = '{emplid}' AND j.JPLevel <= 50
                            )
                            )
            GROUP BY o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,
            o.Address,o.EndDate,e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,j.JPLevel,j.Name,d.Name,jpl.Name,al.AnnualLeave
            ORDER BY aStatus ASC, o.StartDate ASC
                    """
    result = get_data(s,1)
    return result




def HTTP_RETURN(status_code, messange, error: None = "" ,data: Union[list, dict,str,int] | None = {}): #, headers: dict | None = {}
    return {
        'rCode': status_code,
        'rMsg': messange,
        'rError': error,
        'rData': data
    }




# def numberDays(emplID,startDate,endDate,period):
    # if emplID is None or startDate is None or endDate is None:
    #     return HTTP_RETURN(status_code=0,messange='Vui lòng nhập đầy đủ thông tin')
    # s = f'''select IDWorkingTime from Employee where EmpID = {emplID}'''
    # query = get_data(s)
    # if len(query) <= 0:
    #     return HTTP_RETURN(status_code=0,messange='Mã nhân viên không tồn tại')#Employee code does not exist
    
    # if startDate is None or endDate is None:
    #     return HTTP_RETURN(status_code=0,messange='Vui lòng kiểm tra lại ngày bắt đầu hoặc kết thúc')

    # if startDate > endDate:
    #     return HTTP_RETURN(status_code=0,messange='Vui lòng chọn lại ngày nghỉ phép')
    
    # if period < 0.5:
    #     return HTTP_RETURN(status_code=0,messange='Vui lòng Nhập số ngày nghĩ phép')
    
    # time_delta = endDate - startDate + timedelta(days=1)
    # period = time_delta.days
    
    
    # listDays = []
    # listDays_Subtracted = []
    # for i in range(0,period):
    #     day= startDate + timedelta(days=i)
    #     listDays.append(day)

    #     # print(startDate)
    # # print(listDays)
    # if query[0][0] == 0: #công nhân (tally,xn,bx) + chứng từ
    #     if period >= 7 and period < 14:
    #         # period -= 1
    #         del listDays[int((len(listDays)-1)/2)] # trừ ngày nghỉ ở giữa - ngày ở giữa là ngày nghỉ mỗi tuần
    #         listDays_Subtracted = listDays #đưa vào danh sách khác, do biến dùng chung
    #     elif period >= 14 and period < 21:
    #         # period -= 2
    #         del listDays[int((len(listDays)-1)/2)]
    #         del listDays[int((len(listDays)-1)/2)] #trừ 2 ngày nghỉ cuối cùng - 2 ngày cuối cùng là ngày nghỉ mỗi tuần
    #         listDays_Subtracted = listDays
    #     elif period >= 21:
    #         # period -= 3
    #         del listDays[int((len(listDays)-1)/2)]
    #         del listDays[int((len(listDays)-1)/2)]
    #         del listDays[int((len(listDays)-1)/2)]
    #         listDays_Subtracted = listDays
    # elif query[0][0] == 2: #chế độ nghĩ t7,cn
    #     index = len(listDays)
        
    #     for e in range(0,index):
    #         weekday = datetime.isoweekday(listDays[e])
    #         if weekday == 7 or weekday == 6:#ngày chủ nhật hoặc thứ 7
    #             period -= 1
    #         else:
    #             listDays_Subtracted.append(listDays[e])
    # else: #query[0][0] == 1 chế độ nghỉ 1 ngày cn
    #     index = len(listDays)
    #     for e in range(0,index):
    #         weekday = datetime.isoweekday(listDays[e])
    #         if weekday == 7:
    #             period -= 1
    #         else:
    #             listDays_Subtracted.append(listDays[e])

    # # print(listDays_Subtracted)
    # # print(period)
    
    # if period >0:
    #     return HTTP_RETURN(status_code=1,messange='Số ngày nghỉ phép của bạn',data={'listDays':listDays_Subtracted})
    # return HTTP_RETURN(status_code=1,messange='Vui lòng Chọn lại ngày nghỉ phép')

#lấy tất cả đơn nghỉ phép đã duyệt trong tháng
def getDaysOff_Month(month,year,deptID):
    try:
        if deptID == 'NS':
            var = ''
        else:
            var = f'''and e.DeptID = '{deptID}' '''

        s = f'''select o.EmpID,o.StartDate,o.EndDate,o.Period,o.RegDate,o.Address, --o.regID,o.reason,o.Type,
                e.IDWorkingTime,e.LastName,e.FirstName,e.DeptID,
                d.Name as 'DepartmentName',
                j.Name as 'JobPositionName',
                
                ot.Name AS 'OffTypeName' from offregister o
                inner join Employee e on o.EmpID = e.EmpID
                inner join JobPosition j on e.PosID = j.JobPosID
                inner join Department d on e.DeptID = d.DeptID
                inner join OffType ot on o.Type = ot.OffTypeID
                where month(o.startdate) = {month} and year(o.startdate) = {year} {var} and o.regid in
                (select regid from Approval --sum(approvalstate)
                group by regID
                having SUM(approvalstate) = 1)'''
        query = get_data(s,1)
        # print(s)
        if len(query) >0:
            return query
        return []
    except:
        return []
# #lấy danh sách ngày đã đăng nghỉ phép của 1 nhân viên trong tháng
# def daysList_Registered(emplID,month):
#     s = f'''select a.regID,o.StartDate,o.EndDate,o.EmpID from Approval a
#             inner join OffRegister o on a.regID = o.regID
#             where o.EmpID = {emplID} and MONTH(o.StartDate) = {month}
#             group by a.regID,o.StartDate,o.EndDate,o.EmpID
#             having sum(approvalstate) = 1'''
#     query = get_data(s,1)
#     if len(query)>0:
#         return query
#     return []

def daysList_Registered(emplID,month):
    s = f'''select o.regID,o.StartDate,o.EndDate,o.EmpID from OffRegister o
            where o.EmpID = {emplID} and MONTH(o.StartDate) = {month}
            and o.RegDate is not null
           '''
    query = get_data(s,1)
    if len(query)>0:
        return query
    return []

def approvalOrder():
    s= f'''select approver from ApprovalOrder'''
    result = get_data(s)
    approval_Or = []
    if len(result)>0:
        for i in result:
            approval_Or.append(int(i[0]))
    return approval_Or

#-------------------bảng mới tạo

def authorDeptRegis():
    s = f'''select * from AuthorDeptRegis'''
    result = get_data(s)
    lis = []
    if len(result)>0:
        for i in result:
            lis.append(i[1])
    return lis


def idRegisteredJobName():
    s = f'''select * from IDRegisteredJobName'''
    result = get_data(s)
    tup = [0.1,0.2] #cho 2 số ví dụ khi if không thỏa, thì  chuyển đổi về dạng tuple không gặp dấu phẩy cuối cùng(1 phần tử thì sẻ gặp)
    print(tuple(tup))
    if len(result)>0:
        for i in result:
            tup.append(i[1])

    # print(tuple(tup))
    return tuple(tup)


#----------------------------------------THIVANNHAT lầm tối ngày 27.05

def daysInMonth(y,m):
    day_In_Month = []
    try:
        number_of_days = calendar.monthrange(y, m)[1]
        firstDay = datetime.date(datetime(y,m,1))
        for i in range(0,number_of_days):
            day = firstDay + timedelta(days=i)
            day_In_Month.append(day)
        return day_In_Month
    except:
        return day_In_Month
    
def nameOffType():
    offtype = []
    try:
        s = f"""SELECT Name FROM dbo.OffType"""
        result_query1 = get_data(s)
        for row in result_query1:
            offtype.append(row[0])
        return offtype
    except:
        return offtype
        

def numberDays(startDate,endDate):#emplID,
    try:
        if  startDate is None or endDate is None:
            return HTTP_RETURN(status_code=0,messange='Vui lòng nhập đầy đủ thông tin')

        if startDate > endDate:
            return HTTP_RETURN(status_code=0,messange='Vui lòng chọn lại ngày nghỉ phép')
        
        time_delta = endDate - startDate + timedelta(days=1)
        period = time_delta.days
        
        listDays = []
        if period > 0:
            for i in range(0,period):
                day= startDate + timedelta(days=i)
                listDays.append(day)
        return listDays
    except:
        return []

    



    # if len(listDays_Subtracted) >0:
    #     return listDays_Subtracted
    # return HTTP_RETURN(status_code=1,messange='Vui lòng Chọn lại ngày nghỉ phép')

        # print(startDate)
    # # print(listDays)
    # if query[0][0] == 0: #công nhân (tally,xn,bx) + chứng từ
    #     if period >= 7 and period < 14:
    #         # period -= 1
    #         del listDays[int((len(listDays)-1)/2)] # trừ ngày nghỉ ở giữa - ngày ở giữa là ngày nghỉ mỗi tuần
    #         listDays_Subtracted = listDays #đưa vào danh sách khác, do biến dùng chung
    #     elif period >= 14 and period < 21:
    #         # period -= 2
    #         del listDays[int((len(listDays)-1)/2)]
    #         del listDays[int((len(listDays)-1)/2)] #trừ 2 ngày nghỉ cuối cùng - 2 ngày cuối cùng là ngày nghỉ mỗi tuần
    #         listDays_Subtracted = listDays
    #     elif period >= 21:
    #         # period -= 3
    #         del listDays[int((len(listDays)-1)/2)]
    #         del listDays[int((len(listDays)-1)/2)]
    #         del listDays[int((len(listDays)-1)/2)]
    #         listDays_Subtracted = listDays
    # elif query[0][0] == 2: #chế độ nghĩ t7,cn
    #     index = len(listDays)
        
    #     for e in range(0,index):
    #         weekday = datetime.isoweekday(listDays[e])
    #         if weekday == 7 or weekday == 6:#ngày chủ nhật hoặc thứ 7
    #             period -= 1
    #         else:
    #             listDays_Subtracted.append(listDays[e])
    # else: #query[0][0] == 1 chế độ nghỉ 1 ngày cn
    #     index = len(listDays)
    #     for e in range(0,index):
    #         weekday = datetime.isoweekday(listDays[e])
    #         if weekday == 7:
    #             period -= 1
    #         else:
    #             listDays_Subtracted.append(listDays[e])

    # print(listDays_Subtracted)
    # print(period)
    
   