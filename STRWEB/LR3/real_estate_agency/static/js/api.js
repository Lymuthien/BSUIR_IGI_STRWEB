(() => {
  const root = document.getElementById('geoWidgetRoot');
  if (!root) return;

  const address = root.dataset.estateAddress;
  const btn = document.getElementById('geoBtnEstate');
  const statusEl = document.getElementById('geoStatusEstate');
  const resultEl = document.getElementById('geoResultEstate');
  const actionsEl = document.getElementById('geoActionsEstate');

  const visitorLatInput = document.getElementById('visitor_lat');
  const visitorLonInput = document.getElementById('visitor_lon');
  const visitorDistanceInput = document.getElementById('visitor_distance_km');

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }
  function clearResult() {
    if (resultEl) resultEl.innerHTML = '';
    if (actionsEl) actionsEl.innerHTML = '';
  }

  // Haversine (km)
  function haversineKm(lat1, lon1, lat2, lon2) {
    const toRad = v => v * Math.PI / 180;
    const R = 6371; // Earth radius km
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat/2)**2 +
              Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
              Math.sin(dLon/2)**2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }

  async function geocodeWithNominatim(address) {
    const email = encodeURIComponent('email@example.com');
    const url = `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(address)}&addressdetails=0&email=${email}`;
    const resp = await fetch(url, {
      headers: {
        'Accept': 'application/json'
      }
    });
    if (!resp.ok) throw new Error('Geocoding failed: ' + resp.status);
    const data = await resp.json();
    if (!Array.isArray(data) || data.length === 0) {
      throw new Error('Адрес не найден в геокодере');
    }
    const item = data[0];
    return { lat: parseFloat(item.lat), lon: parseFloat(item.lon) };
  }

  btn.addEventListener('click', async () => {
    clearResult();
    setStatus('Определяем координаты объявления...');
    try {
      const place = await geocodeWithNominatim(address);
      setStatus('Координаты объявления найдены: ' + place.lat.toFixed(6) + ', ' + place.lon.toFixed(6));
      if (!navigator.geolocation) {
        setStatus('Геолокация не поддерживается в этом браузере.');
        return;
      }
      setStatus('Получаем ваше местоположение...');
      navigator.geolocation.getCurrentPosition(async (pos) => {
        const user = {
          lat: pos.coords.latitude,
          lon: pos.coords.longitude,
          accuracy: pos.coords.accuracy
        };

        if (visitorLatInput) visitorLatInput.value = user.lat;
        if (visitorLonInput) visitorLonInput.value = user.lon;

        const distKm = haversineKm(user.lat, user.lon, place.lat, place.lon);
        if (visitorDistanceInput) visitorDistanceInput.value = distKm.toFixed(3);

        const lines = [];
        lines.push(`<div><strong>Расстояние по прямой:</strong> ${distKm.toFixed(2)} км</div>`);
        lines.push(`<div class="small">Точность определения вашей позиции: ${user.accuracy ? user.accuracy + ' м' : 'неизвестно'}</div>`);

        const gmaps = `https://www.google.com/maps/dir/?api=1&origin=${user.lat},${user.lon}&destination=${place.lat},${place.lon}&travelmode=driving`;
        lines.push(`<div><a href="${gmaps}" target="_blank" rel="noopener">Открыть маршрут в Google Maps</a></div>`);

        resultEl.innerHTML = lines.join('\n');
        setStatus('Готово.');
      }, (err) => {
        setStatus('Не удалось получить местоположение: ' + err.message);
      }, { enableHighAccuracy: true, timeout: 15000 });
    } catch (e) {
      setStatus('Ошибка: ' + (e.message || e));
    }
  });
})();
