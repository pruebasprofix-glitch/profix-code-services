import tempfile
import unittest
from pathlib import Path
from datetime import date
from operaciones import reporte

class Reportes(unittest.TestCase):
    def ejecutar(self, tipo, contenido):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'datos.csv'
            p.write_text(contenido, encoding='utf-8')
            return reporte(tipo,p,date(2026,9,12))[1]
    def test_limite_y_decimales(self):
        r=self.ejecutar('inventario','sku,producto,existencia,minimo,objetivo\na,A,2.5,2.5,10\nb,B,4,3,10\n')
        self.assertEqual([(x['sku'],x['cantidad_sugerida']) for x in r],[('a','7.5')])
    def test_fechas_y_cerrados(self):
        r=self.ejecutar('seguimiento','id,cliente,estado,proximo_contacto,nota\na,A,abierto,2026-09-12,x\nb,B,ganado,2026-09-01,x\nc,C,abierto,2026-09-13,x\n')
        self.assertEqual([(x['id'],x['dias_pendientes']) for x in r],[('a','0')])
    def test_rechaza_datos_invalidos(self):
        for cantidad in ('NaN','Infinity','-1','texto'):
            with self.subTest(cantidad=cantidad), self.assertRaises(ValueError):
                self.ejecutar('inventario',f'sku,producto,existencia,minimo,objetivo\na,A,{cantidad},2,10\n')
        with self.assertRaises(ValueError):
            self.ejecutar('seguimiento','id,cliente,estado,proximo_contacto,nota\na,A,abierto,2026-02-30,x\n')

if __name__=='__main__': unittest.main()
