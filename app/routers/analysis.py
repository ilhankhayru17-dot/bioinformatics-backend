import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.services.statistics import compute_sequence_stats


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

    # Tentukan format berdasarkan ekstensi file
    extension = file_path.suffix.lower()

    if extension in [".fasta", ".fa"]:
        file_format = "fasta"

    elif extension in [".fastq", ".fq"]:
        file_format = "fastq"

    else:
        logger.error(
            "Unsupported sequence format: %s",
            extension
        )

        raise HTTPException(
            status_code=400,
            detail="Format file harus FASTA atau FASTQ"
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
        stats = compute_sequence_stats(
            file_path,
            file_format
        )

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
            "format": file_format,
            **stats
        }

    # TSV
    tsv = (
        "filename\tformat\tsequences\ttotal_length\t"
        "min_length\tmax_length\tmean_length\tgc_percent\n"
    )

    tsv += (
        f"{filename}\t"
        f"{file_format}\t"
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