state = 0
if state == 0:
        a = "Anh/Chị có đơn cần phê duyệt! (vui lòng truy cập vào web):"
elif state == 1:
        a = "Đơn đã được phê duyệt! (vui lòng truy cập vào web)"
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
print(html)
#-----------------------------------------------------------------
# if jplevel > 50:
#             #thông tin người nhận mail (trưởng phòng)
#             s2 = f'''
#                 SELECT e.EmpID,e.FirstName,e.LastName,e.DeptID,
#                     j.JPLevel,
#                     jpl.Name AS 'Position',
#                     u.Email
#                 FROM dbo.Employee e
#                 INNER JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
#                 INNER JOIN dbo.JPLevel jpl ON jpl.JPLevelID = j.JPLevel
#                 INNER JOIN dbo.Users u ON u.EmpID = e.EmpID
#                 WHERE e.DeptID = '{deptID}' AND j.JPLevel <= 50
#                 '''
#             query_receiver = get_data(s2)
#             if len(query_receiver)>0:
#                 for row in query_receiver:
#                     receiver_email.append(row[6])
#             else:#lấy mail người phế duyệt chỉ định
#                 s4 = f'''
#                         SELECT e.EmpID,e.FirstName,e.LastName,e.DeptID,j.JPLevel,u.Email FROM dbo.Employee e 
#                         LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
#                         LEFT JOIN dbo.Users u ON u.EmpID = e.EmpID
#                         WHERE j.JPLevel <=50 AND e.DeptID IN (
#                         SELECT pDeptID FROM dbo.Department
#                         WHERE DeptID = '{deptID}')
#                         '''
#                 query_receiver = get_data(s4)
#                 if len(query_receiver)>0:
#                     for row in query_receiver:
#                         receiver_email.append(row[5])
#             # sentMail(receiver_email)
#             return receiver_email
#         #cấp trưởng nhóm gửi
#         elif jplevel == 50: 
#             #jplevel_TP_PP = ((int(jplevel/10)-1)*10)+9
#             s3 = f'''
#                     SELECT d.pDeptID,e.FirstName,j.JPLevel,u.Email FROM dbo.Department d
#                     LEFT JOIN dbo.Employee e ON e.DeptID = d.pDeptID
#                     LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
#                     LEFT JOIN dbo.Users u ON u.EmpID = e.EmpID
#                     WHERE d.DeptID = '{deptID}' AND j.JPLevel < '{jplevel}' 
#                     '''     
#             query_receiver = get_data(s3)
#             if len(query_receiver)>0:
#                 for row in query_receiver:
#                     receiver_email.append(row[3])
#             return receiver_email
#         #Cấp phó bộ phận gửi
#         elif jplevel > 40: #lớn hơn 40 (jplevel 41-->49)
#             s5 =  f'''
#                     select e.EmpID,e.FirstName,e.LastName,e.DeptID,j.JPLevel,u.Email from employee e
#                     left join JobPosition j on e.PosID = j.JobPosID
#                     left join dbo.Users u ON u.EmpID = e.EmpID
#                     where e.deptID = '{deptID}' and j.JPLevel = 40'''
#             query_receiver = get_data(s5)
#             if len(query_receiver) > 0:
#                 for row in query_receiver:
#                     receiver_email.append(row[5])
#             else:
#                 s6 = f'''
#                         SELECT e.EmpID,e.FirstName,e.LastName,e.DeptID,j.JPLevel,u.Email FROM dbo.Employee e
#                         LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
#                         LEFT JOIN dbo.Users u ON u.EmpID = e.EmpID
#                         WHERE j.JPLevel <= 40 AND e.DeptID in
#                         (SELECT pDeptID FROM dbo.Department
#                         WHERE DeptID = '{deptID}')
#                         '''
#                 query_receiver = get_data(s6)
#                 if len(query_receiver) > 0:
#                     for row in query_receiver:
#                         receiver_email.append(row[5])
#             return receiver_email
#         #cấp trưởng phòng gửi
#         elif jplevel == 40:
#             s7 = f'''
#                     SELECT e.EmpID,e.FirstName,e.LastName,e.DeptID,j.JPLevel,u.Email FROM dbo.Employee e
#                     LEFT JOIN dbo.JobPosition j ON j.JobPosID = e.PosID
#                     LEFT JOIN dbo.Users u ON u.EmpID = e.EmpID
#                     WHERE j.JPLevel < 40 AND e.DeptID in
#                     (SELECT pDeptID FROM dbo.Department
#                     WHERE DeptID = '{deptID}')




