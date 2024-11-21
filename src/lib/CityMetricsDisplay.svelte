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
        {#if width < (600 - 30)}
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
        width: 100%;
        display: table;
        margin-top: 20px;
        /* border: 2px solid var(--brandDarkBlue); */
    }

    .resp-table-body {
        display: table-row-group;
    }

    .resp-table-row {
        display: table-row;
    }

    .table-body-cell-value {
        width: 20%;
        font-family: TradeGothicLTLight;
        font-size: 16px;
        display: table-cell;
        /* border: 2px solid #c4d4e0; */
        background-color: #ceeff0;
        padding: 8px;
        line-height: 1.42857143;
        vertical-align: top;
    }

    .table-body-cell-header {
        font-family: TradeGothicLTLight;
        font-size: 16px;
        display: table-cell;
        /* border: 2px solid #92abbe; */
        background-color: #7fd4d9;
        padding: 8px;
        line-height: 1.42857143;
        vertical-align: top;
    }
</style>