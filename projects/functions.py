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
            if len(rows) > 0:
                results = []
                columns = [column[0] for column in cursor.description]
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

#hàm kết nối - truy vấn - đóng kết nối - insert data - update
def insert_data(query):
    try:
        cn = connect_db1()
        cursor = cn.cursor()
        cursor.execute(query)
        cn.commit
        cn.close()
        return [{'note': 'Insert thành công'}]
    except:
        return []



#chỉ kết nối database 1 lần
cn = connect_db1()


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
def depart_manager(emplid,jplevel_TP_PP):
    s = f"""
        --trước khi thực thi câu lệnh này thì: jplevel <= 50

            SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,
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
                    when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận'
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
            o.Address,e.LastName,e.FirstName,e.DeptID,e.PosID,e.ComeDate,j.JPLevel,j.Name,d.Name,jpl.Name,al.AnnualLeave
            ORDER BY aStatus ASC, o.StartDate ASC
                    """
    result = get_data(s,1)
    return result
    

#hàm lấy đơn nghĩ phép cùng phòng ban
def roommates(depid,jplevel):
    s = f"""
            SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,
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
                    when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận'
                    when sum(a.ApprOrder) = 7 then 5 --N'GĐ Kiêm Soát'
                    else 'Error!' end as aStatus
            FROM dbo.OffRegister o
            LEFT JOIN dbo.Approval a ON a.regID = o.regID
            LEFT JOIN dbo.Employee e ON e.EmpID = o.EmpID
            LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
            LEFT JOIN dbo.Department d ON d.DeptID = e.DeptID
            LEFT JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
            LEFT JOIN dbo.AnnualLeave al ON al.EmpID = o.EmpID 
            WHERE  e.DeptID = '{depid}' AND	j.JPLevel > '{jplevel}' AND o.RegDate IS NOT NULL
            group by o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.Address,
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
                select r.EmpID,r.regID,r.Period,r.StartDate,r.RegDate,r.Type,r.Address,r.Reason,
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
                        when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận'
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
                group by r.EmpID,r.regID,r.Period,r.StartDate,r.RegDate,r.Type,r.Address,r.Reason,e.FirstName,e.LastName,
                e.ComeDate,e.DeptID,e.PosID,j.JPLevel,j.Name,d.Name,jpl.Name,al.AnnualLeave
                ORDER BY aStatus ASC, r.StartDate ASC
                    """
    result = get_data(s,1)
    return result

#lấy danh sách phê duyệt được chỉ định
def depart_staff_manager(EmpID):
    s = f'''
            SELECT o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,
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
                when sum(a.ApprOrder) = 3 then 4 --N'NS Tiếp Nhận'
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
            GROUP BY o.regID,o.EmpID,o.Type,o.Reason,o.StartDate,o.Period,o.RegDate,o.AnnualLeave,o.Address,
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
    message["To"] = ';'.join(receiver_email)
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
                sender_email, receiver_email, message.as_string()
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




