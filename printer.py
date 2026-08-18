"""Windows printer handling."""

import logging

import win32print

from config import PRINTER_NAME


logger = logging.getLogger(__name__)


def is_printer_available() -> bool:
    """Return True when the configured printer exists in Windows."""

    try:
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL
            | win32print.PRINTER_ENUM_CONNECTIONS
        )

        printer_names = {
            printer[2]
            for printer in printers
        }

        return PRINTER_NAME in printer_names

    except Exception:
        logger.exception("Failed to enumerate Windows printers")
        return False


def print_zpl(zpl: str) -> None:
    """Send ZPL directly to the configured printer."""

    if not zpl.strip():
        raise ValueError("ZPL content cannot be empty.")

    if not is_printer_available():
        raise RuntimeError(
            f"Printer '{PRINTER_NAME}' is not available."
        )

    printer_handle = None

    try:
        logger.info(
            "Sending print job to printer '%s'",
            PRINTER_NAME,
        )

        printer_handle = win32print.OpenPrinter(PRINTER_NAME)

        win32print.StartDocPrinter(
            printer_handle,
            1,
            ("QR Print Job", None, "RAW"),
        )

        try:
            win32print.StartPagePrinter(printer_handle)

            try:
                win32print.WritePrinter(
                    printer_handle,
                    zpl.encode("utf-8"),
                )

            finally:
                win32print.EndPagePrinter(printer_handle)

        finally:
            win32print.EndDocPrinter(printer_handle)

        logger.info("Print job sent successfully.")

    except Exception:
        logger.exception("Failed to print ZPL")
        raise

    finally:
        if printer_handle is not None:
            win32print.ClosePrinter(printer_handle)