from pathlib import Path
from Bio import SeqIO


def compute_sequence_stats(file_path: Path, file_format: str) -> dict:
    """
    Menghitung statistik sequence dari file FASTA atau FASTQ.
    """

    file_format = file_format.lower()

    if file_format not in {"fasta", "fastq"}:
        raise ValueError("Format sequence harus FASTA atau FASTQ")

    sequences = []

    for record in SeqIO.parse(file_path, file_format):
        sequence = str(record.seq).upper()

        if sequence:
            sequences.append(sequence)

    if not sequences:
        raise ValueError("Tidak ditemukan sequence yang valid")

    lengths = [len(sequence) for sequence in sequences]

    count = len(sequences)
    total_length = sum(lengths)
    min_length = min(lengths)
    max_length = max(lengths)
    mean_length = total_length / count

    gc_count = sum(
        sequence.count("G") + sequence.count("C")
        for sequence in sequences
    )

    gc_percent = 100 * gc_count / total_length

    return {
        "sequences": count,
        "total_length": total_length,
        "min_length": min_length,
        "max_length": max_length,
        "mean_length": round(mean_length, 2),
        "gc_percent": round(gc_percent, 2),
    }