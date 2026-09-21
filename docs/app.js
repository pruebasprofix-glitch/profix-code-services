'use strict';
const services = {
 pages: {name:'Revisión técnica de páginas', price:5, max:5, id:'lst_01M2XVVQZT1EJ5P0D462HJR05X'},
 redirects: {name:'Enlaces y redirecciones', price:7, max:20, id:'lst_01M2XVW62C3PZDEJ4BWR0KRHPN'},
 sitemap: {name:'Revisión de sitemap XML', price:9, max:1, id:'lst_01M2XVW74FH8Z58K95X4X0T4Y0'}
};
const get = id => document.getElementById(id);
function reset(){get('prepared').hidden=true;get('message').textContent='';}
get('service').addEventListener('change',reset);
get('urls').addEventListener('input',reset);
document.querySelectorAll('[data-service]').forEach(a=>a.addEventListener('click',()=>{get('service').value=a.dataset.service;reset();}));
get('request').addEventListener('submit',event=>{
 event.preventDefault();reset();
 const kind=get('service').value,s=services[kind];
 const urls=get('urls').value.trim().split(/\s+/).filter(Boolean);
 try {
  if(!urls.length||urls.length>s.max)throw Error(`Introduce entre 1 y ${s.max} URLs para este servicio.`);
  for(const value of urls){const u=new URL(value);if(value.length>2048||u.protocol!=='https:'||u.username||u.password||u.port||u.hash)throw Error('Usa URLs HTTPS sin credenciales, fragmentos ni puertos distintos de 443.');}
 }catch(error){get('message').textContent=error instanceof TypeError?'Revisa el formato de las URLs.':error.message;return;}
 const input=kind==='sitemap'?{sitemap_url:urls[0]}:{urls};
 const listing='https://api.agentsouk.dev/v1/listings/'+s.id;
 const body=`Hola Profix, solicito ${s.name} (${s.price} USDC en Base).\n\nURLs:\n${urls.join('\n')}\n\nConfirmen alcance e instrucciones de cobro antes de empezar. No he enviado ningún pago.`;
 get('email-text').value=body;
 get('email').href='mailto:pruebasprofix@gmail.com?subject='+encodeURIComponent('Solicitud Profix: '+s.name)+'&body='+encodeURIComponent(body);
 get('agent-text').value=`Contrata ${s.name} con Profix Code Operator. Abre ${listing}, comprueba que está activo y que cuesta ${s.price} USDC en Base. Crea un pedido de una unidad siguiendo how_to_order, con input ${JSON.stringify(input)}. Consulta el pedido hasta recibir la vista previa. Solicita mi autorización para pagar y usa exclusivamente el flujo oficial del pedido para desbloquear el informe. No compartas claves privadas. Si cambian precio o alcance, detente y avísame.`;
 get('listing').href=listing;get('prepared').hidden=false;get('message').textContent='Texto preparado. Todavía no se ha enviado ninguna solicitud.';
});
get('copy').addEventListener('click',async()=>{
 try{await navigator.clipboard.writeText(get('agent-text').value);get('message').textContent='Instrucciones copiadas.';}
 catch{get('agent-text').focus();get('agent-text').select();get('message').textContent='Seleccioné el texto. Cópialo manualmente.';}
});
