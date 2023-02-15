# Ideas Proyecto Regionales

- [ ] Crear modelo productos - proveedor/stock
- [ ] Crear modelo pedidos
- [ ] Crear modelo periodos

## Lógica

### Cosas a tener en cuenta:  

- Cada mes se debe actualizar los precios de los productos con el proveedor.  Así, cambiarán todos los precios automaticamente.  

    Por ejemplo, los precios de las promos que incluyen productos los cuales su precio fué incrementado tambien aumentarán porque siempre se toman los precios en referencia a la base de datos de Artículos del proveedor.  
    Pasará lo mismo con los precios de los artículos de la tabla stock y demás.

- No se debe cambiar el precio de los productos de los pedidos ya realizados.  

    Si el pedido se realiza en una fecha y el cambio de precio del proveedor es posterior a esta misma, ¡el precio de venta que ya fue comunicado al cliente no debe cambiar!  

    Para ello, cuando cambie un precio en la tabla de artículos del proveedor, se actualizaran las siguientes tablas:  
  - Tabla stock.
  - Tabla Promos.  

  No se debe actualizar la tabla completa de Pedidos de manera automática (¡NUNCA!); solo se toman los nuevos datos del nuevo pedido en la tabla Pedidos pero no se actualiza completa para que no modifique el precio de otros pedidos anteriormente realizados.
