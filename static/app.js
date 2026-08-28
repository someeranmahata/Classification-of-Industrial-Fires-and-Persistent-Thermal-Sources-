let map = L.map('map').setView(
    [22.5, 78.9],
    5
);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        attribution:
            '&copy; OpenStreetMap contributors'
    }
).addTo(map);

let markersLayer = L.layerGroup().addTo(map);

async function loadHotspots() {

    markersLayer.clearLayers();

    let days =
        document.getElementById("days").value;

    let response =
        await fetch(
            `/api/hotspots?days=${days}`
        );

    let data =
        await response.json();

    console.log(data);

    let industrialCount = 0;
    let thermalCount = 0;
    let otherCount = 0;
    
    console.log(data)
    data.forEach(point => {

        let color = "orange";
        let label = "Other";

        // 0 = Fire
        if (point.prediction == 0) {

            color = "red";
            label = "Industrial Fire";
            industrialCount++;
        }

        // 1 = Thermal
        else if (point.prediction == 1) {

            color = "green";
            label = "Persistent Thermal Source";
            thermalCount++;
        }

        // 2 = Other
        else {

            color = "orange";
            label = "Other";
            otherCount++;
        }

        L.circleMarker(
            [point.latitude, point.longitude],
            {
                radius: 8,
                color: color,
                fillColor: color,
                fillOpacity: 0.8,
                weight: 2
            }
        )
        .bindPopup(`
            <b>${label}</b>
            <br>
            Latitude: ${point.latitude}
            <br>
            Longitude: ${point.longitude}
            <br>
            Brightness: ${point.brightness}
            <br>
            FRP: ${point.frp}
            <br>
            Raw Prediction: ${point.prediction}
        `)
        .addTo(markersLayer);

    });

    document.getElementById(
        "industrial_count"
    ).innerText = industrialCount;

    document.getElementById(
        "thermal_count"
    ).innerText = thermalCount;

    document.getElementById(
        "other_count"
    ).innerText = otherCount;
}

loadHotspots();