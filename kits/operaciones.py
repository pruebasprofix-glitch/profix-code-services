"""Reportes locales de inventario y seguimiento. Python 3.10+, sin dependencias."""
import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


def reporte(tipo, entrada, hoy):
    campos = {'inventario': ['sku', 'producto', 'existencia', 'minimo', 'objetivo'],
              'seguimiento': ['id', 'cliente', 'estado', 'proximo_contacto', 'nota']}[tipo]
    with open(entrada, encoding='utf-8-sig', newline='') as f:
        lector = csv.DictReader(f)
        if lector.fieldnames != campos:
            raise ValueError('Columnas requeridas, en orden: ' + ','.join(campos))
        salida, ids = [], set()
        for n, fila in enumerate(lector, 2):
            if None in fila or any(v is None for v in fila.values()):
                raise ValueError(f'Fila {n}: número de columnas incorrecto')
            fila = {k: v.strip() for k, v in fila.items()}
            clave = fila[campos[0]]
            if not clave or clave in ids:
                raise ValueError(f'Fila {n}: identificador vacío o repetido')
            ids.add(clave)
            if tipo == 'inventario':
                try:
                    actual, minimo, objetivo = (Decimal(fila[k]) for k in campos[2:])
                    if any(not x.is_finite() or x < 0 for x in (actual, minimo, objetivo)) or objetivo < minimo:
                        raise ValueError()
                except (InvalidOperation, ValueError):
                    raise ValueError(f'Fila {n}: cantidades no negativas y objetivo >= mínimo requeridos')
                if actual <= minimo:
                    salida.append({**fila, 'cantidad_sugerida': str(max(Decimal(0), objetivo-actual))})
            else:
                if fila['estado'] not in ('abierto', 'ganado', 'perdido'):
                    raise ValueError(f'Fila {n}: estado debe ser abierto, ganado o perdido')
                try:
                    contacto = date.fromisoformat(fila['proximo_contacto'])
                except ValueError:
                    raise ValueError(f'Fila {n}: fecha requerida YYYY-MM-DD')
                if fila['estado'] == 'abierto' and contacto <= hoy:
                    salida.append({**fila, 'dias_pendientes': str((hoy-contacto).days)})
    extra = 'cantidad_sugerida' if tipo == 'inventario' else 'dias_pendientes'
    return campos + [extra], salida


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('tipo', choices=['inventario', 'seguimiento'])
    p.add_argument('entrada', type=Path)
    p.add_argument('salida', type=Path)
    p.add_argument('--hoy', type=date.fromisoformat, default=date.today())
    a = p.parse_args()
    try:
        if a.entrada.resolve() == a.salida.resolve():
            raise ValueError('Entrada y salida deben ser diferentes')
        campos, filas = reporte(a.tipo, a.entrada, a.hoy)
        with a.salida.open('x', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            # Prevent spreadsheet formula execution in exported text fields.
            for fila in filas:
                w.writerow({k: "'"+v if v.lstrip().startswith(('=', '+', '-', '@')) else v for k,v in fila.items()})
        print(f'{len(filas)} pendientes; reporte: {a.salida}')
    except (ValueError, OSError) as e:
        p.exit(1, f'Error: {e}\n')

if __name__ == '__main__':
    main()
