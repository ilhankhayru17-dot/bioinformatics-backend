import logging
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.validation import validate_file_extension


logger = logging.getLogger("bioinformatics")

router = APIRouter(
    prefix="/api",
    tags=["Upload"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Nama file tidak ditemukan"
        )

    try:
        extension = validate_file_extension(
            file.filename
        )

    except ValueError as error:
        logger.error(str(error))

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    file_path = UPLOAD_DIR / file.filename

    content = await file.read()

    if not content:
        logger.error(
            "File kosong: %s",
            file.filename
        )

        raise HTTPException(
            status_code=400,
            detail="File kosong"
        )

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    logger.info(
        "File uploaded: %s",
        file.filename
    )

    return {
        "filename": file.filename,
        "format": extension.replace(".", ""),
        "status": "uploaded"
    }