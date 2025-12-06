# handler_xls.py
import xlrd
from xlutils.copy import copy
from utils import generate_output_name, alert

def process_xls(filepath: str):
    try:
        book = xlrd.open_workbook(filepath, formatting_info=True)
    except:
        alert("無法開啟 .xls 檔案，可能為加密檔案，不支援處理。")
        return

    newfile = generate_output_name(filepath)
    wb = copy(book)

     # 嘗試移除 workbook protect（不同版本 API 不同，因此安全 try）
    try:
        wb._Workbook__wb.protect = False
    except:
        try:
            wb.get_workbook().protect = False
        except:
            pass

    # 移除所有 sheet protect
    for i in range(len(book.sheets())):
        try:
            wb.get_sheet(i).protect = False
        except:
            pass

    wb.save(newfile)
    alert(f"完成！已輸出：\n{newfile}")
