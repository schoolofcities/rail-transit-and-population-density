<script>
	import '../assets/styles.css'; 
	
	import TopSofC from "../lib/TopSofC.svelte";

	import LongCityGraphic from '../lib/LongCityGraphic.svelte';

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
		'Middle East & North Africa': '#007FA3', 
		'East Asia': '#0D534D', 
		'South East Asia & Oceania': '#6FC7EA', 
		'Latin America & Caribbean': '#F1C500', 
		'South & Central Asia': '#AB1368',
	}

	const cities = Object.keys(citiesDens);
	cities.sort()

	let curCityOne = "Mumbai";
	let curCityTwo = "Taipei";

	const metrics = [
		// "General density",
		"Population density (people / km²)",
		"Population density in the area 1km from all major rail transit stations",
		"% of total population that lives 1km from a major rail transit station",
		"% of the urban area within 1km of a major rail transit station",
		"Concentration ratio (% of population near transit / % of area near transit)"
	];

	const metricsKeys = [
		// "raw_dens",
		"urban_dens",
		"station_dens",
		"transit_pop_pct",
		"transit_area_pct",
		"transit_ratio",
	];

	const metricValues = [
		// 7500,
		8000,
		40000,
		80,
		40,
		30,
	]

	let curMetric = metrics[2];
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

		<LongCityGraphic/>


		<h1>Rail transit and population density</h1>
		<h2>Comparing and ranking 250+ cities around the world</h2>
		<p>
			Aniket Kali & Jeff Allen | December 2024
		</p>
		<br>

	</div>

	<div class="text">
		
		<p>
			Public transit is important infrastructure in many cities. Ideally, major transit routes and stations are sited to serve and connect the most amount of people while covering an efficient amount of area. However, there's a lot of variation in how and where lines and stations are placed relative to where people live.
		</p>

		<p>
			We've created maps of major transit lines overlaid onto population density for 250+ of the most populated cities around the globe. Click the dropdowns to view and compare how well transit systems serve their populations. Using these maps, we've computed a number of different metrics examining characteristics of transit oriented development, and ranked how well cities perform relative to each other.
		</p>

		<!-- <p> -->
			<!-- Each map below displays a population density heatmap overlayed with major transit routes.  -->
			<!-- We show density in 1 sqkm tiles, covering a 50 km radius from city centers. Transit lines and stations are shown in purple, and only include regional rail, subways, and LRT. -->
		<!-- </p> -->

		<!-- <h3>Compare Cities</h3> -->

		<br>

		<div id="legend">
			<p >
				Rail transit line and station
				<svg width="40" height="15" xmlns="http://www.w3.org/2000/svg">
					<line x1="0" y1="10" x2="40" y2="10" stroke="#0D534D" stroke-width="1" />
					<circle cx="18" cy="10" r="3" fill="#0D534D" />
				</svg>
			</p>
			<p style="padding-top: 10px;">						
				Population density (people / km²)
			</p>
			<div id="legend-gradient"></div>
			<div id="legend-numbers">
				<p id="legend-numbers-left">0</p>
				<p id="legend-numbers-right">10,000+</p>
			</div>
			
		</div>
		

	</div>

	<div class="charts">

		<CityDisplay cities={cities} bind:curCity={curCityOne} />

		<CityDisplay cities={cities} bind:curCity={curCityTwo} />

		<CityMetricsDisplay citiesDens={citiesDens} cityOne={curCityOne} cityTwo={curCityTwo} metrics={metrics} metricsKeys={metricsKeys} />

	</div>

	<div class="text">

		<!-- <h5><u>Density metrics</u></h5>

		<p>{metrics[0]}: Total population divided by total area</p>
		<p>{metrics[1]}: Population divided by area, for 1 sqkm tiles with at least 100 people</p>
		<p>{metrics[2]}: Average population divided by area, for each 1km radius around a station</p>

		<h5><u>Transit metrics</u></h5>

		<p>{metrics[3]}: Percent of the total population that is urban (> 100 people in a 1 sqkm tile) and within 1 km of a station</p>
		<p>{metrics[4]}: Percent of the total area that is urban and within 1km of a station</p>
		<p>{metrics[5]}: {metrics[3]} divided by {metrics[4].toLowerCase()}</p> -->

		<br>
		<br>

		<p>
			Add some brief description on what each metric means / how to intrepret
		</p>

		<p>
			Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
		</p>

		

		<!-- Our water layer is from <a href="https://www.arcgis.com/home/item.html?id=e750071279bf450cbd510454a80f2e63">World Water Bodies</a>, and we applied the Douglas-Peucker simplification algorithm to reduce file size. -->
		

	</div>



	<div class="text">

		<br>

		<h3>City Rankings</h3>

		<p style="font-family: TradeGothicLTLight">
			Select by metric:
		</p>
		
		<select bind:value={curMetric}>
			{#each metrics as value}
				<option {value}>{value}</option>
			{/each}
		</select>

		<p style="font-family: TradeGothicLTLight">
			Select by region:
		</p>
		
	</div>

	<div class="charts">
		
		<HorizontalBarChart 
			curMetric={curMetric} 
			curMetricKey={curMetricKey} 
			maxMetricValue={maxMetricValue} 
			data={citiesDens} 
			classifierColours={regionColours}
		/>

	</div>

	<div class="text">

		<h3>Data sources</h3>

		<p>
			Cities included are from a dataset by <a href="https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/" target="_blank">Natural Earth</a>, which includes point coordinates for the centre of each city. For each city, we then defined the urban region shown on the maps as a circle with a 50km radius from this centre point.  We chose to use a standard circle size for all regions to account for idiosyncrasies in how different parts of the world define metro areas. 50km is approximately the outer range that someone would commute to/from a city centre along a major rail corridor.
		</p>

		<p>
			We started with a list of the 300 most populated cities, but then manually removed cases where one city was essentially the suburb of another city at our scale (e.g. Howrah was removed since it is very close to Kolkata). We also only included cities with rail transit.
			<!-- though left in ambiguous cases (e.g., Hong Kong and Shenzhen). -->
		</p>

		<p>
			We sourced the population density data from <a href="https://hub.worldpop.org/geodata/summary?id=24777" target="_blank">WorldPop</a>. The first population density metric is computed after removing areas where population density is less than 100km², to account for how some regions have more or less agricultural land and habitable geography (e.g. mountains, water, etc.).
		</p>

		<p>
			We downloaded railway and station data from <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> (OSM) using <a href="https://overpass-turbo.eu/" target="_blank">overpass turbo</a> with <a href="https://github.com/schoolofcities/world-city-transit-density/blob/main/analysis/query_osm.py" target="_blank">this query</a>. We then calculated 1km buffers around each point and then estimated the population within the buffered area via aerial interpolation. While the quality and comprehensiveness of OSM data is quite good in most cities, there are several cities that have missing or incorrect data. As OSM data is edited and improved, we'll aim to update our maps and metrics.
		</p>

		<p>
			There are two main limitations with this data. 1) it only includes rail transit, not Bus Rapid Transit (BRT), which in many cities provides comporable service to rail. 2) does not account for frequency (i.e. headway) of routes. While many transit agencies share their routes and schedules in GTFS format, which includes information about frequency and often technology (bus, rail, etc.), we found that the availability of GTFS at a global scale was not available, particularly outside of Europe and North America. 
		</p>

		<p>
			All code and data is available on our <a href="https://github.com/schoolofcities/world-city-transit-density/tree/main" target="_blank">GitHub repository</a>. 
		</p>

		<br>
		<br>
		<br>

	</div>

</main>

<style>

	select {
		width: 100%;
		max-width: 700px;
	}

	#legend {
		width: 100%;
	}

	#legend p {
		font-family: TradeGothicLTLight;
		margin-bottom: 0px;
		margin-top: 0px;
		color: var(--brandDarkBlue);
	}

	#legend-gradient {
		width: 100%;
		height: 15px;
		border: solid 1px var(--brandLightBlue);
		border-radius: 10px;
		background: rgb(255,255,255);
		background: linear-gradient(90deg, rgba(255,255,255,1) 0%, rgba(241,197,0,1) 50%, rgba(220,70,51,1) 100%);
	}

	#legend-numbers {
		display: flex;
		justify-content: space-between;
	}

	#legend-numbers-left {
		text-align: left;
	}

	#legend-numbers-right {
		text-align: right;
	}

</style>