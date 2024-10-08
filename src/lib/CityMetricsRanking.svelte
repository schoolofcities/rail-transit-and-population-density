<script>
    export let curMetric;
    export let curMetricKey;
    export let citiesDens;

    // https://github.com/sveltejs/svelte/issues/13446#issuecomment-2382939034
    let dens = Object.entries(citiesDens);
    $: sortedDens = dens.toSorted(function(a,b) {return a[1][curMetricKey] <= b[1][curMetricKey]})
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
            {#each sortedDens as [city, cityInfo]}
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