document.addEventListener("DOMContentLoaded", function () {
    // ユーザーの位置情報を取得し、マップを表示
    function initMap() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(success, error);
        } else {
            alert("Geolocation is not supported by this browser.");
        }

        function success(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            initMapWithCoords(lat, lon);
        }

        function error() {
            alert("Unable to retrieve your location. Using default location.");
            const defaultLat = 35.6895; // 東京の緯度
            const defaultLon = 139.6917; // 東京の経度
            initMapWithCoords(defaultLat, defaultLon);
        }
    }

    function initMapWithCoords(lat, lon) {
        const map = L.map('map').setView([lat, lon], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
        }).addTo(map);

        const marker = L.marker([lat, lon]).addTo(map)
            .bindPopup('ここにいます！')
            .openPopup();

        // 3秒間処理を停止
        sleep(3000).then(() => fetchWeatherData(lat, lon));
    }

    function fetchWeatherData(lat, lon) {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,precipitation&current_weather=true&timezone=Asia/Tokyo`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTPエラー! ステータス: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data); // デバッグ用にデータをコンソールに出力
                displayWeather(data);
            })
            .catch(error => {
                console.error("Error fetching weather data:", error);
                alert("天気情報を取得できませんでした: " + error.message);
            });
    }

    function displayWeather(data) {
        const weatherContainer = document.getElementById('weather');
        if (!weatherContainer) {
            console.error("#weather 要素が見つかりませんでした。");
            return;
        }

        const currentWeather = data.current_weather;
        weatherContainer.innerHTML = `
            <h2>天気情報</h2>
            <p>気温: ${currentWeather.temperature}°C</p>
            <p>風速: ${currentWeather.windspeed} m/s</p>
        `;
    }

    // JavaScriptで処理を一時停止するための関数
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    initMap();
});
