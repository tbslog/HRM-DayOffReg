import pandas as pd
from fastapi import FastAPI,HTTPException,Depends, Form
import pyodbc
import json
import uvicorn
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from security import validate_token
import functions as fn




cn = fn.cn
app = FastAPI()


@app.get('/')
async def home():
    return f"Đây là FastAPI token: {fn.generate_token('kieu.pham',30)}"

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}



# Tạo class
class LoginRequest(BaseModel):
    username: str
    password: str
@app.post('/getToken')
def getToken(request_data: LoginRequest):  #truyền vào class LoginRequest
    print(f'[x] request_data: {request_data.__dict__}')
    if fn.verify_password(username=request_data.username, password=request_data.password):
        token = fn.generate_token(request_data.username,30)  # 30 ngày
        return {
            'token': token
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


# token
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzQ0NTYwNTUsInVzZXJuYW1lIjoia2lldS5waGFtIn0.VB0nKOrTpTba4hx4525Y46rNbfeHklOVcT9VoAgTrHM

# 1. Đọc dữ liệu
# ----------------------------------------------------------------------------------------------------------------------
@app.get('/dsChucDanh', dependencies=[Depends(validate_token)])
async def dsChucDanh():
    s = f"""
                SELECT * FROM dbo.hsseChucDanh
            """
    cursor = cn.cursor()
    rows = cursor.execute(s).fetchall()
    df = pd.DataFrame([tuple(t) for t in rows], columns=['Mã chức danh', 'Tên chức danh'])
    return (df.to_dict('dict'))     # trả về dạng json (bắt buộc)
# ----------------------------------------------------------------------------------------------------------------------





# 2. Thêm dữ liệu
# ----------------------------------------------------------------------------------------------------------------------
# Tạo class
class ThongTin(BaseModel):
    MaNV: str
    HoTen: str
    QueQuan: str
    Vitricongviec: str

@app.post('/themChucDanh', dependencies=[Depends(validate_token)])
async def themChucDanh(request_data: ThongTin):
    cursor = cn.cursor()
    insert_records = f'''
        insert into dbo.Nhat(MaNV, HoTen, QueQuan, Vitricongviec ) 
        values 
        ('{request_data.MaNV}', N'{request_data.HoTen}', N'{request_data.QueQuan}', N'{request_data.Vitricongviec}')
        '''
    cursor.execute(insert_records)
    cn.commit()

#     Cách 2
@app.post('/themChucDanh1', dependencies=[Depends(validate_token)])
async def themChucDanh1(request_data: ThongTin):
    cursor = cn.cursor()
    s = f'''
        insert into dbo.Nhat(MaNV, HoTen, QueQuan, Vitricongviec ) values (?, ?, ?, ?)
        '''
    cursor.execute(s,request_data.MaNV,request_data.HoTen,request_data.QueQuan,request_data.Vitricongviec)
    cn.commit()
# ----------------------------------------------------------------------------------------------------------------------


# 3. Cập nhật dữ liệu
# ----------------------------------------------------------------------------------------------------------------------
@app.post('/capNhatThongTin', dependencies=[Depends(validate_token)])
async def capNhatThongTin(request_data: ThongTin):
    cursor = cn.cursor()
    insert_records = f'''
        UPDATE dbo.Nhat SET HoTen=?, QueQuan=?, Vitricongviec=? WHERE MaNV=?
    '''
    cursor.execute(insert_records,request_data.HoTen, request_data.QueQuan, request_data.Vitricongviec,request_data.MaNV)
    cn.commit()
# ----------------------------------------------------------------------------------------------------------------------


# 4. Xóa dữ liệu
# ----------------------------------------------------------------------------------------------------------------------
@app.post('/xoaThongTin', dependencies=[Depends(validate_token)])
def xoaThongTin(maNV):
    cursor = cn.cursor()
    s = f'''DELETE FROM dbo.Nhat where MaNV=? '''
    cursor.execute(s,maNV)
    cn.commit()
# ----------------------------------------------------------------------------------------------------------------------


# 5. chạy nhiều lệnh trong SQL Server (Procedure)
@app.post('/run_procedure', dependencies=[Depends(validate_token)])
def run_procedure(manv):
    s = f"""
            SET NOCOUNT ON;
            DECLARE @count SMALLINT

            BEGIN
                SET @count=(SELECT COUNT(*) FROM dbo.Nhat WHERE MaNV={manv})
                IF @count>0
                    SELECT N'Tồn tại' AS KQ
                ELSE
                    SELECT N'Không tồn tại' AS KQ
            END;
        """
    cursor = cn.cursor()
    cursor.execute(s)
    rows = cursor.fetchall()
    # df = pd.DataFrame([tuple(t) for t in rows], columns=['Kết quả'])
    return ({'Kết quả': rows[0][0]})  # trả về dạng json (bắt buộc)