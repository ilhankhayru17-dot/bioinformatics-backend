import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.services.statistics import compute_fasta_stats


logger = logging.getLogger("bioinformatics")


router = APIRouter(
    prefix="/api",
    tags=["Analysis"]
)

UPLOAD_DIR = Path("uploads")


@router.post("/analyze")
def analyze_file(
    filename: str,
    output_format: str = "json"
):

    logger.info("Starting analysis: %s", filename)

    file_path = UPLOAD_DIR / filename

    # Cek file
    if not file_path.exists():
        logger.error("File not found: %s", filename)

        raise HTTPException(
            status_code=404,
            detail=f"File '{filename}' tidak ditemukan"
        )

    # Cek format output
    if output_format not in ["json", "tsv"]:
        logger.error(
            "Invalid output format: %s",
            output_format
        )

        raise HTTPException(
            status_code=400,
            detail="output_format harus json atau tsv"
        )

    try:
        stats = compute_fasta_stats(file_path)

    except ValueError as error:
        logger.error(
            "Analysis failed: %s",
            error
        )

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    logger.info(
        "Analysis completed: %s",
        filename
    )

    # JSON
    if output_format == "json":
        return {
            "filename": filename,
            **stats
        }

    # TSV
    tsv = (
        "filename\tsequences\ttotal_length\tmin_length\t"
        "max_length\tmean_length\tgc_percent\n"
    )

    tsv += (
        f"{filename}\t"
        f"{stats['sequences']}\t"
        f"{stats['total_length']}\t"
        f"{stats['min_length']}\t"
        f"{stats['max_length']}\t"
        f"{stats['mean_length']}\t"
        f"{stats['gc_percent']}\n"
    )

    return PlainTextResponse(
        content=tsv,
        media_type="text/tab-separated-values"
    )