
function handleRowClick(departamento) {
    window.location.href = `/participacion_total?id=nacional,${departamento}`;
}

function handleMouseOver(element) {
    element.style.cursor = "pointer";
    element.style.backgroundColor = "#f5f5f5";
}

function handleMouseOut(element) {
    element.style.backgroundColor = "";
}

function printContent(elementId) {
    const content = document.getElementById(elementId);
    const printWindow = window.open('', '', 'height=600,width=800');
    
    printWindow.document.write('<html><head><title>Imprimir</title>');
    
    const styles = document.getElementsByTagName('link');
    for(let i = 0; i < styles.length; i++) {
        printWindow.document.write(styles[i].outerHTML);
    }
    printWindow.document.write('</head><body>');
    printWindow.document.write(content.innerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.focus();
    setTimeout(function() {
        printWindow.print();
        printWindow.close();
    }, 250);
}