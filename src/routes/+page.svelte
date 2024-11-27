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
		'Middle East & North Africa': '#F1C500', 
		'East Asia': '#0D534D', 
		'South East Asia & Oceania': '#6FC7EA', 
		'Latin America & Caribbean': '#007FA3', 
		'South & Central Asia': '#AB1368',
	}

	const cities = Object.keys(citiesDens);
	cities.sort()

	let curCityOne = "Mumbai";
	let curCityTwo = "Taipei";

	const metrics = [
		// "General density",
		"Population density (people / km²)",
		"Population density within 1km of major transit stations",
		"% of population in the region that lives 1km from a major transit station",
		"% of the urban area within 1km of a major transit station",
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
			Brief description on what each metric means / how to intrepet
		</p>

		<p>
			We also obtained our list of cities from <a href="https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/" target="_blank">Natural Earth</a>, which provides a longitude/latitude point for the centre of the city. For each city, we defined the urban region as a circle with a 50km radius from this centre point. 
		</p>

		<p>
			We initially used the 300 most populated cities, and then manually removed cases where one city was essentially the suburb of another city at our scale (e.g. Howrah was removed since it is very close to Kolkata). 
			<!-- though left in ambiguous cases (e.g., Hong Kong and Shenzhen). -->
		</p>

		<p>
			We sourced geographic population density from <a href="https://hub.worldpop.org/geodata/summary?id=24777" target="_blank">WorldPop</a>. The region wide population density metric only includes areas which have a population density of greater than 100km², to account for how some regions have more or less farmland and habitable geography (e.g. mountains, water, etc.).
		</p>		

		<p>
			We obtained railway and station data from <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> (OSM) using <a href="https://overpass-turbo.eu/" target="_blank">overpass turbo</a> with <a href="https://github.com/schoolofcities/world-city-transit-density/blob/main/analysis/query_osm.py" target="_blank">this query</a>. We then calculated 1km buffers around each point and then estimated the population within the buffered area via aerial interpolation. While the quality and comprehensiveness of OSM data is quite good in most cities, there are several cities that have missing or incorrect data. As OSM is edited and improved, we'll aim to update our maps and metrics.
		</p>

		<p>
			Limitations of transit data, BRT and frequency, and of course connectivity/accessibility
		</p>

		<p>
			All code and relevant data is available on our <a href="https://github.com/schoolofcities/world-city-transit-density/tree/main" target="_blank">GitHub repository</a>. Below is a chart ranking all cities for each of the five metrics. You can also download this data here.
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

</main>

<style>

	select {
		width: 100%;
		max-width: 700px;
	}

</style>