from pathlib import Path


ALLOWED_EXTENSIONS = {
    ".fasta",
    ".fa",
    ".fastq",
    ".fq"
}


def validate_file_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Format file harus FASTA atau FASTQ"
        )

    return extension
