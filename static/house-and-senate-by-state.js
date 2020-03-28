// Script for state-by-state visualization (easier navigation than party viewer, use by default)

function congressByState(n) {
    document.querySelector('#congress-vis').hidden = false;
    d3.json('/congress/' + n).then((data)=>{
        // let parties = listParties(data);
        let states = listStates(data);
        let chambers = ['House', 'Senate'];
        
        // house
        let houseData = data.filter(function(d){
            if (d.chamber === 'House') {
                return d;
            }
        });
        let houseMembersByState = {};
        for (s in states) {
            let state = states[s];
            houseMembersByState[state] = houseData.filter(
                function(d) { return d.state===state; }
            )
        }
        console.log(houseMembersByState);
        
    })
}