function congress(n) {
  // gets the data from the endpoint and visualizes it
  
  d3.json('/congress/' + n).then(function(data) {
    const congress = d3.select('body')
      .selectAll('p')
      .data(data);

    congress.exit().remove();

    congress.text(function(data) { return data.bioname; });

    congress.enter()
      .append('p')
      .text(function(data) { return data.bioname; });

  });
}

function showCongress() {
  // get the selected option
  let selectedIndex = document.getElementById('congress_num_select').options.selectedIndex;
  selectedCongress = document.getElementById('congress_num_select').options[selectedIndex].value; // hilariously verbose
  congress(selectedCongress);
}
