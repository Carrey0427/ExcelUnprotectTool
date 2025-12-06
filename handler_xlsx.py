# handler_xlsx.py
import zipfile
import tempfile
import os
import shutil
from lxml import etree
from utils import generate_output_name, alert

NS = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def remove_protection(file_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    # 移除 sheetProtection
    for elem in root.xpath("//ns:sheetProtection", namespaces=NS):
        parent = elem.getparent()
        parent.remove(elem)

    # 移除 workbookProtection
    for elem in root.xpath("//ns:workbookProtection", namespaces=NS):
        parent = elem.getparent()
        parent.remove(elem)

    tree.write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=False)

def process_xlsx(filepath: str):
    outpath = generate_output_name(filepath)
    tmpdir = tempfile.mkdtemp()

    # 解壓 Excel
    with zipfile.ZipFile(filepath, "r") as z:
        z.extractall(tmpdir)

    changed = False

    # 處理 worksheets
    ws_dir = os.path.join(tmpdir, "xl", "worksheets")
    if os.path.exists(ws_dir):
        for f in os.listdir(ws_dir):
            if f.endswith(".xml"):
                p = os.path.join(ws_dir, f)
                before = open(p, "rb").read()
                remove_protection(p)
                after = open(p, "rb").read()
                if before != after:
                    changed = True

    # 處理 workbook.xml
    wb_xml = os.path.join(tmpdir, "xl", "workbook.xml")
    if os.path.exists(wb_xml):
        before = open(wb_xml, "rb").read()
        remove_protection(wb_xml)
        after = open(wb_xml, "rb").read()
        if before != after:
            changed = True

    if not changed:
        alert("此檔未受保護或無需移除保護。")
        shutil.rmtree(tmpdir)
        return

    # 重新壓縮成 Excel
    with zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in os.walk(tmpdir):
            for file in files:
                fp = os.path.join(folder, file)
                arc = os.path.relpath(fp, tmpdir)
                z.write(fp, arc)

    shutil.rmtree(tmpdir)
    alert(f"完成！已輸出：\n{outpath}")
