# Une tus archivos CSV en un solo reporte

¿Cada semana juntas exportaciones de pedidos o inventario a mano? Preparamos un script para consolidar archivos con las mismas columnas y generar un resumen de filas por archivo.

**Adaptación inicial: US$25**, después de confirmar por escrito el alcance. Incluye un formato de entrada acordado, validación con una muestra anonimizada, instrucciones y una corrección dentro del alcance. La fecha de entrega se acuerda antes del pedido. Proyectos mayores se cotizan por separado. PayPal se coordina en privado; no publiques datos de pago.

Escribe a [pruebasprofix@gmail.com](mailto:pruebasprofix@gmail.com?subject=Presupuesto%20CSV) o [pide presupuesto en GitHub](https://github.com/pruebasprofix-glitch/profix-code-services/issues/new?template=work-request.yml). Indica cuántos archivos tienes, sus columnas y qué resultado necesitas. Puedes escribir por correo sin tener cuenta de GitHub. Usa una muestra ficticia o anonimizada; no envíes credenciales ni datos confidenciales. No es necesario pagar para solicitar presupuesto.

## Prueba gratuita

El script de este repositorio se puede usar y adaptar gratuitamente. El servicio de pago es la adaptación y entrega para tu caso particular, no el acceso al código. Se permite usar, copiar, modificar y distribuir este script sin garantía.

Requiere Python 3.10 o posterior. Exporta tus hojas de Excel como CSV UTF-8; esta versión no lee archivos XLSX directamente.

```sh
python consolidate_csv.py enero.csv febrero.csv --output combinado.csv --report resumen.html
```

Para archivos separados por punto y coma añade `--delimiter ";"`. Abre `resumen.html` en tu navegador. Conserva filas repetidas y valores originales; no modifica los archivos de entrada ni calcula ingresos. Rechaza columnas incompatibles y destinos existentes. Carga los datos en memoria: no está diseñada para archivos masivos. Si falla la escritura del reporte, puede quedar el CSV generado; el mensaje de error informa del fallo.

Los valores de los CSV se conservan, incluidas fórmulas si las hubiera: abre en una hoja de cálculo únicamente datos de fuentes de confianza.

## Evidencia y transparencia

Desarrollo asistido por IA, operado por @pruebasprofix-glitch. Las pruebas se ejecutan con `python -m unittest test_consolidate_csv.py`. No hay clientes ni ventas verificadas de este producto todavía. La demostración utiliza datos ficticios.
