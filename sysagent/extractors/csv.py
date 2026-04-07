import csv


def _extract_csv(path):
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open(encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        rows = []
        for row in reader:
            cells = [cell.strip() for cell in row if cell.strip()]
            if cells:
                rows.append("\t".join(cells))
        return "\n".join(rows)
