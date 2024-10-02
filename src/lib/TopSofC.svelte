<script>
	import logoFull from '/src/assets/top-logo-full.svg';


	let width;

	let barWidth = 262;
	$: if (width < 500) {
		barWidth = 262
	} else {
		barWidth = 383
	}

</script>

<div id="bar" bind:clientWidth={width}>

	<div id="logo" style="width: {barWidth}px">
		<a href="https://www.schoolofcities.utoronto.ca/"><img src={logoFull} alt="School of Cities"></a>
	</div>

</div>

<style>
	#bar {
		position: fixed;
		overflow: hidden;
   		top: 0px;
		height: 50px;
		background-color: var(--brandWhite);
		margin-bottom: 20px;
		border-bottom: 1px solid var(--brandGray);
		width: 100%;
		min-width: 200px;
		padding-left: 0px;
		padding-right: 0px;
		z-index: 99999;
		opacity: 0.98;
		box-shadow: 0 2px 0 0 rgba(224, 224, 224, 0.268);
	}

	#logo {
		margin: auto;
		max-width: 260px;
		height: 50px;
		z-index: 99999;
	}

	a {
		color: black;
	}
	a:hover {
		opacity: 0.5;
	}

	img {
		color: blue;
		height: 50px;
		width: auto;
	}
	img:hover {
		opacity: 0.5;
		cursor: pointer;
	}
</style>
