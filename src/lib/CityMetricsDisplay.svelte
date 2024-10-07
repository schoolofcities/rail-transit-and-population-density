<script>
    export let citiesDens;
    export let cityOne;
    export let cityTwo;
</script>

<!-- https://stackoverflow.com/a/69528090 -->

<div class="resp-table">
    <div class="resp-table-body">
        <div class="resp-table-row"> 
            <div class="table-body-cell">
                {citiesDens[cityOne]['raw_dens'].toFixed(2)}
            </div>
            <div class="table-body-cell">
                Overall Density
            </div>
            <div class="table-body-cell">
                {citiesDens[cityTwo]['raw_dens'].toFixed(2)} 
            </div>
        </div>
        <div class="resp-table-row"> 
            <div class="table-body-cell">
                {citiesDens[cityOne]['floor_dens'].toFixed(2)}
            </div>
            <div class="table-body-cell">
                Modified Density
            </div>
            <div class="table-body-cell">
                {citiesDens[cityTwo]['floor_dens'].toFixed(2)}
            </div>
        </div>
    </div>
</div>