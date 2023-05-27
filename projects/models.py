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
    emplid: int = 0
    type: int
    reason: str = ""
    startdate: datetime.date #| None = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y%m%d")
    endDate: datetime.date = None
    period: float = None
    address: str = ""
    command: int
    # otherRegis:int
# class phê duyệt
class Approve(BaseModel):
    regid: int
    comment: str = ''
    state: int


# class RecallApprovalLeave(BaseModel):
#     regid: int = None


class ChangePass(BaseModel):
    # username: str = ""
    currentPassword: str = ""
    newPassword: str = ""
    confirmPass: str = ""

class Getlist(BaseModel):
    needAppr: int
    astatus: list[int] = []

class AdjustDayOff(BaseModel):
    # emplid: int = None
    regid: int
    offtype: int
    reason: str = ""
    startdate: datetime.date
    endDate: datetime.date = None
    period: float = None
    address: str = ""
    command: int

class Im_department(BaseModel):
    name_deptID: str = ''
    deptlevel: int = None
    pDeptID: str = ''
    note: str = ''

class Update_department(BaseModel):
    deptID: str = ''
    nameDeptID: str = ''
    deptLevel: int = None
    pDeptID: str = ''
    deptMng: int = None
    status: int = 1
    note: str = ''


class Import_position(BaseModel):
    jplevelID: int = None
    Name: str = ''
    # status: int = 1
    # pJPlevel: int = None
    note: str = ''
    # state: int = None
    
class Update_position(BaseModel):
    jplevelID: int = None
    name: str = ''
    status: int = None
    # pJPlevel: int = None
    note: str = ''

class Import_JobPosition(BaseModel):
    jplevel: int = None
    jpname: int = None
    deptID: str = ''
    #status: int = 0
    note: str = ''


class Update_JobPosition(BaseModel):
    jobPosID: int = None
    name: str = ''
    jplevel: int = None
    jpname: int = None
    deptID: str = ''
    status: int = None
    note: str = ''
    





# class HRM(BaseModel):
#     class Tinhluong(BaseModel):
#         a: int
#         b: int
#     class Thongtinnhanvien(BaseModel):
#         c: str
#         d: datetime.date


    


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
