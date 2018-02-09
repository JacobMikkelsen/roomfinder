"use strict";

// https://www.epochconverter.com/weeknumbers
Date.prototype.getWeek = function () {
    var target  = new Date(this.valueOf());
    var dayNr   = (this.getDay() + 6) % 7;
    target.setDate(target.getDate() - dayNr + 3);
    var firstThursday = target.valueOf();
    target.setMonth(0, 1);
    if (target.getDay() != 4) {
        target.setMonth(0, 1 + ((4 - target.getDay()) + 7) % 7);
    }
    return 1 + Math.ceil((firstThursday - target) / 604800000);
}

function appendRoomTypes(form){
    var roomTypes = document.getElementsByName("room_type");

    for (var i = 0; i < roomTypes.length; i++){
        if (roomTypes[i].checked){
            console.log("Appending {RU[], " + roomTypes[i].value + "}");
            form.append("RU[]", roomTypes[i].value);
        }
    }

    // form.append("RU[]", "RU_GP-LEC");
    // form.append("RU[]", "RU_GP-TUTSEM");
}

function findRooms(){

    // TODO, wipe existing content in DOM, add spinner

    var request = createRequest();

    // TODO Assuming user is in UNSW timezone
    var d = new Date();
    
    var dayString = weekdayFromIndex(d.getDay());
    
    var fr_time = dateToTimeIndex(d);
    var to_time = fr_time + 2;
    
    var week = d.getWeek();

    // TODO IE doesn't support FormData... craft our own string payload and use url encoded?
    var form = new FormData();
    form.append("search_rooms", "Search");
    form.append("days[]", dayString);
    form.append("fr_week", week.toString());
    form.append("to_week", week.toString());
    form.append("fr_time", fr_time.toString());
    form.append("to_time", to_time.toString());

    appendRoomTypes(form);
    
    var minString = d.getMinutes() >= 30 ? "30" : "00";

    addToDOM("Rooms free today between " + d.getHours() + ":" + minString + " and " + ((d.getHours() + 1)%24) + ":" + minString);

    request.send(form);
}

function createRequest(){
    // TODO This cors thing works but... Doesn't seem ideal

    var cors = "https://cors-anywhere.herokuapp.com/";
    var url = "http://nss.cse.unsw.edu.au/tt/find_rooms.php?dbafile=2018-KENS-COFA.DBA&campus=KENS";

    var request = new XMLHttpRequest();
    request.open("POST", cors + url);
    
    request.onreadystatechange = function(){
        // TODO Could improve by checking for 3, 'progress', so we can update
        //      the DOM as more comes in. The whole content comes in each time
        //      though... So we could peg the last character, len(response), to
        //      start reading from in the next response? Process the new stuff
        //      each time?
        
        // TODO wipe exisiting content in DOM, then add the data we got

        // Note: 4 is DONE
        if (request.readyState === 4){
            // TODO check response status to see if it actually worked
            processResponse(request.responseText);
        }
    };

    return request;
};

function dateToTimeIndex(d){
    var hour = d.getHours();
    
    // Flag if we have 30 minutes or more
    var half = d.getMinutes() >= 30 ? 1 : 0;
    
    return hour * 2 + half;
}

function weekdayFromIndex(index){
    // TODO Error checking, i.e. index out for bounds
    var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    return weekdays[index];
}

function processResponse (response){
    
    var rows = getRows(response);
    addToDOM("Found " + rows.length + " rooms");
    var rooms = getRooms(rows);
    
    var len = rooms.length;
    
    for (var i = 0; i < len; i++){
        addToDOM(rooms[i][1]);
    }
}

function getRows(response){
    var rowPattern = /<tr class=\"[\s\S]+?tr>/g;
    
    return response.match(rowPattern);
}

function getRooms(rows){
    var detailsPattern = /<td class=\"data\">(.+?)<\/td>/g;
    var len = rows.length;
    
    // TODO: Set array length for performance?
    var rooms = [];
    
    for (var i = 0; i < len; i++){
        var details = [];
        var match;
        
        while ((match = detailsPattern.exec(rows[i])) !== null){
            details.push(match[1]);
        }
        
        rooms.push(details);
    }
    
    return rooms;
}

function addToDOM (string){
    // TODO Gross! Get rid of this!
    var body = document.getElementsByClassName("container")[0];
    var p = document.createElement("p");
    p.appendChild(document.createTextNode(string));
    body.appendChild(p);
}

function main(){
    // Just for testing
}

main();