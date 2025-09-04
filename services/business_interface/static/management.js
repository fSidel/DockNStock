(function(){
const dropArea = document.getElementById('dropArea');
const fileInput = document.getElementById('photoInput');
const thumb = document.getElementById('thumb');
const photoError = document.getElementById('photoError');
const dropText = document.getElementById('dropText');


const showError = (msg) => { photoError.textContent = msg; photoError.hidden = false; };
const clearError = () => { photoError.textContent = ''; photoError.hidden = true; };


function handleFile(file){
clearError();
if(!file) return;
if(!file.type.startsWith('image/')){ showError('Please pick an image file.'); return; }
const url = URL.createObjectURL(file);
thumb.src = url;
thumb.style.display = 'block';
dropText.textContent = file.name + ' (' + Math.round(file.size/1024) + ' KB)';
}


// Click opens file dialog
dropArea.addEventListener('click', () => fileInput.click());
// Keyboard: Enter/Space
dropArea.addEventListener('keydown', (e)=>{ if(e.key==='Enter' || e.key===' ') { e.preventDefault(); fileInput.click(); } });


// File input change
fileInput.addEventListener('change', (e)=> handleFile(e.target.files[0]));


// Drag events
['dragenter','dragover'].forEach(evt => dropArea.addEventListener(evt, (e)=>{ e.preventDefault(); e.stopPropagation(); dropArea.classList.add('dragover'); }));
['dragleave','drop'].forEach(evt => dropArea.addEventListener(evt, (e)=>{ e.preventDefault(); e.stopPropagation(); dropArea.classList.remove('dragover'); }));
dropArea.addEventListener('drop', (e)=>{ const dt = e.dataTransfer; if(dt && dt.files && dt.files.length) { fileInput.files = dt.files; handleFile(dt.files[0]); } });

document.getElementById('productForm').addEventListener('reset', () => {
  thumb.src = '';
  thumb.style.display = 'none';
  dropText.textContent = 'Drag & drop a photo here, or click to select';
  clearError();
});

// Simple form validation
document.getElementById('productForm').addEventListener('submit', (e)=>{
clearError();
const name = document.getElementById('name');
const qty = document.getElementById('quantity');
const wgt = document.getElementById("weigth");

if(!name.value.trim()){ 
    e.preventDefault(); 
    name.focus(); 
    name.setCustomValidity('Required'); 
    name.reportValidity(); 
    return; 
}

name.setCustomValidity('');
if(qty.value === '' || Number(qty.value) < 0){ 
    e.preventDefault(); 
    qty.focus(); 
    qty.setCustomValidity('Must be 0 or greater'); 
    qty.reportValidity(); 
    return; 
}
if(wgt.value === '' || Number(wgt.value) < 0){ 
    e.preventDefault(); 
    qty.focus(); 
    qty.setCustomValidity('Must be 0 or greater'); 
    qty.reportValidity(); 
    return; 
}
qty.setCustomValidity('');
});



})();