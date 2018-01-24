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
    var regex = /(<tr class=\".+?tr>)/;
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
