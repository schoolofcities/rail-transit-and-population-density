<script>

	import sofcLongCity from "../assets/sofc-long-city.svg";

	let transitColour = "#1E3765";

	let topWidth;

</script>






<div id="longCityGraphic" bind:offsetWidth={topWidth}>

	<img width="100%" height="71" src={sofcLongCity} alt="sofcLongCity" />

	<svg width="100%" height="20">
		<line
			x1="2"
			y1="10"
			x2={topWidth - 5}
			y2="10"
			stroke={transitColour}
			stroke-width="3"
			stroke-linecap="round"
		/>
		{#each [0, 1, 2, 3] as c}
			<circle
				r={4}
				cx={20 + c * ((topWidth - 30 - 16) / 3)}
				cy={10}
				stroke-width="3px"
				stroke={transitColour}
				fill="#fff"
			/>
		{/each}
	</svg>

</div>