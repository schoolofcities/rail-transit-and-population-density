<script>
    import '../assets/styles.css'; 

    import TopSofC from "../lib/TopSofC.svelte";
    import CityDisplay from '../lib/CityDisplay.svelte';
    import CityMetricsDisplay from '../lib/CityMetricsDisplay.svelte';
    import CityMetricsRanking from '../lib/CityMetricsRanking.svelte';

    import citiesDens from "../data/cities_dens.json"
    for (const city in citiesDens) {
        for (const metric in citiesDens[city]) {
            if (citiesDens[city][metric] === null) citiesDens[city][metric] = 0;
        }
    }

    const cities = Object.keys(citiesDens);

    let curCityOne = "Toronto";
    let curCityTwo = "Chicago";

    const metrics = [
        "Overall density",
        "Modified density",
        "Transit density"
    ];

    const metricsKeys = [
        "raw_dens",
        "floor_dens",
        "transit_dens"
    ];

    let curMetric = "Overall density";
    $: curMetricKey = metricsKeys[metrics.indexOf(curMetric)];
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

        <CityDisplay cities={cities} bind:curCity={curCityOne} />

        <CityDisplay cities={cities} bind:curCity={curCityTwo} />

        <CityMetricsDisplay citiesDens={citiesDens} cityOne={curCityOne} cityTwo={curCityTwo} />

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

        <CityMetricsRanking curMetric={curMetric} curMetricKey={curMetricKey} citiesDens={citiesDens} />
    </div>

    <div class="text">
        <h3>Appendix</h3>
        <p>Footnotes on methods etc...</p>
        <p>Link to code/data...</p>
    </div>
</main>

<style>
    select {
        width: 100%;
    }
</style>