(() => {
  document.documentElement.classList.add('js-ready');

  const detail = document.querySelector('[data-product-detail]');
  if (!detail) return;

  const price = detail.querySelector('[data-price-value]');
  const comparePrice = detail.querySelector('[data-compare-price-value]');
  const stock = detail.querySelector('[data-stock-value]');
  const radios = detail.querySelectorAll('[data-variant-preview] input[type="radio"]');
  const quantity = detail.querySelector('.add-to-cart-form input[name="quantity"]');

  radios.forEach((radio) => {
    radio.addEventListener('change', () => {
      if (price) price.textContent = radio.dataset.price || '';
      if (comparePrice) comparePrice.textContent = radio.dataset.comparePrice || '';
      if (stock) stock.textContent = radio.dataset.stock || '';
      if (quantity && radio.dataset.stockQuantity) {
        quantity.max = radio.dataset.stockQuantity;
        if (Number(quantity.value) > Number(radio.dataset.stockQuantity)) quantity.value = radio.dataset.stockQuantity;
      }
    });
  });
})();
