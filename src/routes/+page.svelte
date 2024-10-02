<script>
    import '../assets/styles.css'; 
    import TopSofC from "../lib/TopSofC.svelte";
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
        ... comparison ...
        <p>Info on method...</p>
        <p>Commentary...</p>
    </div>

    <div class="text">
        <h3>Rank Cities</h3>
        <p>Info/background...</p>
        ... ranking ...
    </div>

    <div class="text">
        <h3>Appendix</h3>
        <p>Footnotes on methods etc...</p>
        <p>Link to code/data...</p>
    </div>
</main>
