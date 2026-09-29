from pathlib import Path

from app.services.statistics import compute_fasta_stats


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

    result = compute_fasta_stats(fasta_file)

    assert result["sequences"] == 3
    assert result["total_length"] == 18
    assert result["min_length"] == 4
    assert result["max_length"] == 8
    assert result["mean_length"] == 6.0
    assert result["gc_percent"] == 66.67