from escpos.printer import Win32Raw
import win32print

PRINTER_NAME = "EPSON TM-U950 Receipt"

COMMAND_SELECT_RECEIPT = b"\x1B\x63\x30\x02"

def print_receipt(text):
    try:
        available_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        if PRINTER_NAME not in available_printers:
            raise ValueError(f"La impresora '{PRINTER_NAME}' no está disponible.")

        printer = Win32Raw(PRINTER_NAME)

        printer._raw(COMMAND_SELECT_RECEIPT)

        printer.text(text)

        printer.cut()

        printer.close()

        print("Impresión completada con éxito.")
    except Exception as e:
        print(f"Error al imprimir: {e}")
