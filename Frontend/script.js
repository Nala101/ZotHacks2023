

const UTC_RADIUS = 360;

let serverUrl = 'http://127.0.0.1:5000/results';

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

function SortInfo(searchResults){

    let results = searchResults;

    // let UTC = results.filter(onlyUTC);
    // let outUTC = results.filter(outsideUTC);
    
    console.log(results);
}


function displayResults(){


}


getResturantsInAreaUCI()
