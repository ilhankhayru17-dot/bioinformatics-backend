from pathlib import Path

from app.services.statistics import compute_sequence_stats


def test_compute_fasta_stats(tmp_path):
    fasta_file = tmp_path / "sample.fasta"

    fasta_file.write_text(
        ">seq1\n"
        "ATGCGC\n"
        ">seq2\n"
        "ATGC\n"
        ">seq3\n"
        "ATGCGCGC\n"
    )

    result = compute_sequence_stats(
        fasta_file,
        "fasta"
    )

    assert result["sequences"] == 3
    assert result["total_length"] == 18
    assert result["min_length"] == 4
    assert result["max_length"] == 8
    assert result["mean_length"] == 6.0
    assert result["gc_percent"] == 66.67


def test_compute_fastq_stats(tmp_path):
    fastq_file = tmp_path / "sample.fastq"

    fastq_file.write_text(
        "@seq1\n"
        "ATGCGCATGC\n"
        "+\n"
        "IIIIIIIIII\n"
        "@seq2\n"
        "ATGCATGCATGC\n"
        "+\n"
        "IIIIIIIIIIII\n"
    )

    result = compute_sequence_stats(
        fastq_file,
        "fastq"
    )

    assert result["sequences"] == 2
    assert result["total_length"] == 22
    assert result["min_length"] == 10
    assert result["max_length"] == 12
    assert result["mean_length"] == 11.0
    assert result["gc_percent"] == 54.55


def test_empty_fasta(tmp_path):
    fasta_file = tmp_path / "empty.fasta"

    fasta_file.write_text("")

    import pytest

    with pytest.raises(ValueError):
        compute_sequence_stats(
            fasta_file,
            "fasta"
        )