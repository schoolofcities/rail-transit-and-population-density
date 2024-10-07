<script>
    export let curMetric;
    export let curMetricKey;
    export let citiesDens;

    let dens = Object.entries(citiesDens);
    $: dens.sort(function(a,b) {return a[1][curMetricKey] <= b[1][curMetricKey]});
</script>

<div class="table-container">
    <div class="resp-table">
        <div class="resp-table-body">
            <div class="resp-table-row"> 
                <div class="table-body-cell">
                    City
                </div>
                <div class="table-body-cell">
                    {curMetric}
                </div>
            </div>
            {#each dens as [city, cityInfo]}
            <div class="resp-table-row"> 
                <div class="table-body-cell">
                    {city}
                </div>
                <div class="table-body-cell">
                    {cityInfo[curMetricKey].toFixed(2)}
                </div>
            </div>
            {/each}
        </div>
    </div>
</div>

<style>
    .table-container {
        overflow-y: scroll;
        height: 300px;
        display: block;
    }
</style>