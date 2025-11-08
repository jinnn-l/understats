/**
 * @author Walter G. https://www.thatsoftwaredude.com/content/14060/building-a-simple-csv-file-preview-with-pure-javascript
 */ 
const fileInput = document.getElementById('csvInput');
const preview = document.getElementById('preview');
const info = document.getElementById('info');

// handle file upload
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    // validate file type
    if (!file.name.endsWith('.csv')) {
        preview.innerHTML = '<div class="error">Please upload a CSV file</div>';
        info.textContent = '';
        return;
    }

    // read file
    const reader = new FileReader();

    reader.onload = function(e) {
        const text = e.target.result;
        const table = createTableFromCSV(text);
        
        if (table) {
            preview.innerHTML = '';
            preview.appendChild(table);
            info.textContent = `Showing preview of ${file.name}`;
        } else {
            preview.innerHTML = '<div class="error">Error: File appears to be empty</div>';
            info.textContent = '';
        }
    };

    reader.onerror = function() {
        preview.innerHTML = '<div class="error">Error reading file</div>';
        info.textContent = '';
    };

    reader.readAsText(file);
});

// create HTML table from CSV content
function createTableFromCSV(csv) {
    // split into rows and handle common delimiters
    const rows = csv.split(/\r?\n/);
    if (rows.length === 0) return null;

    const table = document.createElement('table');
    
    // create table header
    const headers = parseCSVRow(rows[0]);
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // create table body
    const tbody = document.createElement('tbody');
    
    // process only first 100 rows for performance
    const maxRows = Math.min(rows.length, 101); // +1 because first row is header
    
    // start from 1 to skip header
    for (let i = 1; i < maxRows; i++) {
        if (rows[i].trim() === '') continue;
        
        const rowData = parseCSVRow(rows[i]);
        const tr = document.createElement('tr');
        
        rowData.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        
        tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    return table;
}

// parse a single CSV row handling quotes and commas
function parseCSVRow(row) {
    const cells = [];
    let currentCell = '';
    let inQuotes = false;
    
    for (let i = 0; i < row.length; i++) {
        const char = row[i];
        
        if (char === '"') {
            if (inQuotes && row[i + 1] === '"') {
                // handle escaped quotes
                currentCell += '"';
                i++;
            } else {
                // toggle quote state
                inQuotes = !inQuotes;
            }
        } else if (char === ',' && !inQuotes) {
            // end of cell
            cells.push(currentCell.trim());
            currentCell = '';
        } else {
            currentCell += char;
        }
    }
    
    // push the last cell
    cells.push(currentCell.trim());
    
    return cells;
}