#03/09/2023
API	day-off-letters - lấy đơn nghĩ phép (đổi method post --> get)				
		parameter:			
               needAppr:	1	lấy đơn quản lý
                           khác	lấy chính mình
               astatus (truyền vào 1,2,3,…):	1	Chờ Duyệt
                                             2	Đã Duyệt
                                             3	Từ Chối
                                             4	NS Tiếp Nhận
                                             5	GD Kiểm soát
					
	day-off-letter - Đăng ký nghĩ phép	thêm điều kiện: nghĩ phép phải có lý do			



#update 02/18/2023 function 
lấy typeID(loại phép) mới nhất khi có cập nhật trên sever
lấy thêm thông tin đơn (tên vị trí làm việc,số ngày phép còn lại,ngày vào,) của cấp dưới
sửa tên "accept" về lại tiếng việt (hàm lấy đơn them regID)
thêm điều kiện (đơn bị từ chối phải có comment)




# 02/08/2023
update ngày 02/08/2023 function đăng ký nghĩ phép (API day-off-letter) - cấu trúc JSON cho dữ liệu trả về:
{
'rCode': <integer value>,
'rData': dict { }
'rMsg': <string value>,
'rError': dict {
   <fieldName>: [<error messager = string vaue>]
   }
}

