    function abrir_modal(url) {
        $('#popup').load(url, function() {
            $(this).modal('show');
        });
        return false;
    }

    function cerrar_clave() {
    }