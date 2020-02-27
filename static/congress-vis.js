var dataGlobal = [];
var partiesAndMembers;
function congress(n) {
  // gets the data from the endpoint and visualizes it
  d3.json('/congress/' + n).then(function(data) {
    let parties = listParties(data);
    let membersOfParties = {};
    // remove any and all pre-existing party divs
    d3.selectAll('.party').remove();
    // Given parties, let's add divs for each
    for (p in parties) {
      let party = parties[p];
      let partyDiv = document.createElement('div');
      partyDiv.id = party;
      partyDiv.className = "party";
      document.getElementById('app').appendChild(partyDiv); // we really could use d3 for this...
      // now let's separate by party
      membersOfParties[party] = data.filter(function(d) {
        return d.party === party;
      })
      partiesAndMembers = membersOfParties;
    }
    const partyDivs = d3.select('#app').selectAll('div .party').data(Object.keys(membersOfParties))
    partyDivs.enter().append('div').attr("class", "party").text(function(d, i) { return d;})
    let idx = 0; // time to hack!
    for (p in membersOfParties) {
      let header = document.createElement('h3');
      header.textContent = p;
      document.getElementById(p).append(header);
      d3.select('#' + p).selectAll('p').data(membersOfParties[p]).enter().append('p')
        .text(function(d) { return d.bioname; });
      
      let svg = d3.select('svg').append('g').attr("class", p);
      svg.attr("transform", "translate("+idx*150+")");
      svg.data(Object.keys(membersOfParties)).exit().remove();      
      let congress = svg.selectAll('circle').data(membersOfParties[p])
        .attr("cx", function(d, i) { return 10 + i%10 * 15;})
        .attr("cy", function(d, i) { return 10 + Math.floor(i/10) * 15; })
        .attr("r", 10+"px");

      congress.enter().append("circle")
        .attr("cx", function(d, i) { return 10 + i%10 * 15;})
        .attr("cy", function(d, i) { return 10 + Math.floor(i/10) * 15; })
        .attr("r", 10+"px");

      congress.exit().remove();
      idx+=1;
    }

    /* const congress = d3.select('#congress_holder')
      .selectAll('p')
      .data(data);

    congress.exit().remove();

    congress.text(function(data) { 
      return data.bioname + ', ' + data.party + ', ' + data.state + ', ' + data.district; 
    });

    congress.enter()
      .append('p')
      .text(function(data) { return data.bioname+', '+data.party+', '+data.state+', '+data.district; });*/
    dataGlobal = data;
  });
}

function showCongress() {
  // get the selected option
  let selectedIndex = document.getElementById('congress_num_select').options.selectedIndex;
  selectedCongress = document.getElementById('congress_num_select').options[selectedIndex].value; // hilariously verbose
  congress(selectedCongress);
}
