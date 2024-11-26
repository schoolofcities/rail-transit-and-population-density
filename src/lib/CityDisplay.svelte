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
        width: 100%;
        max-width: 220px;
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