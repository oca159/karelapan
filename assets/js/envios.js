$(document).ready(function(){
    $('.casos-evaluacion').click(function(evt){
        var tabla_casos = $(this).closest('td').find('table.tabla-casos');
        if($(tabla_casos).css('display') == 'none'){
            $(tabla_casos).show('slow');
        } else {
            $(tabla_casos).hide('slow');
        }
    });
    $('.casos-pendiente').popover({
        'html': true,
        'placement': 'top',
        'trigger': 'click',
        'content': 'Este envío no ha sido evaluado'
    });
});
