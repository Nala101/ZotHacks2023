

const UTC_RADIUS = 360;

let serverUrl = 'http://127.0.0.1:5001/results';

function getResturantsInAreaYelp() {
    fetch(serverUrl)
        .then(res => res.json())
        .then(SortInfo);
}

function getResturantsInAreaUCI(){
    fetch('./on_campus_locations.json')
    .then((response) => response.json())
    .then((json) => console.log(json));

}

function onlyUTC(resturant) {
  return resturant.distance < UTC_RADIUS;
}
function outsideUTC(resturant) {
    return resturant.distance > UTC_RADIUS;
}


function SortInfo(searchResults){

    let results = JSON.parse(searchResults);

    let UTC = results.filter(onlyUTC);
    let outUTC = results.filter(outsideUTC);
    
    console.log(onlyUTC);
}


function displayResults(){


}


getResturantsInAreaUCI()
getResturantsInAreaYelp()