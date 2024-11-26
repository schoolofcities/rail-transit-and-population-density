<script>
    export let citiesDens;
    export let cityOne;
    export let cityTwo;

    export let metrics;
    export let metricsKeys;

    let width;
</script>

<!-- https://stackoverflow.com/a/69528090 -->

<div class="resp-table" bind:offsetWidth={width}>
    <div class="resp-table-body">
        {#if width < (710 - 30)}
            <div class="resp-table-row"> 
                <div class="table-body-cell-header">
                    {cityOne}
                </div>
                <div class="table-body-cell-header">
                </div>
                <div class="table-body-cell-header">
                    {cityTwo} 
                </div>
            </div>
        {/if}

        {#each metrics as metric, i}
            <div class="resp-table-row"> 
                <div class="table-body-cell-value">
                    {citiesDens[cityOne][metricsKeys[i]].toFixed(2)}
                </div>
                <div class="table-body-cell-header">
                    {metric}
                </div>
                <div class="table-body-cell-value">
                    {citiesDens[cityTwo][metricsKeys[i]].toFixed(2)} 
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .resp-table {
        margin: 0 auto;
        width: 100%;
        max-width: 680px;
        display: table;
        margin-top: 20px;
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