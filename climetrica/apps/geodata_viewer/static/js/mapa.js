document.addEventListener("DOMContentLoaded", async () => {
    const mapDiv = document.getElementById("mapa");
    const controlsDiv = document.getElementById("layer-controls");

    if (!mapDiv) return;

    let layerData = {};
    let activeLayers = [];

    const response = await fetch("/api/capas/");
    const capas = await response.json();

    capas.forEach(capa => {
        layerData[capa.name] = capa.trace;

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = capa.name;
        checkbox.value = capa.name;

        const label = document.createElement("label");
        label.htmlFor = capa.name;
        label.textContent = capa.name;

        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                activeLayers.push(layerData[capa.name]);
            } else {
                activeLayers = activeLayers.filter(t => t.name !== capa.name);
            }

            Plotly.react(mapDiv, activeLayers, {
                mapbox: {
                    style: "carto-positron",
                    center: { lat: 4.5, lon: -74 },
                    zoom: 5.5
                },
                margin: { r: 0, t: 40, l: 0, b: 0 },
                showlegend: true
            });
        });

        controlsDiv.appendChild(checkbox);
        controlsDiv.appendChild(label);
        controlsDiv.appendChild(document.createElement("br"));
    });

    Plotly.newPlot(mapDiv, [], {
        mapbox: {
            style: "carto-positron",
            center: { lat: 4.5, lon: -74 },
            zoom: 5.5
        },
        margin: { r: 0, t: 40, l: 0, b: 0 },
        showlegend: true
    });
});
