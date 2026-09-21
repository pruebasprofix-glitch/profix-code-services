# Customer support writing — English / Español

Original portfolio samples by Profix Code Operator, operated by pruebasprofix-glitch with AI assistance. These are fictional examples, not client work or certified translations. Placeholders must be replaced using the client's actual policies; no refund, delivery date or account change is promised without confirmation.

## 1. Duplicate charge: acknowledgement and next step

**English**

Hi [name],

Thanks for flagging the two charges. Please send the order number and the dates and amounts shown on your statement. Do not send your full card number or a bank statement; those details are not needed for this check.

We'll check whether both entries are completed charges or whether one is a pending authorization. Once that is confirmed, we'll explain the next step under our billing policy.

[Support name]

**Español**

Hola, [nombre]:

Gracias por avisarnos de los dos cargos. Envíanos el número de pedido y las fechas e importes que aparecen en tu estado de cuenta. No envíes el número completo de tu tarjeta ni tu estado de cuenta bancario; no los necesitamos para esta revisión.

Comprobaremos si ambos movimientos son cargos completados o si uno es una autorización pendiente. Cuando lo confirmemos, te explicaremos el siguiente paso conforme a nuestra política de facturación.

[Nombre del equipo de soporte]

## 2. A feature request we cannot promise

**English**

Hi [name],

I understand that [missing capability] makes it harder to [customer's task]. This feature is not currently available, and we do not have a confirmed release date to share.

If you tell us which step is blocking you, we can check whether an existing feature offers a workable alternative. We'll also record your use case for the product team.

[Support name]

**Español**

Hola, [nombre]:

Entiendo que no contar con [función solicitada] dificulta [tarea del cliente]. Esa función todavía no está disponible y no tenemos una fecha de lanzamiento confirmada.

Cuéntanos en qué paso te atoras para comprobar si alguna función existente puede ayudarte. También registraremos tu caso para el equipo de producto.

[Nombre del equipo de soporte]

## 3. Technical explanation in plain language

**Technical source, written for this sample:**
The request timed out before the client received an acknowledgement. Retry with the same idempotency key after checking the operation status to avoid duplicate writes.

**Plain English:**
The app stopped waiting before it received a reply. That does not prove the action failed. First check whether it already completed. If a retry is needed, reuse the same request identifier so a supported service can recognize the retry instead of treating it as a new action.

**Español claro:**
La aplicación dejó de esperar antes de recibir una respuesta. Eso no demuestra que la operación haya fallado. Primero comprueba si ya terminó. Si debes intentarlo de nuevo, reutiliza el mismo identificador de solicitud para que un servicio compatible pueda reconocer el reintento en lugar de tratarlo como una operación nueva.

## Review notes

- Pending authorization is not translated as a completed or duplicate payment.
- No unverified refund eligibility, processing deadline or release commitment is invented.
- The technical rewrite preserves uncertainty: a timeout does not prove failure.
- Idempotency is conditional on service support; it is not presented as a universal guarantee.
- Spanish uses a consistent informal singular voice; a client can request formal usted or a regional glossary.

## Available scope

Small paid pilot: two short support templates, English and Spanish, up to 300 source words total, one revision against a supplied policy, 5 USDC in Base after scope and payment terms are agreed. No live inbox handling is included. General written content only; not certified/legal/medical translation.
