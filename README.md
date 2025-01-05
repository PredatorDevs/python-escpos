# Sistema de Impresión con TM-U950

Este proyecto implementa un sistema de impresión para la impresora Epson TM-U950, utilizando Python y el framework Flask. Proporciona endpoints para manejar la impresión en diferentes formatos (Slip y Receipt).

## Características

- **Receipts**: Imprime tickets en el formato Receipt.
- **Slips (CF y CCF)**: Imprime slips configurados como Comprobante de Crédito Fiscal (CCF) o Comprobante Fiscal (CF).
- Basado en comandos ESC/POS para la comunicación con la impresora.

---

## Requisitos Previos

1. **Python 3.x** instalado.
2. **Entorno virtual** para el aislamiento del proyecto:
    ```bash
    python -m venv venv
    ```
3. Instalar las dependencias desde el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
4. Configurar una impresora Epson TM-U950 conectada al sistema.

---

## Archivos del Proyecto

### **1. `main.py`**
- Inicializa el servidor Flask.
- Define los endpoints para manejar la impresión:
  - `/print/slip/cf`: Imprime un Slip (Comprobante Fiscal).
  - `/print/slip/ccf`: Imprime un Slip (Comprobante de Crédito Fiscal).
  - `/print/receipt/ticket`: Imprime un Receipt.

### **2. `print_slip_cf.py`**
- Define la lógica para imprimir Slips en formato Comprobante Fiscal.

### **3. `print_slip_ccf.py`**
- Define la lógica para imprimir Slips en formato Comprobante de Crédito Fiscal.

### **4. `print_receipt.py`**
- Define la lógica para imprimir Receipts en formato Ticket.

---

## Ejecución del Proyecto

1. **Activar el entorno virtual**:
    ```bash
    source venv/bin/activate  # En Linux/Mac
    .\venv\Scripts\activate   # En Windows
    ```

2. **Ejecutar el servidor**:
    ```bash
    python main.py
    ```

3. **Enviar solicitudes a los endpoints**:
    - Usa herramientas como Postman o `curl` para enviar datos de prueba a los endpoints.

---

## Endpoints Disponibles

1. **Imprimir Slip CF**
    ```http
    POST /print/slip/cf
    Content-Type: application/json
    {
      "header": { ... },
      "details": [ ... ]
    }
    ```

2. **Imprimir Slip CCF**
    ```http
    POST /print/slip/ccf
    Content-Type: application/json
    {
      "header": { ... },
      "details": [ ... ]
    }
    ```

3. **Imprimir Receipt**
    ```http
    POST /print/receipt/ticket
    Content-Type: application/json
    {
      "text": "Texto a imprimir"
    }
    ```

---

## Notas Importantes

- **Comandos ESC/POS**:
  - Este proyecto utiliza comandos específicos para la impresora Epson TM-U950.
  - Asegúrate de que la impresora esté configurada correctamente en el sistema operativo.

- **Pruebas Locales**:
  - El proyecto corre en `localhost` (puerto 5005 por defecto).

- **Errores Comunes**:
  - Si la impresora no está disponible, verifica la conexión o el nombre configurado en los archivos `print_*.py`.

---

## Contribuciones

Si deseas contribuir al proyecto, por favor crea un fork y envía un pull request con tus mejoras.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
