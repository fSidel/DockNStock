  // Image URL loader
  const imageUrlInput = document.getElementById('imageUrl');
  const loadImageBtn = document.getElementById('loadImage');
  const thumb = document.getElementById('thumb');
  const urlDisplay = document.getElementById('urlDisplay');

  loadImageBtn.addEventListener('click', () => {
    const url = imageUrlInput.value.trim();
    if(url) {
      thumb.src = url;
      thumb.style.display = 'block';

      // Limit URL display length
      if(url.length > 100){
        urlDisplay.textContent = "Image URL: " + url.slice(0, 100) + "...";
      } else {
        urlDisplay.textContent = "Image URL: " + url;
      }
    } else {
      thumb.style.display = 'none';
      urlDisplay.textContent = '';
    }
  });

  // Quantity adjust buttons
  const quantityInput = document.getElementById('quantity');
  document.getElementById('increaseQty').addEventListener('click', () => {
    quantityInput.stepUp();
  });
  document.getElementById('decreaseQty').addEventListener('click', () => {
    quantityInput.stepDown();
  });