document.addEventListener('DOMContentLoaded', () => {
  // Dark-mode init
  const toggle = document.getElementById('darkModeToggle');
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
    toggle.checked = true;
  }
  toggle.addEventListener('change', () => {
    document.body.classList.toggle('dark-mode', toggle.checked);
    localStorage.setItem('theme', toggle.checked ? 'dark' : 'light');
  });

  // Show monthly by default
  showForm('monthlyForm');
});

function showForm(id) {
  document.querySelectorAll('.form-section')
    .forEach(f => f.style.display = 'none');
  document.getElementById(id).style.display = 'block';
}

function onSubdivisionChange(subdivision) {
  const subdivisions = {
    // name: { info: "...", lat: X, lon: Y }
     "Andaman & Nicobar Islands": {"info": "Island tropics", "lat": 11.7, "lon": 92.7},
    "Arunachal Pradesh": {"info": "Himalayan foothills", "lat": 28.2, "lon": 94.0},
    "Assam & Meghalaya": {"info": "Valleys & hills", "lat": 26.2, "lon": 91.7},
    "Bihar": {"info": "Gangetic plains", "lat": 25.6, "lon": 85.1},
    "Chhattisgarh": {"info": "Central Indian plains", "lat": 21.3, "lon": 81.6},
    "Coastal Andhra Pradesh": {"info": "Coastal strip", "lat": 16.5, "lon": 81.3},
    "Coastal Karnataka": {"info": "Konkan coast", "lat": 13.3, "lon": 74.7},
    "East Madhya Pradesh": {"info": "Vindhyan uplands", "lat": 23.5, "lon": 80.0},
    "East Rajasthan": {"info": "Arid desert & plains", "lat": 26.0, "lon": 75.0},
    "East Uttar Pradesh": {"info": "Tropical plains", "lat": 26.8, "lon": 83.0},
    "Gangetic West Bengal": {"info": "Delta plains", "lat": 23.0, "lon": 87.9},
    "Gujarat Region": {"info": "Western plains", "lat": 22.3, "lon": 72.6},
    "Haryana Delhi & Chandigarh": {"info": "Indo-Gangetic plain", "lat": 28.6, "lon": 77.2},
    "Himachal Pradesh": {"info": "Himalayan mid-hills", "lat": 31.1, "lon": 77.2},
    "Jammu & Kashmir": {"info": "High Himalayas", "lat": 34.1, "lon": 74.8},
    "Jharkhand": {"info": "Chota Nagpur plateau", "lat": 23.6, "lon": 85.3},
    "Kerala": {"info": "Tropical coast & hills", "lat": 10.5, "lon": 76.2},
    "Konkan & Goa": {"info": "Coastal region", "lat": 16.7, "lon": 73.8},
    "Lakshadweep": {"info": "Coral atolls", "lat": 10.6, "lon": 72.6},
    "Madhya Maharashtra": {"info": "Deccan plateau", "lat": 19.0, "lon": 74.0},
    "Matathwada": {"info": "Semi-arid plateau", "lat": 19.3, "lon": 76.2},
    "Naga Mani Mizo Tripura": {"info": "NE hill states (NM, MZ, TR)", "lat": 25.6, "lon": 93.9},
    "North Interior Karnataka": {"info": "Semi-arid plateau", "lat": 15.3, "lon": 75.7},
    "Orissa": {"info": "Coastal & plateaus mix", "lat": 20.3, "lon": 85.8},
    "Punjab": {"info": "Wheat belt plains", "lat": 31.1, "lon": 75.4},
    "Rayalseema": {"info": "Semi-arid interior", "lat": 14.7, "lon": 78.2},
    "Saurashtra & Kutch": {"info": "Dry arid region", "lat": 22.2, "lon": 70.3},
    "South Interior Karnataka": {"info": "Coastal plateau", "lat": 12.3, "lon": 76.6},
    "Sub Himalayan West Bengal & Sikkim": {"info": "Terai foothills", "lat": 26.7, "lon": 88.4},
    "Tamil Nadu": {"info": "Coastal & plains", "lat": 11.1, "lon": 78.6},
    "Telangana": {"info": "Deccan plateau", "lat": 17.4, "lon": 78.5},
    "Uttarakhand": {"info": "Shivalik foothills", "lat": 30.0, "lon": 79.0},
    "Vidarbha": {"info": "Mahanadi basin", "lat": 20.7, "lon": 78.9},
    "West Madhya Pradesh": {"info": "Malwa plateau", "lat": 22.7, "lon": 75.9},
    "West Rajasthan": {"info": "Thar desert region", "lat": 26.9, "lon": 70.9},
    "West Uttar Pradesh": {"info": "Granary region", "lat": 28.6, "lon": 77.2}
 };

  const meta = subdivisions[subdivision];
  document.getElementById('subdivisionInfo').textContent = meta ? meta.info : 'No info available.';
  const weatherText = document.getElementById('weatherText');

  if (!meta) {
    weatherText.textContent = '--';
    return;
  }

  fetch(`/weather?subdivision=${encodeURIComponent(subdivision)}`)
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        weatherText.textContent = 'Not available';
      } else {
        weatherText.textContent = 
          `${data.temp.toFixed(1)}°C, ${data.humidity}% RH, ${data.description}`;
      }
    })
    .catch(() => {
      weatherText.textContent = 'Error';
    });
}
