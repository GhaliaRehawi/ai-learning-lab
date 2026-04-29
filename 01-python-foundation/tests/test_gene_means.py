# tests/gene_means.py
import textwrap
from pathlib import Path
import pytest
from exercises.gene_means import gene_means

@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    p = tmp_path / "expression.csv"
    p.write_text(textwrap.dedent("""\
        sample_id,gene,expression
        S001,TP53,12.5
        S001,MYC,8.1
        S002,TP53,11.7
        S002,MYC,9.3
    """))
    return p

def test_gene_means_basic(sample_csv):
    result = gene_means(str(sample_csv))
    assert result["TP53"] == pytest.approx(12.1)
    assert result["MYC"] == pytest.approx(8.7)

def test_handles_single_row(tmp_path: Path):
    p = tmp_path / "singlerow.csv"
    p.write_text("sample_id,gene,expression\nS002,MYC,9.3\n")
    result = gene_means(str(p))
    assert result["MYC"] == pytest.approx(9.3)


@pytest.mark.parametrize("gene,value", [
    ("TP53", 12.4),
    ("MYC", 8.1),
    ("FOXP3", 0.0),
    ("ACTB", -3.5),     # negatives must also work
])
def test_constant_value_yields_that_value(tmp_path: Path, gene: str, value: float):
    p = tmp_path / "const.csv"
    rows = "\n".join(f"S{i:03d},{gene},{value}" for i in range(1, 6))
    p.write_text(f"sample_id,gene,expression\n{rows}\n")

    result = gene_means(str(p))
    assert result[gene] == pytest.approx(value)
    assert len(result) == 1
