import tempfile
import datetime
import os
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog


def save_temp_workbook(workbook) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    tmp_path = os.path.join(tempfile.gettempdir(), f"PhieuThu_{timestamp}.xlsx")
    workbook.save(tmp_path)
    return tmp_path


def select_printer_name(self) -> str | None:
    """
    Mở hộp thoại chọn máy in của Windows (thông qua Qt),
    trả về tên máy in hoặc None nếu hủy.
    """
    printer = QPrinter()
    dlg = QPrintDialog(printer, self)
    if dlg.exec():
        return printer.printerName()
    return None


def print_with_excel(file_path: str, printer_name: str | None = None, copies: int = 1):
    """
    In file Excel bằng COM (yêu cầu Excel cài trên máy).
    - printer_name: tên máy in Windows (ví dụ 'Microsoft Print to PDF' hoặc tên máy in thật).
    """
    try:
        import win32com.client as win32
        import pythoncom
        pythoncom.CoInitialize()  # đảm bảo init COM trong thread hiện tại

        excel = win32.DispatchEx("Excel.Application")
        excel.Visible = False
        # Mở read-only, không update links, không đặt alert
        wb = excel.Workbooks.Open(file_path, ReadOnly=True, UpdateLinks=False)
        excel.DisplayAlerts = False
        try:
            if printer_name:
                # Lưu ý: tên phải đúng chính xác như trong Windows Printers & Scanners
                excel.ActivePrinter = printer_name
            # Tuỳ chọn setup để vừa một trang ngang (nếu muốn)
            try:
                sht = wb.Worksheets(1)
                sht.PageSetup.Zoom = False
                sht.PageSetup.FitToPagesWide = 1
                sht.PageSetup.FitToPagesTall = False
                sht.PageSetup.Orientation = 1  # 1=Portrait, 2=Landscape (nếu cần)
            except Exception:
                pass

            wb.PrintOut(Copies=copies)  # có thể thêm: ActivePrinter=printer_name
        finally:
            wb.Close(SaveChanges=False)
            excel.Quit()
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass