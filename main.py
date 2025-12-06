# main.py
import os, sys
sys.path.append(os.path.dirname(__file__))
from tkinter import Tk, filedialog
from utils import get_ext, alert, is_encrypted
from handler_xlsx import process_xlsx
from handler_xls import process_xls

def handle_file(filepath: str):
    if is_encrypted(filepath):
        alert("不支援加密開啟保護的檔案。")
        return

    ext = get_ext(filepath)

    if ext in [".xlsx", ".xlsm"]:
        process_xlsx(filepath)
    elif ext == ".xls":
        process_xls(filepath)
    else:
        alert("不支援的檔案格式。")

def run():
    # 支援拖曳啟動
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        handle_file(filepath)
        return

    # GUI 選擇檔案
    root = Tk()
    root.withdraw()
    file = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls *.xlsm")])

    if file:
        handle_file(file)
    else:
        alert("未選取任何檔案。")

if __name__ == "__main__":
    run()
