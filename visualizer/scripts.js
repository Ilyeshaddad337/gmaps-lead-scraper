document.addEventListener('DOMContentLoaded',async () => {
    const table = document.getElementById('dentist-table');
    // fetch the data from data.csv

    let  data = await fetch('data.csv');
    data = await data.text();
    // Parse CSV data
    let  rows =  data.split('\n');
    rows.shift();
    rows = rows.map(row => 
    {
        if (row.split('"').length < 2) {
            return row.split(',').map(cell => cell.trim());
        }

        let message = row.split('"')[1].replaceAll('"', '').trim();
       let d = row.split('"')[0].split(",").map(cell => cell.trim());
       d.pop();
        d.push(message);
        return d;
    });

    data = rows.slice(1); // Skip header row
    const tbody = table.querySelector('tbody');
    // Function to create table rows
    const createRow = (rowData) => {
        const row = document.createElement('tr');
        rowData.forEach((cellData, index) => {
            const cell = document.createElement('td');
            if (index === 6) {
                // For Website column, make it a link
                const link = document.createElement('a');
                link.href = cellData;
                link.target = '_blank';
                link.textContent = cellData;
                cell.appendChild(link);
            } else {
                cell.textContent = cellData;
            }
            
            // Add copy button to each cell
            const button = document.createElement('button');
            button.textContent = 'Copy';
            button.classList.add('copy-button');
            button.onclick = () => copyToClipboard(cell.textContent || cell.querySelector('a')?.href);
            cell.appendChild(button);
            row.appendChild(cell);
        });
        return row;
    };

    // Populate the table with data
    data.forEach(rowData => {
        tbody.appendChild(createRow(rowData));
    });

    // Function to handle column drag
    const thElements = table.querySelectorAll('th');
    thElements.forEach(th => {
        th.addEventListener('dragstart', dragStart);
        th.addEventListener('dragover', dragOver);
        th.addEventListener('drop', drop);
    });

    let draggedTh;

    function dragStart(e) {
        draggedTh = e.target;
        e.dataTransfer.setData('text/plain', draggedTh.textContent);
    }

    function dragOver(e) {
        e.preventDefault();
    }

    function drop(e) {
        e.preventDefault();
        const targetTh = e.target;
        if (targetTh !== draggedTh && targetTh.nodeName === 'TH') {
            const draggedIndex = [...thElements].indexOf(draggedTh);
            const targetIndex = [...thElements].indexOf(targetTh);
            swapColumns(draggedIndex, targetIndex);
        }
    }

    // Swap columns based on indices
    function swapColumns(fromIndex, toIndex) {
        const rows = [...tbody.rows];
        rows.forEach(row => {
            const cells = [...row.cells];
            const fromCell = cells[fromIndex];
            const toCell = cells[toIndex];
            row.insertBefore(fromCell, toCell);
        });
        const ths = [...table.querySelectorAll('th')];
        table.querySelector('thead').appendChild(ths[toIndex]);
    }

    // Function to copy content to clipboard
    function copyToClipboard(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text.replaceAll("Copy", "").trim();
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }
});


document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById('dentist-table');

    // Add event listener to each cell
    table.addEventListener('click', (event) => {
        const target = event.target;
        if (target.tagName === 'TD') {
            const row = target.parentElement; // Get the row containing the clicked cell

            // Toggle row color between gray and white
            if (row.style.backgroundColor === 'gray') {
                row.style.backgroundColor = 'white'; // Reset to white
            } else {
                row.style.backgroundColor = 'gray'; // Change to gray
            }
        }
    });
});

