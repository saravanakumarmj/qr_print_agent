"""QR Print Agent."""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from config import HOST, PORT, PRINTER_NAME
from printer import is_printer_available, print_zpl


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("qr_print_agent")


app = FastAPI(
    title="QR Print Agent",
    version="1.0.0",
)


class PrintRequest(BaseModel):
    """Incoming print request."""

    zpl: str = Field(
        ...,
        min_length=1,
        description="Raw ZPL to send to the printer.",
    )


@app.get("/health")
def health() -> dict:
    """Return agent and printer status."""

    printer_available = is_printer_available()

    return {
        "agent": "online",
        "printer": PRINTER_NAME,
        "printer_available": printer_available,
    }


@app.post("/print")
def print_label(request: PrintRequest) -> dict:
    """Send ZPL to the configured Windows printer."""

    if not is_printer_available():
        raise HTTPException(
            status_code=503,
            detail=(
                f"Printer '{PRINTER_NAME}' "
                "is not available."
            ),
        )

    try:
        print_zpl(request.zpl)

        return {
            "success": True,
            "message": "Print sent successfully.",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Print request failed")

        raise HTTPException(
            status_code=500,
            detail=f"Print failed: {exc}",
        ) from exc


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting QR Print Agent")
    logger.info("Printer: %s", PRINTER_NAME)
    logger.info("Listening on: %s:%s", HOST, PORT)

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info",
    )