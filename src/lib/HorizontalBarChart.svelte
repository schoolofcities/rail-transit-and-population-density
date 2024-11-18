<script>
    export let curMetric;
    export let curMetricKey;
    export let maxMetricValue;
    export let citiesDens;

    // https://github.com/sveltejs/svelte/issues/13446#issuecomment-2382939034
    let dens = Object.entries(citiesDens);
    $: sortedDens = dens.toSorted(function(a,b) {return a[1][curMetricKey] <= b[1][curMetricKey]});

    // Define chart dimensions 
    let chartWidth;
	let chartHeight = 100;
	$: chartHeight = 24 * sortedDens.length + 50;  // Responsive to the subset chosen

    // Define chart parameters
    let barStart = 29;

    // Create the chart scaffolding
    $: showPct = curMetric.includes('pct');
    $: xAxisIntervals = [...Array(6).keys()].map(x => (x/5) * maxMetricValue);
	$: xAxisIntervalSpacing = (chartWidth - 50) / (xAxisIntervals.length - 1);
</script>

<div id="chart-wrapper" bind:offsetWidth={chartWidth}>
    <svg height={chartHeight} width={chartWidth} id="chart">
        <polygon id="diamond" points="0,-6 6,0 0,6 -6,0" fill="black" stroke="white" stroke-width="2" />
        <polygon points="0,-6 6,0 0,6 -6,0" fill="#191919" stroke="#191919" stroke-width="4" />
        
        <!-- Create the chart background -->
        {#each xAxisIntervals as xInterval, i}
            <line class="grid"
                x1 = {29 + i * xAxisIntervalSpacing}
                y1 = 34
                x2 = {29 + i * xAxisIntervalSpacing}
                y2 = {chartHeight}
            ></line>

            <line class="grid-white"
                x1 = {29 + i * xAxisIntervalSpacing}
                y1 = 34
                x2 = {29 + i * xAxisIntervalSpacing}
                y2 = 38
            ></line>

            <text class="axis-label"
                x = {35 + i * xAxisIntervalSpacing}
                y = 30
                text-anchor="end"
            >
                {xInterval}
                {#if showPct}
                    %
                {/if}
            </text>
        {/each}

        <!-- {#each xAxisIntervals as xInterval, i}
            <line class="grid"
                x1 = {29 + i * xAxisIntervalSpacing}
                y1 = 34
                x2 = {29 + i * xAxisIntervalSpacing}
                y2 = {chartHeight}
                stroke-opacity="0.91"
            ></line>

            {#if i === 0}
                <line class="grid-white"
                    x1 = {29 + i * xAxisIntervalSpacing}
                    y1 = 34
                    x2 = {29 + i * xAxisIntervalSpacing}
                    y2 = {chartHeight}
                    stroke-opacity=0.5
                ></line>
            {/if}
        {/each} -->

        <!-- Graph the data onto the chart -->
        {#each sortedDens as [city, cityInfo], i}
            <line class="bar"
                x1={30}
                y1={52 + i * 24}
                x2={((chartWidth - 50) * (cityInfo[curMetricKey] / maxMetricValue)) + 29}  
                y2={52 + i * 24}
                style="
                    stroke: white;
                    stroke-width: 16;
                    stroke-opacity: 0.08
                "
            ></line>

            <line class="bar"
                x1={0}
                y1={52 + i * 24}
                x2={4}
                y2={52 + i * 24}
                style="
                    stroke: yellow;
                    stroke-width: 16;
                    stroke-opacity: 1
                "
            ></line>

            <text class="axis-label"
                x = 8
                y = {57 + i * 24}
                text-anchor="start"
            >{i + 1}</text>

            <text class="bar-label"
                x={34}
                y={56 + i * 24}
                style="
                    fill: white;
                "
            >{city}</text>
        {/each}
    </svg>
</div>

<style>
	#chart-wrapper {
		margin: 0 auto;
		max-width: 1080px;
		min-width: 375px;
		border-top: solid 1px var(--brandDarkBlue);
		border-bottom: solid 1px var(--brandDarkBlue);
		padding-bottom: 10px;
		margin-bottom: 10px;
		padding-left: 10px;
	}

	#chart {
		margin-top: 10px;
		margin-bottom: 10px;
		background-color: var(--brandGray90);
	}

	.grid {
		stroke: var(--brandDarkBlue);
		stroke-width: 1px;
	}

	.grid-white {
		stroke: var(--brandWhite);
		stroke-width: 1px;
	}

	.axis-label {
        stroke: 'grey';
		fill: var(--brandGray);
		font-size: 14px;
	}

	.bar-label {
		/* fill: var(--brandWhite); */
		font-size: 13px;
	}
</style>