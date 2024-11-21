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
		/* https://stackoverflow.com/a/73036389 */
		display: flex;
		/* flex-wrap: wrap; */
		flex-direction: row;
		justify-content: space-around;
		flex-flow: wrap;
		padding-top: 10px;
	}

	.button {
		width: 225px;
		height: 30px;
		float: left;
		border: 2px solid var(--brandDarkBlue);
		background-color: #f5fcfc;
		margin-top: 5px;
		margin-bottom: 5px;
	}

	@media screen and (max-width: 550px) {
		.button {
			width: 90%;
		}
	}

	.button:hover {
		cursor: pointer;
	}

	.box {
		height: 100%;
		width: 15px;
		/* border: solid 1px var(--brandDarkBlue); */
		float: left;
	}

	.name {
		font-family: TradeGothicLTLight;
		overflow: hidden;
		padding: 6px;
		color: var(--brandBlack);
		font-size: 14px;
	}

	.name:hover {
		opacity: 0.7;
	}
</style>