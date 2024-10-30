<script>
    export let curCity;
    export let cities;
    cities.sort()

    // const cityImage = import('../assets/city_image/toronto.png');

    import cityImage from '../assets/city_image/tokyo.png';
</script>

<div class="city-compare">
    <select bind:value={curCity}>
        {#each cities as value}
            <option {value}>{value}</option>
        {/each}
    </select>

    <img alt="Urban density overlayed with transit" src={cityImage} />
</div>

<style>
    .city-compare {
        width: 49.5%;
        display: inline-block;
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