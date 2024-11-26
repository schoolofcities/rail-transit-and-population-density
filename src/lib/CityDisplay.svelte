<script>

    import "../assets/styles.css";

    export let curCity;
    export let cities;

</script>



<div class="city-compare">
    

    {#await import(`../assets/city_image/${curCity.toLowerCase()}.png`) then { default: src }}
        <img {src} alt="" />
    {/await}

    <select bind:value={curCity}>
        {#each cities as value}
            <option {value}>{value}</option>
        {/each}
    </select>
</div>



<style>
    .city-compare {
        width: 48%;
        display: inline-block;
        vertical-align: top;
        text-align: center; /* Centers text and inline elements */
        position: relative; /* For flex alignment */
        padding-left: 15px;
    }

    select {
        display: block;
        margin: 0 auto; /* Horizontally center the select */
        width: 100%;
        max-width: 200px;
        color: var(--brandDarkBlue);
        background-color: white;
        border: solid 1px var(--brandLightBlue);
        border-radius: 5px;
        margin-top: 10px;
        padding: 3px;
	    padding-left: 5px;
        font-size: 14px;   
    }

    img {
        width: 100%;
        height: auto;
        border-radius: 50%;
        border: solid 1px var(--brandLightBlue);
    }

    @media screen and (max-width: 600px) {
        .city-compare {
            width: 100%;
            padding-left: 0px;
        }
    }
</style>