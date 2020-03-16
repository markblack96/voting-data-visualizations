// my function junk drawer
function voteTemplate(data) {
  return `
    <br>
    <div class="vote-info box bo-h">
      <ul>
        <li><h5>${data.dtl_desc === 'nan' ? data.vote_question : data.dtl_desc}</h5></li>
        <li>${data.date}</li>
        <li>${data.cast}</li>
        <li>Yea: ${data.yea_count}, Nay: ${data.nay_count}</li>
      </ul>
    </div>
  `
}
function listParties(data) {
  let parties = [];
  for (d in data) {
    if (parties.find(function(datum) { return datum === data[d].party; }) === undefined) {
      parties.push(data[d].party);
    }
  }
  return parties;
}
function getVotes(icpsr, congressNum) {
  // uses icpsr and congressNum to retrieve voting data for individual congresspersons
  d3.json('/votes/'+icpsr+'/'+congressNum).then((data)=>{
      // clear previous vote info
      console.log(data);
      for (d in data) {
        let div = document.createElement('div');
        div.innerHTML = voteTemplate(data[d]);
        document.querySelector('#biography').appendChild(div);
      }
    }
  );
}