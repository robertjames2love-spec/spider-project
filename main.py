import time

from excel_util import ExcelUtil
from api_util import ApiUtil
if ApiUtil().auth():
    ExcelUtil().read_excel()
else:
    print('授权失败')
time.sleep(1000)
