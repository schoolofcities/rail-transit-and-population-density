<script>
    export let curCity;
    export let cities;
    cities.sort()
</script>

<div class="city-compare">
    <select bind:value={curCity}>
        {#each cities as value}
            <option {value}>{value}</option>
        {/each}
    </select>

    {curCity} map here
</div>

<style>
    .city-compare {
        width: 49.5%;
        display: inline-block;
    }

    select {
        width: 100%;
    }
</style>