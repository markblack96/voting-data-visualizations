// my function junk drawer
function listParties(data) {
  let parties = [];
  for (d in data) {
    if (parties.find(function(datum) { return datum === data[d].party; }) === undefined) {
      parties.push(data[d].party);
    }
  }
  return parties;
}
function fetchVotes(icpsr, congressNum) {
  // uses icpsr and congressNum to retrieve voting data for individual congresspersons
  fetch('/votes/'+icpsr+'/'+congressNum).then(
    //todo: this
  );
}