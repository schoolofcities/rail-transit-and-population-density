<script>
    import '../assets/styles.css'; 
    import TopSofC from "../lib/TopSofC.svelte";

    let curCityOne = "Toronto";
    let curCityTwo = "Chicago";

    let curMetric = "Overall density";

    const cities = [
        "Chicago",
        "Delhi",
        "Tokyo",
        "Toronto",
    ];

    const metrics = [
        "Overall density",
        "Modified density",
        "Transit density"
    ];

    function handleCityOneChange(event) {
        const selectedValue = event.target.value;

    }
</script>

<svelte:head>
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1, minimum-scale=1"
    />
</svelte:head>

<TopSofC />

<main>
    <div class="title">
        <h1>Comparing Transit-Oriented Density</h1>
        <p>
            Aniket Kali, Jeff Allen
        </p>
        <p>
            Published TBD
        </p>
    </div>

    <div class="text">
        <p>Info/background on project...</p>
        <h3>Compare Cities</h3>
        <div class="city-compare">
            <select bind:value={curCityOne}>
                {#each cities as value}
                    <option {value}>{value}</option>
                {/each}
            </select>

            {curCityOne}
        </div>

        <div class="city-compare">
            <select bind:value={curCityTwo}>
                {#each cities as value}
                    <option {value}>{value}</option>
                {/each}
            </select>

            {curCityTwo}
        </div>

        <p>Info on method...</p>
        <p>Commentary...</p>
    </div>

    <div class="text">
        <h3>Rank Cities</h3>
        <p>Info/background...</p>

        <select bind:value={curMetric}>
            {#each metrics as value}
                <option {value}>{value}</option>
            {/each}
        </select>
    </div>

    <div class="text">
        <h3>Appendix</h3>
        <p>Footnotes on methods etc...</p>
        <p>Link to code/data...</p>
    </div>
</main>

<style>
    .city-compare {
        width: 49.5%;
        display: inline-block;
    }

    select {
        width: 100%;
    }
</style>