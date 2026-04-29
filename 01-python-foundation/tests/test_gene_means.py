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
        S001,TP53,12.4
        S001,MYC,8.1
        S002,TP53,11.7
        S002,MYC,9.3
    """))
    return p

def test_gene_means_basic(tmp_path: Path):
    result = gene_means(str(tmp_path / "expression.csv"))
    pytest.approx(result["TP53"], 12.05)
    pytest.approx(result["MYC"], 8.1)

def test_handles_single_row(tmp_path: Path):
    p = tmp_path / "singlerow.csv"
    p.write_text("sample_id,gene,expression\nS002,MYC,9.3\n")
    result = gene_means(str(p))
    pytest.approx(result["MYC"], 9.3)


@pytest.mark.parametrize("constant_expressions.csv",
                         ("""\
                         sample_id,gene,expression
                         S001,TP53,12.4
                         S002,TP53,12.4
                         S003,TP53,12.4
                         """,
                          """\
                          sample_id,gene,expression
                          S001,P53,8.1
                          S002,P53,8.1
                          S003,P53,8.1
                          """,
                          """\
                          sample_id,gene,expression
                          S001,MYC,8.2
                          S002,MYC,8.2
                          S003,MYC,8.2
                          """))
def test_mean_across_constant(tmp_path: Path):
    result = gene_means(str(tmp_path / "constant_expressions.csv"))
    pytest.approx(result["TP53"], 12.4)
    pytest.approx(result["P53"], 8.1)
    pytest.approx(result["key"], 8.2)
