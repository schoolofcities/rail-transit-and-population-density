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
        padding-top: 10px;
    }

    select {
        width: 100%;
        max-width: 220px;
    }

    img {
        width: 100%;
        max-width: 600px;
        height: auto;
        border-radius: 50%;
        border: solid 1px var(--brandLightBlue);
        box-shadow: 0 0 15px 10px rgba(214, 214, 214, 0.35);
    }

    @media screen and (max-width: 880px) {
        .city-compare {
            width: 100%;
            padding-left: 0px;
        }
    }

</style>