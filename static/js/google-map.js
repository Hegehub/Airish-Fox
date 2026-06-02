(function () {
  "use strict";

  function readNumber(element, name, fallback) {
    var value = Number(element.dataset[name]);
    return Number.isFinite(value) ? value : fallback;
  }

  function renderFallback(element, message) {
    element.classList.add("store-map--error");
    if (!element.textContent.trim()) {
      element.textContent = message || "Карта временно недоступна. Используйте кнопку маршрута.";
    }
  }

  window.initAirishFoxMaps = function initAirishFoxMaps() {
    var maps = document.querySelectorAll("[data-google-map]");
    if (!maps.length) {
      return;
    }
    if (!window.google || !window.google.maps) {
      maps.forEach(function (element) { renderFallback(element); });
      return;
    }

    maps.forEach(function (element) {
      try {
        var lat = readNumber(element, "lat", null);
        var lng = readNumber(element, "lng", null);
        if (lat === null || lng === null) {
          renderFallback(element, "Координаты магазина пока не указаны.");
          return;
        }
        var position = { lat: lat, lng: lng };
        var options = {
          center: position,
          zoom: readNumber(element, "zoom", 15),
          disableDefaultUI: false,
          streetViewControl: false,
          mapTypeControl: false
        };
        if (element.dataset.mapId) {
          options.mapId = element.dataset.mapId;
        }
        var map = new window.google.maps.Map(element, options);
        new window.google.maps.Marker({
          position: position,
          map: map,
          title: element.dataset.title || "Airish Fox"
        });
      } catch (error) {
        renderFallback(element);
      }
    });
  };

  document.addEventListener("DOMContentLoaded", function () {
    if (window.google && window.google.maps) {
      window.initAirishFoxMaps();
      return;
    }
    window.setTimeout(function () {
      if (!window.google || !window.google.maps) {
        document.querySelectorAll("[data-google-map]").forEach(function (element) {
          renderFallback(element);
        });
      }
    }, 3500);
  });
}());
