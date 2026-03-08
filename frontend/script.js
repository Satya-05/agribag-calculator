const API_URL = 'https://agribag-calculator.onrender.com';
let currentData = null;
let allRecords = [];

function showSection(name) {
    document.querySelectorAll('.section').forEach(s => s.hidden = true);
    document.getElementById(`section-${name}`).hidden = false;
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    if (name === 'records') loadRecords();
}

function previewImage() {
    const file = document.getElementById('fileInput').files[0];
    if (!file) return;
    document.getElementById('image-preview').src = URL.createObjectURL(file);
    document.getElementById('preview-container').hidden = false;
    document.getElementById('calculate-btn').hidden = false;
    document.getElementById('upload-area').hidden = true;
}

function removeImage() {
    document.getElementById('fileInput').value = '';
    document.getElementById('image-preview').src = '';
    document.getElementById('preview-container').hidden = true;
    document.getElementById('calculate-btn').hidden = true;
    document.getElementById('upload-area').hidden = false;
}

async function uploadImage() {
    const farmerName = document.getElementById('farmer-name').value.trim();
    const date = document.getElementById('date').value;
    const file = document.getElementById('fileInput').files[0];

    if (!farmerName) { showToast('⚠️ Please enter farmer name!'); return; }
    if (!date) { showToast('⚠️ Please select a date!'); return; }
    if (!file) { showToast('⚠️ Please upload an image!'); return; }

    document.getElementById('section-upload').hidden = true;
    document.getElementById('section-loading').hidden = false;
    animateLoadingSteps();

    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('farmer_name', farmerName);
        formData.append('date', date);

        const response = await fetch(`${API_URL}/process-image`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        document.getElementById('section-loading').hidden = true;

        if (data.success) {
            currentData = data;
            displayResults(data);
        } else {
            showToast('❌ Error: ' + data.error);
            document.getElementById('section-upload').hidden = false;
        }

    } catch (error) {
        console.error('Upload error:', error);
        document.getElementById('section-loading').hidden = true;
        document.getElementById('section-upload').hidden = false;
        showToast('❌ Could not connect to server! Error: ' + error.message);
    }
}

function animateLoadingSteps() {
    const steps = ['step1', 'step2', 'step3'];
    steps.forEach(s => document.getElementById(s).classList.remove('active'));
    document.getElementById('step1').classList.add('active');
    setTimeout(() => {
        document.getElementById('step1').classList.remove('active');
        document.getElementById('step2').classList.add('active');
    }, 2000);
    setTimeout(() => {
        document.getElementById('step2').classList.remove('active');
        document.getElementById('step3').classList.add('active');
    }, 4000);
}

