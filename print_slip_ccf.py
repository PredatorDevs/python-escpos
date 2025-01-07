from escpos.printer import Win32Raw
import win32print

PRINTER_NAME = "EPSON TM-U950 Slip"

COMMAND_INITIALIZE = b"\x1B\x40"

COMMAND_SELECT_SLIP = b"\x1B\x63\x30\x04"

COMMAND_WAIT_FOR_PAPER = b"\x1B\x76\x01"

def print_slip_ccf(header, details):
    try:
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
        printer.textln(f"{(header['docDatetimeForPrint'] or ""):>85}") #8
        printer.textln('') #9
        printer.text(f"              {(header['customerFullname'] or "-")[:30]:<30}") #10
        printer.textln(f"{(header['customerDepartmentName'] or "-")[:24]:>40}") #10
        printer.text(f"               {(header['customerAddress'] or "-")[:29]:<29}") #11
        printer.textln(f"{(header['customerNrc'] or "-")[:24]:>40}") #11
        printer.text(f"          {(header['customerNit'] or "-")[:17]:<17}") #12
        printer.text(f"{(header['customerCityName'] or "-")[:19]:>19}") #12
        printer.textln(f"{(header['customerEconomicActivityName'] or "-")[:40]:>40}") #12
        printer.textln(f"                              {(header['paymentTypeName'] or "")}") #13
        printer.textln('') #14
        printer.textln('') #15
        printer.textln('') #16
        printer.textln('') #17

        # Imprimir detalles
        for detail in details:
            detailToPrintData = [
                f"  {detail['quantity']:>7}" if detail['quantity'] != 0 else f"  {'':>7}",  # Si es 0, reemplazar con cadena vacía
                f"    {detail['productName'][:34]:<34}",                                   # Nombre del producto limitado a 38 caracteres
                f"{detail['unitPriceNoTaxes']:>7.2f}" if detail['unitPriceNoTaxes'] != 0 else f"{'':>7}",  # Precio unitario
                " " * 14,
                # f"{'0.01':>7}",
                f"{detail['noTaxableSubTotal']:>7.2f}" if detail['noTaxableSubTotal'] != 0 else f"{'':>7}",  # Subtotal no gravable
                f"{detail['taxableSubTotalWithoutTaxes']:>7.2f}" if detail['taxableSubTotalWithoutTaxes'] != 0 else f"{'':>10}"       # Subtotal gravable
            ]

            line = " ".join(detailToPrintData)
            printer.textln(line)

        # Agregar líneas en blanco para completar 16 líneas
        remaining_lines = 13 - len(details)
        for _ in range(remaining_lines):
            printer.textln('')

        # Imprimir encabezados
        printer.textln(f"{header['taxableSubTotalWithoutTaxes']:>88.2f}" if header['taxableSubTotalWithoutTaxes'] != 0 else f"{'':>88}")  # Subtotal gravable

        printer.text(f"        {header['totalInLetters'][:34]:<34}")  # Total en letras

        printer.textln(f"{'':>46}")
        printer.textln(f"{header['noTaxableSubTotal']:>88.2f}" if header['noTaxableSubTotal'] != 0 else f"{'':>88}")  # Subtotal no gravable
        printer.textln(f"{(header['taxableSubTotalWithoutTaxes'] + header['noTaxableSubTotal']):>88.2f}" if header['total'] != 0 else f"{'':>88}")         # Total pagado
        printer.textln(f"{header['ivaTaxAmount']:>88.2f}" if header['ivaTaxAmount'] != 0 else f"{'':>88}")           # Retención IVA
        printer.textln(f"{header['IVAretention']:>88.2f}" if header['IVAretention'] != 0 else f"{'':>88}")           # Retención IVA
        printer.textln(f"{(header['total'] - header['IVAretention']):>88.2f}")                         # Total general
        # printer.textln(f"{header['total']:>88.2f}" if header['total'] != 0 else f"{'':>88}")                         # Total general

        printer.print_and_eject_slip()

        printer.close()

        print("Impresión completada con éxito.")
    except Exception as e:
        print(f"Error al imprimir: {e}")
