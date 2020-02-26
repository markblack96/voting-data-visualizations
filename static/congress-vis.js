var dataGlobal = [];
function congress(n) {
  // gets the data from the endpoint and visualizes it
  d3.json('/congress/' + n).then(function(data) {
    // all of the below is going to need to follow an exit/update pattern
    let parties = listParties(data);
    // Given parties, let's add divs for each
    for (p in parties) {
      let party = parties[p];
      let partyDiv = document.createElement('div');
      partyDiv.id = party;
      document.getElementById('app').appendChild(partyDiv);
      // now let's separate by party
    }
    


    const congress = d3.select('#congress_holder')
      .selectAll('p')
      .data(data);

    congress.exit().remove();

    congress.text(function(data) { 
      return data.bioname + ', ' + data.party + ', ' + data.state + ', ' + data.district; 
    });

    congress.enter()
      .append('p')
      .text(function(data) { return data.bioname+', '+data.party+', '+data.state+', '+data.district; });
    dataGlobal = data;
  });
}

function showCongress() {
  // get the selected option
  let selectedIndex = document.getElementById('congress_num_select').options.selectedIndex;
  selectedCongress = document.getElementById('congress_num_select').options[selectedIndex].value; // hilariously verbose
  congress(selectedCongress);
}
