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
                <div class="table-body-cell">
                    {cityOne}
                </div>
                <div class="table-body-cell">
                </div>
                <div class="table-body-cell">
                    {cityTwo} 
                </div>
            </div>
        {/if}

        {#each metrics as metric, i}
            <div class="resp-table-row"> 
                <div class="table-body-cell">
                    {citiesDens[cityOne][metricsKeys[i]].toFixed(2)}
                </div>
                <div class="table-body-cell">
                    {metric}
                </div>
                <div class="table-body-cell">
                    {citiesDens[cityTwo][metricsKeys[i]].toFixed(2)} 
                </div>
            </div>
        {/each}
    </div>
</div>