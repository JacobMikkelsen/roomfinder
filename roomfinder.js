"use strict";

// XMLHTTPRequest for POST etc.

function sendRequest (){
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
        
        // Note: 4 is DONE
        if (request.readyState === 4){
            // TODO check response status to see if it actually worked
            processResponse(request.responseText);
        }
    };

    // TODO Entry calculation
    var form = new FormData();
    form.append("search_rooms", "Search");
    form.append("days[]", "Wednesday");
    form.append("fr_week", "4");
    form.append("to_week", "4");
    form.append("fr_time", "14");
    form.append("to_time", "16");
    form.append("RU[]", "RU_GP-LEC");
    form.append("RU[]", "RU_GP-TUTSEM");
    // "days[]": days,
    // "fr_week": fr_week,
    // "to_week": to_week,
    // "fr_time": fr_time,
    // "to_time": to_time,
    // "RU[]": ["RU_GP-LEC", "RU_GP-TUTSEM"]

    request.send(form);
}

function processResponse (response){
    
    var rows = getRows(response);
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
    var body = document.getElementsByTagName("body")[0];
    var p = document.createElement("p");
    p.appendChild(document.createTextNode(string));
    body.appendChild(p);
}

function main (){
    addToDOM("Helo");
    sendRequest();
}

main();
