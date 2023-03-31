from pydantic import BaseModel
import datetime



class CreatedByEmpID(BaseModel):
    empID: int
    gmail: str

class CheckLogin(BaseModel):
    username: str = ""
    password: str = ""
    autogen: int  


# class tạo user (tạo tài khoản đầy đủ thông tin)
class Created(BaseModel):
    username: str
    empID: int
    password: str
    email: str

class Username(BaseModel):
    username: str

# class tạo username nhanh
class CheckUsername(BaseModel):
    empID: int



#class đăng ký nghĩ phép
class Offregister(BaseModel):
    type: int
    reason: str = ""
    startdate: datetime.date #| None = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y%m%d")
    period: int
    address: str = ""
    command: int
# class phê duyệt
class Approve(BaseModel):
    regid: int
    comment: str = ''
    state: int

class ChangePass(BaseModel):
    username: str = ""
    currentPassword: str = ""
    newPassword: str = ""
    confirmPass: str = ""

class Getlist(BaseModel):
    needAppr: int
    astatus: list[int] = []

class AdjustDayOff(BaseModel):
    regid: int
    offtype: int
    reason: str = ""
    startdate: datetime.date
    period: int
    address: str = ""
    command: int

# class DayOffSummary(BaseModel):
#     date: datetime.date
    # @validator('date')
    # def validate_date(cls, value):
    #     try:
    #         datetime.datetime(year=value,month=value,day=value)
    #         return value
    #     except ValueError:
    #         raise ValueError("Bạn đã nhập ngày tháng không hợp lệ!")

# class Add_Department(BaseModel):
