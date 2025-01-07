from escpos.printer import Win32Raw
import win32print

PRINTER_NAME = "EPSON TM-U950 Receipt"

COMMAND_INITIALIZE = b"\x1B\x40"

COMMAND_SELECT_RECEIPT = b"\x1B\x63\x30\x02"

COMMAND_FULL_CUT = b"\x1dV\x00"
COMMAND_PARTIAL_CUT = b"\x1B\x6D"

def print_receipt(text):
    try:
        available_printers = [printer[2] for printer in win32print.EnumPrinters(2)]

        if PRINTER_NAME not in available_printers:
            raise ValueError(f"La impresora '{PRINTER_NAME}' no está disponible.")

        printer = Win32Raw(PRINTER_NAME)

        printer.open()

        printer._raw(COMMAND_INITIALIZE)

        printer._raw(COMMAND_SELECT_RECEIPT)

        printer.text(text)

        printer._raw(COMMAND_FULL_CUT)

        printer.cut(mode='FULL',feed=True)

        printer.close()

        print("Impresión completada con éxito.")
    except Exception as e:
        print(f"Error al imprimir: {e}")
