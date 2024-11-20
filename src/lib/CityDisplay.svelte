<script>
    export let curCity;
    export let cities;
</script>

<div class="city-compare">
    <select bind:value={curCity}>
        {#each cities as value}
            <option {value}>{value}</option>
        {/each}
    </select>

    {#await import(`../assets/city_image/${curCity.toLowerCase()}.png`) then { default: src }}
        <img {src} alt="" />
    {/await}
</div>

<style>
    .city-compare {
        width: 49.5%;
        display: inline-block;
    }

    @media screen and (max-width: 600px) {
        .city-compare {
            width: 100%;
        }
    }

    select {
        width: 100%;
    }

	img {
		width: 100%;
		height: 100%;
        border-radius: 50%;
	}
</style>