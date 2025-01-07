from escpos.printer import Win32Raw
import win32print

PRINTER_NAME = "EPSON TM-U950 Slip"

COMMAND_INITIALIZE = b"\x1B\x40"

COMMAND_SELECT_SLIP = b"\x1B\x63\x30\x04"

COMMAND_WAIT_FOR_PAPER = b"\x1B\x76\x01"

def print_slip_cf(header, details):
    try:        
        print(header)
        print(details)
        available_printers = [printer[2] for printer in win32print.EnumPrinters(2)]

        if PRINTER_NAME not in available_printers:
            raise ValueError(f"La impresora '{PRINTER_NAME}' no está disponible.")

        printer = Win32Raw(PRINTER_NAME)

        printer.open()

        printer._raw(COMMAND_INITIALIZE)

        printer._raw(COMMAND_SELECT_SLIP)

        printer._raw(COMMAND_WAIT_FOR_PAPER)

        printer.textln('') #1
        printer.textln('') #2
        printer.textln('') #3
        printer.textln('') #4
        printer.textln('') #5
        printer.textln('') #6
        printer.textln('') #7
        printer.textln('') #8
        printer.textln('') #9
        printer.textln('') #10
        printer.textln(f"              {header['customerFullname']}") #11
        printer.textln(f"               {header['customerAddress']}") #12
        printer.textln(f"{header['docDatetimeForInvoice']:>85}") #13
        printer.textln(f"                    {header['paymentTypeName']}") #14
        printer.textln('') #15
        printer.textln('') #16

        # Imprimir detalles
        for detail in details:
            detailToPrintData = [
                f"{float(detail['quantity'] or 0):>7}" if detail['quantity'] != 0 else f"{'':>7}",  # Si es 0, reemplazar con cadena vacía
                f" {detail['productName'][:37]:<37}",                                   # Nombre del producto limitado a 38 caracteres
                f"{float(detail['unitPrice'] or 0):>7.2f}" if detail['unitPrice'] != 0 else f"{'':>7}",  # Precio unitario
                f"{float(detail['noTaxableSubTotal'] or 0):>7.2f}" if detail['noTaxableSubTotal'] != 0 else f"{'':>7}",  # Subtotal no gravable
                f"{float(detail['taxableSubTotal'] or 0):>7.2f}" if detail['taxableSubTotal'] != 0 else f"{'':>7}"       # Subtotal gravable
            ]

            printer.text("  ")
            line = "     ".join(detailToPrintData)  # Separar columnas con espacios
            printer.textln(line)

        # Agregar líneas en blanco para completar 16 líneas
        print('printing remaining lines')
        remaining_lines = 16 - len(details)
        for _ in range(remaining_lines):
            printer.textln('')

        # Imprimir encabezados
        printer.textln(f"{float(header['taxableSubTotal'] or 0):>88.2f}" if header['taxableSubTotal'] != 0 else f"{'':>88}")  # Subtotal gravable

        printer.text(f"        {header['totalInLetters']:<42}")  # Total en letras

        printer.textln(f"{float(header['noTaxableSubTotal'] or 0):>88.2f}" if header['noTaxableSubTotal'] != 0 else f"{'':>88}")  # Subtotal no gravable
        printer.textln(f"{float(header['saleTotalPaid'] or 0):>88.2f}" if header['saleTotalPaid'] != 0 else f"{'':>88}")         # Total pagado
        printer.textln(f"{float(header['IVAretention'] or 0):>88.2f}" if header['IVAretention'] != 0 else f"{'':>88}")           # Retención IVA
        printer.textln(f"{float(header['total'] or 0):>88.2f}" if header['total'] != 0 else f"{'':>88}")                         # Total general


        printer.print_and_eject_slip()

        printer.close()

        print("Impresión completada con éxito.")
    except Exception as e:
        print(f"Error al imprimir: {e}")
