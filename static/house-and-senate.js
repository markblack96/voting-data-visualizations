// house and senate visualizations, separated

// retrieves house & senate data from the api and displays it
var dataGlobal;
const bioTemplate = (person)=>{
    return `
        <h5>${person.bioname}</h5>
        <ul>
            <li>${person.chamber}</li>
            <li>${person.party}</li>
            <li>${person.state}${person.chamber === 'House' ? ", district " + person.district : ''}</li>
        </ul>
        <button class="button" id="showVotes">Show Votes</button>
        <div id="votes"></div>
    `
}
function congress(n) {
    d3.json('/congress/' + n).then(function(data) {
        dataGlobal = data;
        let parties = listParties(data);
        let chambers = ['House', 'Senate'];
        // Goal: use two different svgs for house and senate SVGs

        // house
        let houseData = data.filter(function(d){
            if (d.chamber === 'House') {
                return d;
            }
        });
        let houseMembersByParty = {};
        for (p in parties) {
            let party = parties[p];
            houseMembersByParty[party] = houseData.filter(
                function(d) { return d.party===party; }
            )
        }
        // sort house data by size of party so largest parties get display first
        parties.sort(function(a, b) {
            return houseMembersByParty[b].length - houseMembersByParty[a].length;
        });
        if (Object.keys(houseMembersByParty).length > 2) {
            d3.select('svg.house').attr('width', function() {
                return Object.keys(houseMembersByParty).length * 200;
            })
        }
        // idea: manage state for g (x, y) coords with an object
        let positions = [];
        for (var i=0; i<parties.length; i++) {
            let x = (i, prevParty)=> {
                if (i > 0){
                    if (prevParty.length < 10) {
                        return positions[i-1].x + (20*prevParty.length);
                    } else {
                        return positions[i-1].x + 200;
                    }
                } else {
                    return 0;
                }
            }
            positions.push({
                'class': parties[i].replace(".", "").replace(' ', ''),
                'x': x(i, houseMembersByParty[parties[i-1]])
                
            })
        }
        console.log(positions);

        let g = d3.select('.house')
            .selectAll('g')
            .data(parties)
                .attr('class', function(d) { return d.replace(".", "").replace(' ', '');})
                .attr('transform', function(d, i) {
                    let translateFactor = 0;
                    if (i>0 && houseMembersByParty[parties[i-1]].length <= 5) {
                        translateFactor = 100;
                    }
                    return "translate(" + (positions.find(party => party.class === d.replace(".", "").replace(' ', '')).x) + ")";
                })
        
        g.enter().append('g')
            .attr('class', function(d) { return d.replace(".", "").replace(' ', '');})
            .attr('transform', function(d, i) {
                let translateFactor = 0;
                if (i>0 && houseMembersByParty[parties[i-1]].length <= 5) {
                    translateFactor = 100;
                }
                return "translate(" + (positions.find(party => party.class === d.replace(".", "").replace(' ', '')).x) + ")";// "translate(" + (i * 200 - translateFactor) + ")"; 
            });

        g.exit().remove();

        let houseMembers = d3.selectAll('svg.house g')
            .data(parties).selectAll('circle')
            .data(function(d) {return houseMembersByParty[d];}) // get party members in chamber
                .attr('cx', function(d, i){return 10 + i%10 * 20;})
                .attr('cy', function(d, i){return 10 + Math.floor(i/10) * 20;})
                .attr('r', 8+'px')
                .on('mouseover', function(d) { 
                    d3.select(this).attr('stroke-width', 3);
                    d3.select('.tooltip').transition().duration(100).style('opacity', 0.9);
                    d3.select('.tooltip').html(`
                        <h5>${d.bioname}</h5>
                        <ul>
                            <li>${d.party}</li>
                            <li>{d.state}${d.chamber === 'House' ? ", district " + d.district : ''}</li>
                        </ul>
                    `);
                    d3.select('.tooltip')
                        .style('left', d3.event.pageX + 'px')
                        .style('top', d3.event.pageY - 28 + 'px');
                }).on('mouseout', function(d) { 
                    d3.select(this).attr('stroke-width', 1) 
                    d3.select('.tooltip').style('opacity', 0);
                }).on('click', function(d) {
                    // set biography data
                    d3.select('#biography')
                        .html(`
                        <h5>${d.bioname}</h5>
                        <ul>
                            <li>${d.party}</li>
                            <li>${d.state}${d.chamber === 'House' ? ", district " + d.district : ''}</li>
                        </ul>
                    `)
                });
        
        houseMembers.enter().append('circle')
            .attr('cx', function(d, i){return 10 + i%10 * 20;})
            .attr('cy', function(d, i){return 10 + Math.floor(i/10) * 20;})
            .attr('r', 8+'px')
            .on('mouseover', function(d) { 
                d3.select(this).attr('stroke-width', 3);
                d3.select('.tooltip').transition().duration(100).style('opacity', 0.9);
                d3.select('.tooltip').html(`
                <h5>${d.bioname}</h5>
                <ul>
                    <li>${d.party}</li>
                    <li>${d.state}, district ${d.district}</li>
                </ul>
            `);
                d3.select('.tooltip')
                        .style('left', d3.event.pageX + 'px')
                        .style('top', d3.event.pageY + 'px');
            }).on('mouseout', function(d) { 
                d3.select(this).attr('stroke-width', 1) 
                d3.select('.tooltip').style('opacity', 0);
            }).on('click', function(d) {
                // set biography data
                d3.select('#biography')
                    .html(`
                    <h5>${d.bioname}</h5>
                    <ul>
                        <li>${d.party}</li>
                        <li>${d.state}${d.chamber === 'House' ? ", district " + d.district : ''}</li>
                    </ul>
                `)
            });
        houseMembers.exit().remove();

        // now do senate
        let senateData = data.filter(function(d){
            if (d.chamber === 'Senate') {
                return d;
            }
        });
        let senatorsByParty = {};
        for (p in parties) {
            let party = parties[p];
            senatorsByParty[party] = senateData.filter(
                function(d) { return d.party===party; }
            )
        }

        positions = [];
        for (var i=0; i<parties.length; i++) {
            let x = (i, prevParty)=> {
                if (i > 0){
                    if (prevParty.length < 10) {
                        return positions[i-1].x + (20*prevParty.length);
                    } else {
                        return positions[i-1].x + 200;
                    }
                } else {
                    return 0;
                }
            }
            positions.push({
                'class': parties[i].replace(".", "").replace(' ', ''),
                'x': x(i, senatorsByParty[parties[i-1]])// i > 0 ?  positions[i-1].x + 20 * houseMembersByParty[parties[i-1]].length : 0
                
            })
        }

        g = d3.select('svg.senate')
            .selectAll('g')
            .data(parties)
                .attr('class', function(d) { return d.replace(".", "").replace(' ', '');})
                .attr('transform', function(d, i) {
                    let translateFactor = 0;
                    if (i>0 && houseMembersByParty[parties[i-1]].length <= 5) {
                        translateFactor = 100;
                    }
                    return "translate(" + (positions.find(party => party.class === d.replace(".", "").replace(' ', '')).x) + ")";// "translate(" + (i * 200 - translateFactor) + ")"; 
                });
        
        g.enter().append('g')
            .attr('class', function(d) { return d.replace(".", "").replace(' ', '');})
            .attr('transform', function(d, i) {
                let translateFactor = 0;
                if (i>0 && houseMembersByParty[parties[i-1]].length <= 5) {
                    translateFactor = 100;
                }
                return "translate(" + (positions.find(party => party.class === d.replace(".", "").replace(' ', '')).x) + ")";// "translate(" + (i * 200 - translateFactor) + ")"; 
            });

        g.exit().remove();

        let senateMembers = d3.selectAll('svg.senate g')
            .data(parties).selectAll('circle')
            .data(function(d) {return senatorsByParty[d];}) // get party members in chamber
                .attr('cx', function(d, i){return 10 + i%10 * 20;})
                .attr('cy', function(d, i){return 10 + Math.floor(i/10) * 20;})
                .attr('r', 8+'px')
                .on('mouseover', function(d) { 
                    d3.select(this).attr('stroke-width', 3);
                    d3.select('.tooltip').transition().duration(100).style('opacity', 0.9);
                    d3.select('.tooltip').html(`
                    <h5>${d.bioname}</h5>
                    <ul>
                        <li>${d.party}</li>
                        <li>${d.state}</li>
                    </ul>
                `);
                    d3.select('.tooltip')
                            .style('left', d3.event.pageX + 'px')
                            .style('top', d3.event.pageY - 28 + 'px');
                }).on('mouseout', function(d) { 
                    d3.select(this).attr('stroke-width', 1) 
                    d3.select('.tooltip').style('opacity', 0);
                }).on('click', function(d) {
                    // set biography data
                    d3.select('#biography')
                        .html(`
                            <h5>${d.bioname}</h5>
                            <ul>
                                <li>${d.party}</li>
                                <li>${d.state}${d.chamber === 'House' ? ", district " + d.district : ''}</li>
                            </ul>
                        `)
                });
        
        senateMembers.enter().append('circle')
            .attr('cx', function(d, i){return 10 + i%10 * 20;})
            .attr('cy', function(d, i){return 10 + Math.floor(i/10) * 20;})
            .attr('r', 8+'px')
            .on('mouseover', function(d) { 
                d3.select(this).attr('stroke-width', 3);
                d3.select('.tooltip').transition().duration(100).style('opacity', 0.9);
                d3.select('.tooltip').html(`
                    <h5>${d.bioname}</h5>
                    <ul>
                        <li>${d.party}</li>
                        <li>${d.state}</li>
                    </ul>
                `);
                d3.select('.tooltip')
                        .style('left', d3.event.pageX + 'px')
                        .style('top', d3.event.pageY - 28 + 'px');
            }).on('mouseout', function(d) { 
                d3.select(this).attr('stroke-width', 1) 
                d3.select('.tooltip').style('opacity', 0);
            }).on('click', function(d) {
                // set biography data
                d3.select('#biography')
                    .html(`
                        <h5>${d.bioname}</h5>
                        <ul>
                            <li>${d.party}</li>
                            <li>${d.state}</li>
                        </ul>
                    `)
            });
        senateMembers.exit().remove();

    });
}

function showCongress() {
    // get the selected option
    let selectedIndex = document.getElementById('congress_num_select').options.selectedIndex;
    let selectedCongress = document.getElementById('congress_num_select').options[selectedIndex].value; // hilariously verbose
    congress(selectedCongress);
  }
  