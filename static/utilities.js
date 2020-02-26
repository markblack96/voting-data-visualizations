function listParties(data) {
  let parties = [];
  for (d in data) {
    if (parties.find(function(datum) { return datum === data[d].party; }) === undefined) {
      parties.push(data[d].party);
    }
  }
  return parties;
}
