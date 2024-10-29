<script>
    import '../assets/styles.css'; 

    import TopSofC from "../lib/TopSofC.svelte";
    import CityDisplay from '../lib/CityDisplay.svelte';
    import CityMetricsDisplay from '../lib/CityMetricsDisplay.svelte';
    import CityMetricsRanking from '../lib/CityMetricsRanking.svelte';

    import citiesDens from "../data/cities_dens.json"

    const cities = Object.keys(citiesDens);

    let curCityOne = "Toronto";
    let curCityTwo = "Chicago";

    const metrics = [
        "General density",
        "Urban density",
        "Station density",
        "% Urban pop near transit",
        "% Urban area near transit",
        "Ratio of urban population and area near transit"
    ];

    const metricsKeys = [
        "raw_dens",
        "urban_dens",
        "station_dens",
        "transit_pop_pct",
        "transit_area_pct",
        "transit_ratio",
    ];

    let curMetric = metrics[0];
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

        <CityMetricsDisplay citiesDens={citiesDens} cityOne={curCityOne} cityTwo={curCityTwo} metrics={metrics} metricsKeys={metricsKeys} />

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