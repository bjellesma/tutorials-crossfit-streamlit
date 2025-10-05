function toggleCard(card){
    card.classList.toggle('clicked');
    updateStats()
}

function updateStats(){
    const selectedCards = document.querySelectorAll('.athlete-card.clicked');
    const statsSummary = document.getElementById('statsSummary');

    let xAxisTotal = 0;
    let yAxisTotal = 0;

    selectedCards.forEach(card => {
        xAxisTotal += parseFloat(card.dataset[x_axis])
        yAxisTotal += parseFloat(card.dataset[y_axis])
    });

    document.getElementById('xAxisTotal').textContent = xAxisTotal;
    document.getElementById('yAxisTotal').textContent = yAxisTotal;
    document.getElementById('athleteCount').textContent = selectedCards.length;
}