
document.getElementById('nroMesa').addEventListener('keypress', function(e) {
    if (!validText(e)) {
        e.preventDefault();
    }
});

function validText(e) {
    var code = (e.which) ? e.which : e.keyCode;
    return code == 8 || (code >= 48 && code <= 57);
}

async function actas_buscar(form) {
    let nroMesa = document.getElementById('nroMesa').value;

    if (nroMesa == "") {
        alert("Ingrese un número de acta");
        return false;
    }
    if (isNaN(nroMesa)) {
        alert("Ingrese un número de acta válido");
        return false;
    }
    if (nroMesa.length < 6) {
        alert("No es un número de acta válido");
        return false;
    }
    
    form.action = `/actas_numero/${nroMesa}`;
    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('myform');
    if (document.getElementById('systemDate')) {
        document.getElementById('systemDate').textContent = SYSTEM_DATE;
    }
    if (document.getElementById('systemUser')) {
        document.getElementById('systemUser').textContent = SYSTEM_USER;
    }
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (actas_buscar(this)) {
            this.submit();
        }
    });
});