"""Combine matching CSV exports without modifying originals. Python 3.10+."""
import argparse
import csv
import html
from pathlib import Path


def consolidate(inputs, output, report, delimiter=','):
    paths = [Path(p).resolve() for p in inputs]
    output, report = Path(output).resolve(), Path(report).resolve()
    if len(set(paths)) != len(paths):
        raise ValueError('An input was supplied twice.')
    if output == report or output in paths or report in paths:
        raise ValueError('Outputs must differ from each other and all inputs.')
    if output.exists() or report.exists():
        raise ValueError('Output already exists; choose new filenames.')
    header = None
    rows, counts = [], []
    for path in paths:
        with path.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.reader(stream, delimiter=delimiter, strict=True)
            current = next(reader, None)
            if not current or any(not column.strip() for column in current) or len(set(current)) != len(current):
                raise ValueError(f'{path.name}: missing, blank, or duplicate column names.')
            if header is None:
                header = current
            if current != header:
                raise ValueError(f'{path.name}: column names/order differ from the first input.')
            count = 0
            for row in reader:
                if not row:
                    continue
                if len(row) != len(header):
                    raise ValueError(f'{path.name}: malformed row near line {reader.line_num}.')
                rows.append(row)
                count += 1
            counts.append((path.name, count))
    if header is None:
        raise ValueError('At least one input is required.')
    # Validate every source before creating either output. Never overwrite files.
    with output.open('x', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream, delimiter=delimiter)
        writer.writerow(header)
        writer.writerows(rows)
    summary = ''.join(f'<tr><td>{html.escape(name)}</td><td>{count}</td></tr>' for name, count in counts)
    with report.open('x', encoding='utf-8') as stream:
        stream.write('<!doctype html><html lang="es"><meta charset="utf-8"><title>Consolidación CSV</title>'
                     '<style>body{font:18px system-ui;max-width:760px;margin:48px auto;padding:20px}'
                     'td,th{padding:12px;text-align:left;border-bottom:1px solid #ddd}</style>'
                     f'<h1>Consolidación CSV</h1><p>{len(paths)} archivos · {len(rows)} filas de datos</p>'
                     '<p>Se conservaron los valores y las filas repetidas. No se calcularon ventas ni ingresos.</p>'
                     '<table><tr><th>Archivo</th><th>Filas</th></tr>'+summary+'</table></html>')
    return len(rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('--output', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--delimiter', choices=[',', ';', '\t'], default=',')
    args = parser.parse_args()
    try:
        count = consolidate(args.inputs, args.output, args.report, args.delimiter)
    except (ValueError, OSError, UnicodeError, csv.Error) as exc:
        parser.exit(1, f'Error: {exc}\n')
    print(f'Combined {count} rows. Report: {args.report}')
