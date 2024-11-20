<script>
    import '../assets/styles.css'; 
    
    import TopSofC from "../lib/TopSofC.svelte";

    import CityDisplay from '../lib/CityDisplay.svelte';
    import CityMetricsDisplay from '../lib/CityMetricsDisplay.svelte';
    import HorizontalBarChart from '../lib/HorizontalBarChart.svelte';
    
    import citiesDens from "../data/cities_dens.json"

	async function loadData() {
		try {
			// const response = await fetch('../recovery_rankings.csv');
			const response = await fetch("../data/cities_dens.json");
			const csvData = await response.text();
			data = csvParse(csvData);
		} catch (error) {
			console.error('Error loading CSV data:', error);
		}
	}

    const regionColours = {
        'US & Canada': '#00A189', 
        'Europe': '#DC4633', 
        'Sub Saharan Africa': '#8DBF2E', 
        'Middle East & North Africa': '#F1C500', 
        'East Asia': '#0D534D', 
        'South East Asia & Oceania': '#6FC7EA', 
        'Latin America & Caribbean': '#007FA3', 
        'South & Central Asia': '#AB1368',
    }

    const cities = Object.keys(citiesDens);
    cities.sort()

    let curCityOne = "Toronto";
    let curCityTwo = "Chicago";

    const metrics = [
        "General density",
        "Urban density",
        "Station density",
        "% Urban pop near transit",
        "% Urban area near transit",
        "Ratio of urban population and area near transit"
    ];

    const metricsKeys = [
        "raw_dens",
        "urban_dens",
        "station_dens",
        "transit_pop_pct",
        "transit_area_pct",
        "transit_ratio",
    ];

    const metricValues = [
        10000,
        10000,
        50000,
        100,
        100,
        25,
    ]

    let curMetric = metrics[0];
    $: curMetricKey = metricsKeys[metrics.indexOf(curMetric)];
    $: maxMetricValue = metricValues[metrics.indexOf(curMetric)];
</script>

<svelte:head>
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1, minimum-scale=1"
    />
</svelte:head>

<TopSofC />

<main>
    <div class="title">
        <h1>Comparing Transit-Oriented Density</h1>
        <p>
            Aniket Kali, Jeff Allen
        </p>
        <p>
            Published TBD
        </p>
    </div>

    <div class="text">
        <p>Transit is a key part of many cities - but there's a lot of variation in how and where lines and stations are placed. Ideally, they serve the most amount of people covering an efficient amount of area.</p>

        <p>Below, you can compare how well transit systems serve their populations for 298 of the most populated cities around the globe. We've computed a number of different metrics examining this, including ranking which cities perform highest on them. </p>

        <p>Each map below displays population density overlayed with transit. We show density in 1 sqkm tiles, covering a 50 km radius. Transit lines and stations are shown in purple, and only include regional rail, subways, and LRT.</p>

        <h3>Compare Cities</h3>

        <CityDisplay cities={cities} bind:curCity={curCityOne} />

        <CityDisplay cities={cities} bind:curCity={curCityTwo} />

        <CityMetricsDisplay citiesDens={citiesDens} cityOne={curCityOne} cityTwo={curCityTwo} metrics={metrics} metricsKeys={metricsKeys} />

        <p>Let's define a few variables first. TODO</p>
        
        <p>We compute our metrics using the following equations: TODO</p>
    </div>

    <div class="text">
        <h3>Rank Cities</h3>

        <select bind:value={curMetric}>
            {#each metrics as value}
                <option {value}>{value}</option>
            {/each}
        </select>
        
        <HorizontalBarChart 
            curMetric={curMetric} 
            curMetricKey={curMetricKey} 
            maxMetricValue={maxMetricValue} 
            data={citiesDens} 
            classifierColours={regionColours}
        />
    </div>

    <div class="text">
        <h3>Appendix</h3>
        <p>We obtained railway and station data from <a href="https://www.openstreetmap.org/">OpenStreetMap</a> (OSM) using <a href="https://overpass-turbo.eu/">overpass turbo</a> with <a href="https://github.com/schoolofcities/world-city-transit-density/blob/main/analysis/query_osm.py">this query</a>. Many cities have missing or incorrect data - let us know if you update OSM, and we'll aim to update our webpage.</p>
        
        <p>We sourced geographic population density from <a href="https://hub.worldpop.org/geodata/summary?id=24777">WorldPop</a>, and center points from <a href="https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/">Natural Earth</a>. Our water layer is from <a href="https://www.arcgis.com/home/item.html?id=e750071279bf450cbd510454a80f2e63">World Water Bodies</a>, and we applied the Douglas-Peucker algorithm to reduce file size.</p>

        <p>All code and relevant data is available on our <a href="https://github.com/schoolofcities/world-city-transit-density/tree/main">GitHub repository</a>.</p>
    </div>
</main>

<style>
    select {
        width: 100%;
    }
</style>