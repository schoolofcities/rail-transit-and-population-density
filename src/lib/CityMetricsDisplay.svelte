<script>
    export let cityMetrics;
    export let cityOne;
    export let cityTwo;

    export let metrics;
    export let metricsKeys;

    let width;

    function nearestHun(n) { 
        return Math.round(n / 100) * 100; 
    }

    function numberWithCommas(n) {  // https://stackoverflow.com/a/10899795
        var parts=n.toString().split(".");
        return parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",") + (parts[1] ? "." + parts[1] : "");
    }
</script>

<!-- https://stackoverflow.com/a/69528090 -->

<div>
    <div class="city-header">
        <div class="city-label">
            {cityOne}
        </div>
        <div class="city-label">
            {cityTwo}
        </div>
    </div>

    <div class="resp-table" bind:offsetWidth={width}>
        <div class="resp-table-body">
            {#each metrics as metric, i}
                <div class="resp-table-row"> 
                    <div class="table-body-cell-value">
                        {#if metric.includes('Concentration')}
                            {cityMetrics[cityOne][metricsKeys[i]].toFixed(2)}
                        {:else if metric.includes('%')}
                            {cityMetrics[cityOne][metricsKeys[i]].toFixed(1)}%
                        {:else if metric == "Urban population"}
                            {(cityMetrics[cityOne][metricsKeys[i]] / (10 ** 6)).toFixed(2)}M
                        {:else}
                            {numberWithCommas(nearestHun(cityMetrics[cityOne][metricsKeys[i]]))}
                        {/if}
                    </div>
                    <div class="table-body-cell-header">
                        {metric}
                    </div>
                    <div class="table-body-cell-value">
                        {#if metric.includes('Concentration')}
                            {cityMetrics[cityTwo][metricsKeys[i]].toFixed(2)}
                        {:else if metric.includes('%')}
                            {cityMetrics[cityTwo][metricsKeys[i]].toFixed(1)}%
                        {:else if metric == "Urban population"}
                            {(cityMetrics[cityTwo][metricsKeys[i]] / (10 ** 6)).toFixed(2)}M
                        {:else}
                            {numberWithCommas(nearestHun(cityMetrics[cityTwo][metricsKeys[i]]))} 
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    .city-header {
        margin: 0 auto;
        width: 100%;
        max-width: 680px;
        margin-top: 20px;
        border-top: 1px solid var(--brandLightBlue);
        color: var(--brandDarkBlue);
        display: flex;
        justify-content: space-between;
    }

    .city-label {
        font-family: TradeGothicLTLight;
        text-align: center;
        background-color: #ffffff;
        padding: 8px;
        line-height: 1.42857143;
        vertical-align: top;
    }

    .resp-table {
        margin: 0 auto;
        width: 100%;
        max-width: 680px;
        display: table;
        color: var(--brandDarkBlue);
        /* border: 2px solid var(--brandDarkBlue); */
    }

    .resp-table-body {
        display: table-row-group;
    }

    .resp-table-row {
        display: table-row;
        /* border-top: solid 1px grey; */
    }

    .table-body-cell-value {
        width: 12%;
        font-family: TradeGothicBold;
        font-size: 16px;
        display: table-cell;
        text-align: center;
        border-top: 1px solid var(--brandLightBlue);
        background-color: #6fc7ea2e;
        padding: 8px;
        line-height: 1.42857143;
        vertical-align: top;
    }

    .table-body-cell-header {
        font-family: TradeGothicLTLight;
        font-size: 16px;
        display: table-cell;
        text-align: center;
        border-top: 1px solid var(--brandLightBlue);
        background-color: #ffffff;
        padding: 8px;
        line-height: 1.42857143;
        vertical-align: top;
    }
</style>