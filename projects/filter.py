def myself(emplid, afilter):
    sFilter = ''
    # afilter = [1,2,4,8,16,32,64,128]
    for a in afilter:
        # 'if filter & a: # đơn mới
            # print (len(sFilter))
            if len(sFilter)>0:
                sFilter = sFilter + ' OR '
            sFilter = sFilter + f'(aStatus = {a})'
        
    
    if len(sFilter)>0:
            sFilter = 'AND (' + sFilter + ')'
    s = f"""
                select r.EmpID,r.regID,r.Period,r.StartDate,r.RegDate,r.Type,r.Address,r.Reason,e.FirstName,e.LastName,e.ComeDate,e.DeptID,e.PosID,j.JPLevel,sum(a.ApprOrder) as apprOrder, sum(a.ApprovalState) as apprState,
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
                WHERE r.EmpID = '{emplid}' {sFilter} --trường hợp lấy empid trong bảng offregister
                group by r.EmpID,r.regID,r.Period,r.StartDate,r.RegDate,r.Type,r.Address,r.Reason,e.FirstName,e.LastName,e.ComeDate,e.DeptID,e.PosID,j.JPLevel
                ORDER BY aStatus ASC, r.StartDate ASC
                    """
    return s

print (myself(11111,[2,3,5]))

