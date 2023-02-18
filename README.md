update 02/18/2023 function 
lấy typeID(loại phép) mới nhất khi có cập nhật trên sever
lấy thêm thông tin đơn (tên vị trí làm việc,số ngày phép còn lại,ngày vào,) của cấp dưới
sửa tên "accept" về lại tiếng việt (hàm lấy đơn them regID)
thêm điều kiện (đơn bị từ chối phải có comment)




# HRM-DayOffReg
update ngày 02/08/2023 function đăng ký nghĩ phép (API day-off-letter) - cấu trúc JSON cho dữ liệu trả về:
{
'rCode': <integer value>,
'rData': dict { }
'rMsg': <string value>,
'rError': dict {
   <fieldName>: [<error messager = string vaue>]
   }
}

