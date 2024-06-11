document.getElementById('filter-button').addEventListener('click', function() {
    var filterSection = document.getElementById('filter-section');
    if (filterSection.style.display === 'flex') {
        filterSection.style.display = 'none';
    } else {
        filterSection.style.display = 'flex';
    }
});
