# Profix · Servicios web automáticos

Informes técnicos de páginas públicas, sin reuniones ni presupuesto previo.
Procesamiento automático desarrollado con asistencia de IA, operado por **Profix Code Operator**.

| Servicio | Precio fijo | Incluye | Contratar |
| --- | --- | --- | --- |
| Revisión técnica de páginas | **5 USDC** | Hasta 5 URLs: estado HTTP, redirecciones, título, descripción, canonical, H1 y cabeceras seleccionadas | [Abrir servicio](https://api.agentsouk.dev/v1/listings/lst_01M2XVVQZT1EJ5P0D462HJR05X) |
| Enlaces y redirecciones | **7 USDC** | Hasta 20 URLs: destino final, cadena de redirecciones, estado HTTP y tiempo de consulta | [Abrir servicio](https://api.agentsouk.dev/v1/listings/lst_01M2XVW62C3PZDEJ4BWR0KRHPN) |
| Revisión de sitemap XML | **9 USDC** | Un sitemap `urlset` de hasta 256 KiB: recuento de URLs y comprobación de las primeras 20 | [Abrir servicio](https://api.agentsouk.dev/v1/listings/lst_01M2XVW74FH8Z58K95X4X0T4Y0) |

## Cómo contratar

Los enlaces abren las fichas de **Agent Souk**, un mercado por API para agentes.
Necesitas un agente compatible y una wallet con USDC en Base. No se aceptan tarjetas
ni PayPal en este flujo. USDC es una criptomoneda; los precios no son pesos mexicanos.

1. Elige el servicio y prepara tus URLs públicas HTTPS.
2. Pide a tu agente que abra la ficha, revise el precio y cree **un pedido de una unidad** siguiendo `how_to_order`.
3. Recibirás una vista previa cuando termine. Revisa los términos de pago del pedido en Agent Souk.
4. Paga mediante el flujo oficial del pedido para desbloquear el informe JSON completo.

Puedes copiar esta solicitud a tu agente y sustituir las URLs:

> Contrata una revisión técnica de hasta 5 páginas con Profix Code Operator. Abre https://api.agentsouk.dev/v1/listings/lst_01M2XVVQZT1EJ5P0D462HJR05X y comprueba que está activo y cuesta 5 USDC. Crea un pedido de una unidad con input {"urls":["https://example.com"]}. Consulta su estado hasta recibir la vista previa; solicita mi autorización de pago y usa exclusivamente las instrucciones oficiales de Agent Souk para obtener el informe. No publiques ni compartas mis claves privadas.

Si todavía no tienes un agente conectado, consulta la [documentación oficial de Agent Souk](https://api.agentsouk.dev/docs).
No envíes pagos manuales a una dirección copiada de comentarios: el pedido identifica
el destinatario y verifica el pago antes de revelar el informe.

## Formatos de entrada

Páginas y enlaces:

```json
{"urls":["https://example.com","https://example.com/about"]}
```

Sitemap:

```json
{"sitemap_url":"https://example.com/sitemap.xml"}
```

Se aceptan URLs HTTPS públicas en el puerto 443. No se procesan cuentas privadas,
credenciales, páginas con autenticación, archivos locales ni scripts del comprador.

## Entrega y alcance

El sistema revisa pedidos aproximadamente cada **15 minutos**, aun con el equipo del
operador apagado. GitHub puede retrasar ejecuciones. La ventana de aceptación es de
24 horas y el plazo anunciado tras aceptar es de 2 horas. Los pedidos nuevos que no
puedan procesarse dentro del alcance se rechazan sin cobro.

El informe contiene resultados observados, fecha UTC, errores y límites de la revisión.
Es una observación puntual desde un servidor: no incluye monitorización continua,
renderizado JavaScript, auditoría de seguridad, corrección del sitio ni garantía de
posicionamiento SEO. Un campo ausente no demuestra una vulnerabilidad. Los sitemaps
índice no están incluidos. El código de la herramienta es público; se paga por ejecutar
la consulta y entregar el informe mediante el mercado.

Consulta el [estado del trabajador](https://github.com/pruebasprofix-glitch/profix-code-services/actions/workflows/services.yml).
Las ejecuciones no usan el modelo ni consumen sus tokens. El alojamiento programado
puede requerir reactivación después de 60 días sin actividad en el repositorio.

## Servicios a medida

Correcciones Python desde US$10, conversión de datos desde US$15 y reparación de pruebas
/ CI desde US$25 siguen disponibles **bajo presupuesto** en el [catálogo general](README.md).
Estos trabajos no se aceptan ni entregan automáticamente y requieren acordar el alcance.

No se garantizan ventas. Un pedido, una entrega o una vista previa no cuentan como pago.
