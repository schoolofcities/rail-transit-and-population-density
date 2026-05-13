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

	const regionNamesFr = {
		'US & Canada': 'États-Unis et Canada',
		'Europe': 'Europe',
		'Sub Saharan Africa': 'Afrique subsaharienne',
		'Middle East & North Africa': 'Moyen-Orient et Afrique du Nord',
		'East Asia': 'Asie de l\'Est',
		'South East Asia & Oceania': 'Asie du Sud-Est et Océanie',
		'Latin America & Caribbean': 'Amérique latine et Caraïbes',
		'South & Central Asia': 'Asie du Sud et centrale',
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

	const metricsFr = [
		"Population urbaine",
		"Densité de population urbaine (habitants/km²)",
		"Densité de population dans un rayon de 1 km autour de toutes les principales gares ferroviaires",
		"% de la population urbaine vivant à moins d'1 km d'une principale gare ferroviaire",
		"% de la zone urbaine située à moins d'1 km d'une principale gare ferroviaire",
		"Taux de concentration (% de la population urbaine à proximité des transports en commun / % de la zone urbaine à proximité des transports en commun)"
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

	let lang = 'en';
</script>

<svelte:head>
	<meta
		name="viewport"
		content="width=device-width, initial-scale=1, minimum-scale=1"
	/>

	<title>Rail Transit & Population Density | School of Cities</title>

	<meta name="description" content="Maps, charts, and rankings that compare 250 cities around the world">
	<meta name="author" content="Aniket Kali & Jeff Allen">

	<meta property="og:title" content="Rail Transit and Population Density in 250 Cities" />
	<meta property="og:description" content="Maps, charts, and rankings that compare 250 cities around the world" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://schoolofcities.github.io/rail-transit-and-population-density" />
	<meta property="og:image" content="https://schoolofcities.github.io/rail-transit-and-population-density/web-card.png" />
	<meta property="og:locale" content="en_CA">

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:site" content="https://schoolofcities.github.io/rail-transit-and-population-density" />
	<meta name="twitter:creator" content="@UofTCities" />
	<meta name="twitter:title" content="Rail Transit and Population Density in 250 Cities" />
	<meta name="twitter:description" content="Maps, charts, and rankings that compare 250 cities around the world" />
	<meta name="twitter:image" content="https://schoolofcities.github.io/rail-transit-and-population-density/web-card.png" /> 

</svelte:head>

<TopSofC />

<main>

	<div class="title">

		<div class="lang-toggle">
			<button class:active={lang === 'en'} on:click={() => lang = 'en'}>English</button>
			<button class:active={lang === 'fr'} on:click={() => lang = 'fr'}>Français</button>
		</div>


		<LongCityGraphic/>

		

		<h1>
			{#if lang === 'fr'}
				Transports ferroviaires et densité de population
			{:else}
				Rail Transit & Population Density
			{/if}
		</h1>
		<h2>
			{#if lang === 'fr'}
				Comparaison et classement de {cities.length} villes à travers le monde
			{:else}
				Comparing and ranking {cities.length} cities around the world
			{/if}
		</h2>
		<p>
			<a href="https://www.linkedin.com/in/aniket-k-8a8b9921b/" target="_blank">Aniket Kali</a> &
			<a href="http://jamaps.github.io/" target="_blank">Jeff Allen</a> |
			{#if lang === 'fr'}Janvier 2025{:else}January 2025{/if}
		</p>
		<br>

		
	</div>

	<div class="text">

		{#if lang === 'fr'}
			<p>
				Un bon réseau de transports en commun relie personnes et lieux. Idéalement, cela se fait de manière efficace et durable, les lignes et les stations desservant et reliant le plus grand nombre de personnes possible. Mais en réalité, il existe de grandes disparités quant à l'efficacité avec laquelle cela est mis en œuvre, tant au sein des villes qu'entre elles.
			</p>
			<p>
				Pour analyser cette question, nous avons créé des cartes des principales lignes et gares de transport ferroviaire (métro, trains régionaux, TLR) superposées aux données de densité de population pour {cities.length} des régions urbaines les plus peuplées du monde. Cliquez sur les menus déroulants ci-dessous pour voir dans quelle mesure les réseaux de transport desservent leurs populations dans différentes villes.
			</p>
			<p>
				Les cartes présentent la même échelle géographique, soit un diamètre de 100 km, afin de pouvoir être facilement comparées entre elles.
			</p>
			<p>
				À partir de ces cartes, nous avons également calculé plusieurs indicateurs permettant d'analyser les caractéristiques du <a href="https://en.wikipedia.org/wiki/Transit-oriented_development" target="_blank">développement axé sur les transports en commun</a> (TOD - Transit oriented development), et nous avons classé les villes en fonction de leurs performances les unes par rapport aux autres. En règle générale, plus la densité de population et la proportion de la population vivant à proximité des principaux réseaux ferroviaires sont élevées, meilleurs sont les résultats.
			</p>
			<p>
				Les données démographiques utilisées pour ces cartes proviennent de <a href="https://zenodo.org/records/11179644" target="_blank">GlobPOP</a>, tandis que les données relatives au réseau ferroviaire proviennent de <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a>. Au bas de cette page, nous décrivons plus en détail ces sources de données, notre méthodologie, ainsi que certaines limites.
			</p>
		{:else}
			<p>
				Good public transit connects people to places. Ideally, this is done efficiently and sustainably, with transit routes and stations serving and connecting the most amount of people possible. But in reality, there's a lot of variation within and between cities in how effectively this is done.
			</p>
			<p>
				To look at this, we've created maps of major rail transit lines and stations (rapid transit, regional rail, LRT) overlaid onto population density for {cities.length} of the most populated urban regions around the globe. Click the dropdowns below to view how well transit systems serve their populations in different cities.
			</p>
			<p>
				Each map has the same geographic scale, 100km in diameter, to be easily comparable with each other.
			</p>
			<p>
				Using these maps, we've also computed several metrics examining characteristics of <a href="https://en.wikipedia.org/wiki/Transit-oriented_development" target="_blank">transit oriented development</a>, and ranked how well cities perform relative to each other. Generally, the greater the density and proportion of the population that lives near major rail transit, the better.
			</p>
			<p>
				Population data for these maps are from <a href="https://zenodo.org/records/11179644" target="_blank">GlobPOP</a>, and rail transit data are from <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a>. At the bottom of this page we describe these data sources, our methodology, and limitations in more detail.
			</p>
		{/if}

		<br>

		<div id="legend">
			<p >
				{#if lang === 'fr'}Ligne de transport ferroviaire et gare{:else}Rail transit line and station{/if}
				<svg width="40" height="15" xmlns="http://www.w3.org/2000/svg">
					<line x1="0" y1="10" x2="38" y2="10" stroke="#1E3765" stroke-width="1" />
					<circle cx="18" cy="10" r="3" fill="#1E3765" />
				</svg>
			</p>
			<p style="padding-top: 10px;">
				{#if lang === 'fr'}Densité de population (habitants/km²){:else}Population density (people / km²){/if}
			</p>
			<div id="legend-gradient"></div>
			<div id="legend-ticks">
				<p>|</p>
				<p>|</p>
				<p>|</p>
				<p>|</p>
				<p>|</p>
				<p>|</p>
				<p>|</p>
			</div>
			<div id="legend-numbers">
				<p id="legend-numbers-left">0 &nbsp;&nbsp;</p>
				<p id="legend-numbers-middle">15,000</p>
				<p id="legend-numbers-right">30,000+</p>
			</div>
		</div>
		

	</div>

	<div class="charts">
		<CityDisplay cities={cities} bind:curCity={curCityOne} />

		<CityDisplay cities={cities} bind:curCity={curCityTwo} />

		<CityMetricsDisplay cityMetrics={cityMetrics} cityOne={curCityOne} cityTwo={curCityTwo} metrics={metrics} metricsFr={metricsFr} metricsKeys={metricsKeys} {lang} />
	</div>

	<div class="text">
		<br>

		<h3>{#if lang === 'fr'}Classement des villes{:else}City Rankings{/if}</h3>

		<p style="font-family: TradeGothicLTLight">
			{#if lang === 'fr'}Sélectionner par indicateur{:else}Select by metric:{/if}
		</p>

		<select bind:value={curMetric}>
			{#each metrics as value, i}
				<option {value}>{lang === 'fr' ? metricsFr[i] : value}</option>
			{/each}
		</select>

		<p style="font-family: TradeGothicLTLight">
			{#if lang === 'fr'}Sélectionner par région{:else}Select by region:{/if}
		</p>
	</div>

	<div class="charts">
		<HorizontalBarChart
			curMetric={curMetric}
			curMetricKey={curMetricKey}
			maxMetricValue={maxMetricValue}
			data={cityMetrics}
			classifierColours={regionColours}
			regionNamesFr={regionNamesFr}
			{lang}
		/>
	</div>

	<div class="text">
		<h3>{#if lang === 'fr'}Données et Méthodes{:else}Data & Methods{/if}</h3>

		{#if lang === 'fr'}
			<p>
				Notre liste de villes provient d'un ensemble de données fourni par <a href="https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/" target="_blank">Natural Earth</a>. A partir d'une liste initiale des 350 villes les plus peuplées, nous avons supprimé manuellement les cas où une ville constituait, à notre échelle, essentiellement la banlieue d'une autre (par exemple, Howrah a été supprimée car elle est très proche de Kolkata), ainsi que les villes ne disposant d'aucun réseau ferroviaire. Nous avons ajouté manuellement quelques villes qui, selon nous, méritaient d'être incluses (par exemple, des villes canadiennes).
			</p>
			<p>
				Pour chaque ville, nous avons ensuite défini la région urbaine représentée sur les cartes comme un cercle d'un rayon de 50 km à partir du point central indiqué dans l'ensemble de données de Natural Earth. Nous avons décidé d'utiliser un rayon standard pour toutes les régions afin de tenir compte des particularités propres à chaque région du monde en ce qui concerne la définition des zones métropolitaines. Un rayon de 50 km correspond approximativement à la distance maximale qu'une personne serait susceptible de parcourir pour se rendre au centre-ville ou en revenir en empruntant un axe ferroviaire principal.
			</p>
			<p>
				Nous avons obtenu les données de densité de population sur <a href="https://zenodo.org/records/11179644" target="_blank">GlobPOP</a>, qui fournit des données sur le nombre d'habitants et la densité de population avec une résolution spatiale de 30 secondes d'arc (environ 1 km à l'équateur) à l'échelle mondiale. Nos indicateurs de densité de population urbaine sont calculés après avoir exclu les zones où la densité de population est inférieure à 400 km², afin de tenir compte des variations régionales en termes de superficie des terres agricoles et de zones géographiques inhabitables (par exemple, montagnes, cours d'eau, etc.). 400 km² correspond au seuil utilisé par <a href="https://www12.statcan.gc.ca/census-recensement/2021/ref/dict/az/definition-eng.cfm?ID=geo049a" target="_blank">Statistique Canada</a> pour définir les localités.
			</p>
			<p>
				Nous avons téléchargé les données relatives aux voies ferrées et aux gares depuis <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> (OSM) à l'aide d'<a href="https://overpass-turbo.eu/" target="_blank">Overpass Turbo</a>, en exécutant <a href="https://github.com/schoolofcities/world-city-transit-density/blob/main/analysis/query_osm.py" target="_blank">cette requête</a>. Nous avons ensuite calculé des zones tampons d'un kilomètre autour de chaque gare, puis estimé la population à l'intérieur de ces zones par interpolation aérienne. OSM repose sur des données issues du crowdsourcing ; bien que la qualité et l'exhaustivité de ces données soient assez bonnes dans la plupart des villes, certaines villes présentent des données manquantes ou erronées. Si vous constatez des erreurs, n'hésitez pas à mettre à jour OSM ! Au fur et à mesure que les données d'OSM seront modifiées et améliorées, nous nous efforcerons de mettre à jour nos cartes et nos indicateurs.
			</p>
			<p>
				Ces données sur les transports en commun présentent deux limites principales : 1) elles ne concernent que le transport ferroviaire, et non les réseaux de bus à haut niveau de service (BHNS), qui, dans de nombreuses villes, offrent un service comparable à celui du transport ferroviaire ; 2) elles ne tiennent pas compte de la fréquence (c'est-à-dire de l'intervalle entre les départs) des lignes. Bien que de nombreuses agences de transport en commun partagent leurs itinéraires et leurs horaires au format GTFS, qui comprend des informations sur la fréquence et souvent sur le mode de transport (bus, train, etc.), nous avons constaté que le format GTFS n'était pas disponible partout à l'échelle mondiale, en particulier en dehors de l'Europe et de l'Amérique du Nord.
			</p>
			<p>
				Bien sûr, le lieu de résidence n'est qu'un élément parmi d'autres ; l'objectif des transports en commun est avant tout d'amener les gens là où ils veulent aller (travail, école, loisirs, etc.). Ce serait formidable de pouvoir superposer à ces cartes des données sur la répartition des lieux d'emploi et d'activité afin d'étudier également le volet « destination » de l'équation et d'analyser la connectivité des réseaux. Un projet à mener dans le futur !
			</p>
			<p>---</p>
			<p>
				Vous trouverez plus d'informations sur ce projet, le code, les données, etc. sur <a href="https://github.com/schoolofcities/world-city-transit-density/tree/main" target="_blank">GitHub</a>.
			</p>
		{:else}
			<p>
				Our list of cities came from a dataset from <a href="https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/" target="_blank">Natural Earth</a>. We started with a list of the 350 most populated cities, but then manually removed cases where one city was essentially the suburb of another city at our scale (e.g. Howrah was removed since it is very close to Kolkata), as well as removed cities without any rail transit. We manually added a few cities we personally thought should be included (e.g. Canadian cities).
			</p>
			<p>
				For each city, we then defined the urban region shown on the maps as a circle with a 50km radius from the centre point noted in the Natural Earth dataset. We chose to use a standard circle size for all regions to account for idiosyncrasies in how different parts of the world define metro areas. 50km is approximately the outer range that someone would commute to/from a city centre along a major rail corridor.
			</p>
			<p>
				We sourced the population density data from <a href="https://zenodo.org/records/11179644" target="_blank">GlobPOP</a> which provides population count and density data at a spatial resolution of 30 arc-seconds (approximately 1km at the equator) around the globe. Our urban population density metrics are computed after removing areas where population density is less than 400km², to account for how regions vary in terms of how much agricultural land and un-habitable geography they have (e.g. mountains, water, etc.). 400km² is the same threshold used by <a href="https://www12.statcan.gc.ca/census-recensement/2021/ref/dict/az/definition-eng.cfm?ID=geo049a" target="_blank">Statistics Canada</a> to define populated places.
			</p>
			<p>
				We downloaded rail and station data from <a href="https://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> (OSM) using <a href="https://overpass-turbo.eu/" target="_blank">overpass turbo</a> with <a href="https://github.com/schoolofcities/world-city-transit-density/blob/main/analysis/query_osm.py" target="_blank">this query</a>. We then calculated 1km buffers around each station and then estimated the population within the buffered area via aerial interpolation. OSM is crowd-sourced data, and while the quality and comprehensiveness of OSM data is quite good in most cities, there are several cities that have missing or incorrect data. If you see any errors, please update OSM! As OSM data is edited and improved, we'll aim to update our maps and metrics in the future.
			</p>
			<p>
				There are two main limitations with this transit data: 1) it only includes rail transit, not Bus Rapid Transit (BRT), which in many cities provides comparable service to rail. 2) it does not account for frequency (i.e. headway) of routes. While many transit agencies share their routes and schedules in GTFS format, which includes information about frequency and often technology (bus, rail, etc.), we found that the availability of GTFS at a global scale was not available everywhere, particularly outside of Europe and North America.
			</p>
			<p>
				Now of course, where people live is just one piece; the goal of transit is ultimately to take people where they want to go (work, school, recreation, etc.). It would be great to layer on employment and activity location data onto these maps to also look at the destination side of the equation as well as analyze connectivity of networks. Something to work on in the future!
			</p>
			<p>---</p>
			<p>
				More information about this project, code, data, etc. are available on <a href="https://github.com/schoolofcities/world-city-transit-density/tree/main" target="_blank">GitHub</a>.
			</p>
		{/if}

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
		width: calc(100% - 32px);
		height: 15px;
		border: solid 1px var(--brandLightBlue);
		margin-left: 0px;
		border-radius: 5px;
		background: rgb(255,255,255);
		background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(241,197,0,0.7) 10%, rgba(220,70,51,0.8) 50%, rgba(171,19,104,0.8) 75%, rgba(109,36,122,0.8) 100%, rgba(109,36,122,0.8) 100%);
	}

	#legend-ticks {
		width: calc(100% - 32px);
		margin-left: 0px;
		display: flex;
		justify-content: space-between;
		margin-top: -10px;
		height: 13px;
	}
	#legend-ticks p {
		font-size: 10px;
	}

	#legend-numbers {
		display: flex;
		justify-content: space-between;
	}
	#legend-numbers p {
		font-size: 17px;
	}

	#legend-numbers-left {
		text-align: left;
	}

	#legend-numbers-middle {
		text-align: center;
		flex-grow: 1; /* Allows the middle number to take up available space */
	}

	#legend-numbers-right {
		text-align: right;
	}

	.lang-toggle {
		display: flex;
		gap: 0;
		margin-bottom: 16px;
	}

	.lang-toggle button {
		font-family: TradeGothicBold;
		font-size: 14px;
		color: var(--brandDarkBlue);
		background: none;
		border: solid 1px var(--brandLightBlue);
		padding: 4px 12px;
		cursor: pointer;
		letter-spacing: 0.05em;
	}

	.lang-toggle button:first-child {
		border-radius: 4px 0 0 4px;
	}

	.lang-toggle button:last-child {
		border-radius: 0 4px 4px 0;
		border-left: none;
	}

	.lang-toggle button.active {
		background: var(--brandDarkBlue);
		color: white;
		border-color: var(--brandDarkBlue);
	}

	.lang-toggle button:not(.active):hover {
		opacity: 0.6;
	}
</style>