const baseUrl = window.location.origin;
const event_id = window.location.pathname.split("/")[2];
let timescale = 1;
let items = {};
let graphData = {};

function init() {
    getItems();
    addTimeHandler();
    drawItemSelection();
}

function addTimeHandler() {
    document.getElementById("1h").addEventListener('click', (e)=>{timescale = 1});
    document.getElementById("2h").addEventListener('click', (e)=>{timescale = 2});
    document.getElementById("4h").addEventListener('click', (e)=>{timescale = 4});
    document.getElementById("8h").addEventListener('click', (e)=>{timescale = 8});
}

function addItemSelectionHandler() {
    document.getElementById("itemSelection").childNodes.forEach(child => {
        child.addEventListener("click", (e)=>{console.log(e.target.id)});
    });
}

function getItems() {
    let xhr = new XMLHttpRequest();
        let fullUrl = baseUrl + "/api/get";

        xhr.open("POST", fullUrl, true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let response = JSON.parse(this.responseText);
                //items = response.items;
                console.log(response);
                items = {};
                for (let i = 0; i < response.items.length; i++) {
                    let item = response.items[i];
                    items[item] = false;
                    console.log(item);
                  }
                  console.log("all items: ", items);
                drawItemSelection();
            }
        };
        
        let data = {event_id: "", timescale: "0", items: []};
        data["event_id"] = event_id;
        xhr.send(JSON.stringify(data));
}

function getData() {
    let xhr = new XMLHttpRequest();
    let fullUrl = baseUrl + "/api/get";

    xhr.open("POST", fullUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(JSON.parse(this.responseText));
        }
    };
    
    let data = {event_id: "", timescale: "", items: {}};
    data["event_id"] = event_id;
    data["timescale"] = timescale;
    const values = Object.values(items);
    values.forEach(item => {
        data.items.item = item;
    });
    xhr.send(JSON.stringify(data));
}

function drawItemSelection() {
    const itemSelectionForm = document.getElementById("itemSelection");
    console.log("items: ", items)

    Object.keys(items).forEach(item => {
        const input = document.createElement("input");
        input.innerHTML = item;
        input.id = item;
        input.type = "checkbox";
        
        const label = document.createElement("label");
        label.innerHTML = item;
        label.htmlFor = item;

        itemSelectionForm.appendChild(input);
        itemSelectionForm.appendChild(label);

        input.addEventListener("change", toggleItem);
        console.log("added checkbox for item: " + item);
        console.log(input);
        console.log(document.getElementById(item));
    });
}

function toggleItem() {
    if (items[this.id]) {
        items[this.id] = false;
    } else {
        items[this.id] = true;
    }
}

function refreshData() {
    getItems();
    drawItemSelection();
    getData();
}

window.addEventListener("DOMContentLoaded", init);