function displayResults(data) {
    document.getElementById('result-farmer').textContent = data.farmer_name;
    document.getElementById('result-date').textContent = data.date;

    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = '';

    for (let row = 0; row < 15; row++) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="sno">${row + 1}</td>
            <td><input type="number" step="0.1" value="${data.grid[row][0]}" id="cell-0-${row}" oninput="recalculate()" /></td>
            <td class="sno">${row + 16}</td>
            <td><input type="number" step="0.1" value="${data.grid[row][1]}" id="cell-1-${row}" oninput="recalculate()" /></td>
            <td class="sno">${row + 31}</td>
            <td><input type="number" step="0.1" value="${data.grid[row][2]}" id="cell-2-${row}" oninput="recalculate()" /></td>
            <td class="sno">${row + 46}</td>
            <td><input type="number" step="0.1" value="${data.grid[row][3]}" id="cell-3-${row}" oninput="recalculate()" /></td>
        `;
        tableBody.appendChild(tr);
    }

    recalculate();
    document.getElementById('section-results').hidden = false;
}

function recalculate() {
    let s1 = 0, s2 = 0, s3 = 0, s4 = 0;

    for (let row = 0; row < 15; row++) {
        s1 += parseFloat(document.getElementById(`cell-0-${row}`)?.value) || 0;
        s2 += parseFloat(document.getElementById(`cell-1-${row}`)?.value) || 0;
        s3 += parseFloat(document.getElementById(`cell-2-${row}`)?.value) || 0;
        s4 += parseFloat(document.getElementById(`cell-3-${row}`)?.value) || 0;
    }

    s1 = Math.round(s1 * 100) / 100;
    s2 = Math.round(s2 * 100) / 100;
    s3 = Math.round(s3 * 100) / 100;
    s4 = Math.round(s4 * 100) / 100;
    const total = Math.round((s1 + s2 + s3 + s4) * 100) / 100;

    document.getElementById('col1-sum-cell').innerHTML = `Col 1: <strong>${s1}</strong> kg`;
    document.getElementById('col2-sum-cell').innerHTML = `Col 2: <strong>${s2}</strong> kg`;
    document.getElementById('col3-sum-cell').innerHTML = `Col 3: <strong>${s3}</strong> kg`;
    document.getElementById('col4-sum-cell').innerHTML = `Col 4: <strong>${s4}</strong> kg`;
    document.getElementById('total-value').textContent = `${total} kg`;

    if (currentData) {
        currentData.column_sums = [s1, s2, s3, s4];
        currentData.total = total;
    }
}

async function confirmAndSave() {
    if (!currentData) return;

    let s1 = 0, s2 = 0, s3 = 0, s4 = 0;
    for (let row = 0; row < 15; row++) {
        s1 += parseFloat(document.getElementById(`cell-0-${row}`)?.value) || 0;
        s2 += parseFloat(document.getElementById(`cell-1-${row}`)?.value) || 0;
        s3 += parseFloat(document.getElementById(`cell-2-${row}`)?.value) || 0;
        s4 += parseFloat(document.getElementById(`cell-3-${row}`)?.value) || 0;
    }

    s1 = Math.round(s1 * 100) / 100;
    s2 = Math.round(s2 * 100) / 100;
    s3 = Math.round(s3 * 100) / 100;
    s4 = Math.round(s4 * 100) / 100;
    const total = Math.round((s1 + s2 + s3 + s4) * 100) / 100;

    try {
        const response = await fetch(`${API_URL}/save-record`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                farmer_name: currentData.farmer_name,
                date: currentData.date,
                total_weight: total,
                column_sums: [s1, s2, s3, s4]
            })
        });

        const result = await response.json();

        if (result.success) {
            showToast('✅ Record saved successfully!');
            setTimeout(() => resetForm(), 1500);
        } else {
            showToast('❌ Error saving record!');
        }

    } catch (error) {
        console.error('Save error:', error);
        showToast('❌ Could not connect to server!');
    }
}

async function loadRecords() {
    try {
        const response = await fetch(`${API_URL}/records`);
        const data = await response.json();
        if (data.success) {
            allRecords = data.records;
            renderRecords(allRecords);
        }
    } catch (error) {
        console.error('Load records error:', error);
        showToast('❌ Could not load records!');
    }
}


function renderRecords(records) {
    const container = document.getElementById('records-container');
    if (records.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>🌾 No records yet</p>
                <span>Start by adding a new entry</span>
            </div>`;
        return;
    }
    container.innerHTML = records.map(r => `
        <div class="record-card">
            <div class="record-top">
                <div>
                    <div class="record-name">👨‍🌾 ${r.farmer_name}</div>
                    <div class="record-date">📅 ${r.date}</div>
                </div>
                <div style="display:flex; align-items:center; gap:16px;">
                    <div class="record-total">${r.total_weight} <span>kg total</span></div>
                    <button onclick="deleteRecord(${r.id})" style="background:#fee2e2; border:none; color:#dc2626; padding:8px 14px; border-radius:8px; cursor:pointer; font-size:13px; font-weight:600;">🗑 Delete</button>
                </div>
            </div>
            <div class="record-cols">
                <div class="record-col">
                    <div class="record-col-label">Column 1</div>
                    <div class="record-col-value">${r.col1_sum} kg</div>
                </div>
                <div class="record-col">
                    <div class="record-col-label">Column 2</div>
                    <div class="record-col-value">${r.col2_sum} kg</div>
                </div>
                <div class="record-col">
                    <div class="record-col-label">Column 3</div>
                    <div class="record-col-value">${r.col3_sum} kg</div>
                </div>
                <div class="record-col">
                    <div class="record-col-label">Column 4</div>
                    <div class="record-col-value">${r.col4_sum} kg</div>
                </div>
            </div>
        </div>
    `).join('');
}

async function deleteRecord(id) {
    if (!confirm('Are you sure you want to delete this record?')) return;
    try {
        const response = await fetch(`${API_URL}/records/${id}`, {
            method: 'DELETE'
        });
        const result = await response.json();
        if (result.success) {
            showToast('✅ Record deleted!');
            loadRecords();
        } else {
            showToast('❌ Error deleting record!');
        }
    } catch (error) {
        showToast('❌ Could not connect to server!');
    }
}

function filterRecords() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const filtered = allRecords.filter(r => r.farmer_name.toLowerCase().includes(query));
    renderRecords(filtered);
}

function resetForm() {
    document.getElementById('farmer-name').value = '';
    document.getElementById('date').valueAsDate = new Date();
    document.getElementById('fileInput').value = '';
    document.getElementById('image-preview').src = '';
    document.getElementById('preview-container').hidden = true;
    document.getElementById('calculate-btn').hidden = true;
    document.getElementById('upload-area').hidden = false;
    document.getElementById('section-results').hidden = true;
    document.getElementById('section-loading').hidden = true;
    document.getElementById('section-upload').hidden = false;
    document.getElementById('table-body').innerHTML = '';
    currentData = null;
    document.querySelectorAll('.nav-btn').forEach((b, i) => {
        b.classList.toggle('active', i === 0);
    });
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

document.getElementById('date').valueAsDate = new Date();