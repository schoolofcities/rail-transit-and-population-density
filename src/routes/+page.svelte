<script>
	import '../assets/styles.css'; 
	
	import TopSofC from "../lib/TopSofC.svelte";

	import LongCityGraphic from '../lib/LongCityGraphic.svelte';

	import CityDisplay from '../lib/CityDisplay.svelte';
	import CityMetricsDisplay from '../lib/CityMetricsDisplay.svelte';
	import HorizontalBarChart from '../lib/HorizontalBarChart.svelte';
	
	import cityMetrics from "../data/city_metrics.json"

	const regionColours = {
		'US & Canada': '#DDDDDD', 
		'Europe': '#DC4633', 
		'Sub Saharan Africa': '#CCBB44', 
		'Middle East & North Africa': '#0072B2', 
		'East Asia': '#f6a7af', 
		'South East Asia & Oceania': '#88CCEE', 
		'Latin America & Caribbean': '#F0E442', 
		'South & Central Asia': '#332288',
	}

	const cities = Object.keys(cityMetrics);
	cities.sort()

	let curCityOne = "Osaka";
	let curCityTwo = "Buenos Aires";

	const metrics = [
		"Urban population",
		"Urban population density (people / km²)",
		"Population density in the area 1km from all major rail transit stations",
		"% of the urban population within 1km of a major rail transit station",
		"% of the urban area within 1km of a major rail transit station",
		"Concentration ratio (% urban pop near transit / % urban area near transit)"
	];

	const metricsKeys = [
		"urban_total_pop",
		"urban_dens",
		"station_dens",
		"transit_pop_pct",
		"transit_area_pct",
		"conc_ratio",
	];

	const metricValues = [
		40000000,
		20000,
		50000,
		80,
		60,
		8,
	]

	let curMetric = metrics[3];
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
		
		<h1>
			Rail transit and population density
		</h1>
		<h2>
			Comparing and ranking {cities.length} cities around the world
		</h2>
		<p>
			Aniket Kali & Jeff Allen | January 2025
		</p>
		<br>

	</div>

	<div class="text">
		
		<p>
			Public transit connects people to employment, education, and allow easy participation in urban life. Ideally, this is done efficiently and sustainably, with transit routes and stations connecting the most amount of people possible. But in reality, there's a lot of variation within and between cities in how effectively this is done.
		</p>
		<p>
			To look at this, we've created maps of major rail transit lines and stations overlaid onto population density for {cities.length} of the most populated urban regions around the globe. Click the dropdowns below to view how well transit systems serve their populations in different cities. 
		</p>
		<p>
			Each map is in exactly the same geographic scale, 100km in diameter.
		</p>
		<p>
			Using these maps, we've also computed several metrics examining characteristics of transit oriented development, and ranked how well cities perform relative to each other. Generally, the greater the density and proportion of the population that lives near major rail transit, the better. 
		</p>
		<p>
			Population data are from <a href="https://github.com/lulingliu/GlobPOP" target="_blank">GlobPOP</a> and rail transit data are from <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a>. At the bottom of this page we describe these data sources, our methodology, and limitations in more detail.
		</p>

		<br>

		<div id="legend">
			<p >
				Rail transit line and station
				<svg width="40" height="15" xmlns="http://www.w3.org/2000/svg">
					<line x1="0" y1="10" x2="38" y2="10" stroke="#1E3765" stroke-width="1" />
					<circle cx="18" cy="10" r="3" fill="#1E3765" />
				</svg>
			</p>
			<p style="padding-top: 10px;">						
				Population density (people / km²)
			</p>
			<div id="legend-gradient"></div>
			<div id="legend-numbers">
				<p id="legend-numbers-left">0</p>
				<p id="legend-numbers-right">30,000</p>
			</div>
		</div>
		

	</div>

	<div class="charts">
		<CityDisplay cities={cities} bind:curCity={curCityOne} />

		<CityDisplay cities={cities} bind:curCity={curCityTwo} />

		<CityMetricsDisplay cityMetrics={cityMetrics} cityOne={curCityOne} cityTwo={curCityTwo} metrics={metrics} metricsKeys={metricsKeys} />
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
			data={cityMetrics} 
			classifierColours={regionColours}
		/>
	</div>

	<div class="text">
		<h3>Data & Methods</h3>

		<p>
			Cities included <a href="https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/" target="_blank">Natural Earth</a>, which includes population estimates and point coordinates for the centre of each city. 
			We started with a list of the 300 most populated cities, but then manually removed cases where one city was essentially the suburb of another city at our scale (e.g. Howrah was removed since it is very close to Kolkata). We also only included cities with rail transit.
		</p>
		<p>
			For each city, we then defined the urban region shown on the maps as a circle with a 50km radius from this centre point. We chose to use a standard circle size for all regions to account for idiosyncrasies in how different parts of the world define metro areas. 50km is approximately the outer range that someone would commute to/from a city centre along a major rail corridor.
		</p>
		<p>
			We sourced the population density data from <a href="https://github.com/lulingliu/GlobPOP" target="_blank">GlobPOP</a> which provides population count and density data at a spatial resolution of 30 arc-seconds (approximately 1km at the equator) around the globe. Our urban population density metrics are computed after removing areas where population density is less than 400km², to account for how regions vary in terms agricultural land and habitable geography they have (e.g. mountains, water, etc.). (400km² is the same threshold used by <a href="https://www12.statcan.gc.ca/census-recensement/2021/ref/dict/az/definition-eng.cfm?ID=geo049a" target="_blank">Statistics Canada</a> for urban areas).
		</p>

		<p>
			We downloaded railway and station data from <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> (OSM) using <a href="https://overpass-turbo.eu/" target="_blank">overpass turbo</a> with <a href="https://github.com/schoolofcities/world-city-transit-density/blob/main/analysis/query_osm.py" target="_blank">this query</a>. We then calculated 1km buffers around each station and then estimated the population within the buffered area via aerial interpolation. OSM is crowd-sourced data, and while the quality and comprehensiveness of OSM data is quite good in most cities, there are several cities that have missing or incorrect data. If you see any errors, please update OSM! As OSM data is edited and improved, we'll aim to update our maps and metrics in the future.
		</p>

		<p>
			There are two main limitations with this transit data: 1) it only includes rail transit, not Bus Rapid Transit (BRT), which in many cities provides comparable service to rail. 2) it does not account for frequency (i.e. headway) of routes. While many transit agencies share their routes and schedules in GTFS format, which includes information about frequency and often technology (bus, rail, etc.), we found that the availability of GTFS at a global scale was not available, particularly outside of Europe and North America. 
		</p>

		<p>
			Now of course, where people live is just one side; the goal of transit is ultimately to take people where they want to go (work, school, recreation, etc.). It would be great to layer on employment and activity location data onto these maps to also look at the destination side of the equation. Something to work on in the future!
		</p>

		<p>
			---
		</p>

		<p>
			More information about this project, code, data, etc. are available on <a href="https://github.com/schoolofcities/world-city-transit-density/tree/main" target="_blank">GitHub</a>. 
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
		background: linear-gradient(90deg, rgba(255,255,255,0.9) 0%, rgba(241,197,0,0.9) 25%, rgba(220,70,51,0.9) 50%, rgba(171,19,104,0.9) 75%, rgba(109,36,122,0.9) 100%);
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