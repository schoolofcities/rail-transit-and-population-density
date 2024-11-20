<script>
    import SelectClassifiers from "./SelectClassifiers.svelte";

    export let curMetric;
    export let curMetricKey;
    export let maxMetricValue;

    export let data;
    export let classifierColours;

    // Classifiers and cleaning data
    let classifiers = Object.keys(classifierColours);
    // https://github.com/sveltejs/svelte/issues/13446#issuecomment-2382939034
    let dataObj = Object.entries(data);
    $: sortedData = dataObj
        .filter(item => classifiers.includes(item[1].region))
        .sort(function(a,b) {return a[1][curMetricKey] <= b[1][curMetricKey]});
    
    // CHART VARIABLES //
    // Define chart dimensions 
    let chartWidth;
	let chartHeight = 100;
	$: chartHeight = 24 * sortedData.length + 50;  // Responsive to the subset chosen

    // Define chart parameters
    let xAxisTop = 34;
    let xAxisStart = 37;

    let regionStart = 0;
    let rankStart = 8;
    let barStart = xAxisStart + 1;
    let barLabelStart = xAxisStart + 5;

    let barTop = 52;
    let rankTop = 56;
    let barLabelTop = 56;

    let barGap = 24;
    let chartEndGap = 60;
    ////

    // Create the chart scaffolding
    $: showPct = curMetric.includes('pct');
    $: xAxisIntervals = [...Array(6).keys()].map(x => (x/5) * maxMetricValue);
	$: xAxisIntervalSpacing = (chartWidth - chartEndGap) / (xAxisIntervals.length - 1);
</script>

<div id="chart-wrapper" bind:offsetWidth={chartWidth}>
    <SelectClassifiers bind:classifiers={classifiers} classifierColours={classifierColours} />

    <svg height={chartHeight} width={chartWidth} id="chart">
        <!-- <polygon id="diamond" points="0,-6 6,0 0,6 -6,0" fill="black" stroke="white" stroke-width="2" /> -->
        <!-- <polygon points="0,-6 6,0 0,6 -6,0" fill="#191919" stroke="#191919" stroke-width="4" /> -->
        
        <!-- Create the chart background -->
        {#each xAxisIntervals as xInterval, i}
            <line class="grid-primary"
                x1 = {xAxisStart + (i * xAxisIntervalSpacing)}
                y1 = {xAxisTop}
                x2 = {xAxisStart + (i * xAxisIntervalSpacing)}
                y2 = {chartHeight}
            ></line>

            <line class="grid-secondary"
                x1 = {xAxisStart + (i * xAxisIntervalSpacing)}
                y1 = {xAxisTop}
                x2 = {xAxisStart + (i * xAxisIntervalSpacing)}
                y2 = {xAxisTop + 4}
            ></line>

            <text class="axis-label"
                x = {(xAxisStart + 6) + (i * xAxisIntervalSpacing)}
                y = {xAxisTop - 4}
                text-anchor="end"
            >
                {xInterval}
                {#if showPct}
                    %
                {/if}
            </text>
        {/each}

        {#each xAxisIntervals as xInterval, i}
            <line class="grid-primary"
                x1 = {xAxisStart + (i * xAxisIntervalSpacing)}
                y1 = {xAxisTop}
                x2 = {xAxisStart + (i * xAxisIntervalSpacing)}
                y2 = {chartHeight}
                stroke-opacity="0.91"
            ></line>

            {#if i === 0}
                <line class="grid-secondary"
                    x1 = {xAxisStart + (i * xAxisIntervalSpacing)}
                    y1 = {xAxisTop}
                    x2 = {xAxisStart + (i * xAxisIntervalSpacing)}
                    y2 = {chartHeight}
                    stroke-opacity=0.5
                ></line>
            {/if}
        {/each}

        <!-- Graph the data onto the chart -->
        {#each sortedData as [city, cityInfo], i}
            <line class="bar-data"
                x1={barStart}
                y1={barTop + (i * barGap)}
                x2={((chartWidth - chartEndGap) * (cityInfo[curMetricKey] / maxMetricValue)) + xAxisStart}  
                y2={barTop + (i * barGap)}
            ></line>

            <line class="bar-classifier"
                x1={regionStart}
                y1={barTop + (i * barGap)}
                x2={regionStart + 4}
                y2={barTop + (i * barGap)}
                style="
                    stroke: {classifierColours[cityInfo['region']]};
                "
            ></line>

            <text class="axis-label"
                x = {rankStart}
                y = {rankTop + (i * barGap)}
                text-anchor="start"
            >{i + 1}</text>

            <text class="bar-label"
                x={barLabelStart}
                y={barLabelTop + (i * barGap)}
            >{city}</text>
        {/each}
    </svg>
</div>

<style>
	#chart-wrapper {
		margin: 0 auto;
		max-width: 1080px;
		min-width: 300px;
		/* border-top: solid 1px var(--brandDarkBlue);
		border-bottom: solid 1px var(--brandDarkBlue); */
		padding-bottom: 10px;
		margin-bottom: 10px;
		/* padding-left: 10px; */
	}

	#chart {
		margin-top: 10px;
		margin-bottom: 10px;
		background-color: var(--brandWhite);
	}

	.grid-primary {
		stroke: var(--brandLightBlue);
		stroke-width: 1px;
	}

	.grid-secondary {
		stroke: var(--brandDarkBlue);
		stroke-width: 1px;
	}

	.axis-label {
        stroke: 'grey';
		fill: var(--brandBlack);
		font-size: 14px;
	}

    .bar-data {
        stroke: var(--brandBlack);
        stroke-width: 16;
        stroke-opacity: 0.08;
    }

    .bar-classifier {
        stroke-width: 16;
        stroke-opacity: 1;
    }

	.bar-label {
		fill: var(--brandBlack); 
		font-size: 13px;
	}
</style>