<script>
	export let classifiers;
	export let classifierColours;

	function handleClick(name) {
		if (classifiers.includes(name)) {
			classifiers = classifiers.filter(item => item !== name);
		} else {
			classifiers = [...classifiers, name];
		}
	}
</script>

<div class="buttons">
	{#each Object.entries(classifierColours) as [classifier, colour]}
		<div
			class="button"
			aria-hidden="true"
			on:click={() => handleClick(classifier)}
			style="color: white; opacity: {classifiers.includes(classifier) ? 1 : 0.333}"
		>
			<div class="box" style="background-color: {colour}"></div>
			<div class="name">
				{classifier}
			</div>
		</div>
	{/each}
</div>

<style>
	.buttons {
		display: flex;
		flex-wrap: wrap;
		/* max-width: 750px; */
	}

	.button {
		width: 225px;
		float: left;
	}

	.button:hover {
		cursor: pointer;
	}

	.box {
		height: 15px;
		width: 15px;
		border: solid 1px var(--brandDarkBlue);
		float: left;
	}

	.name {
		overflow: hidden;
		padding-left: 5px;
		color: var(--brandBlack);
		font-size: 15px;
	}

	.name:hover {
		opacity: 0.7;
	}
</style>