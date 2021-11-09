var itemList = {
    // (A) INITIALIZE
    items: [], // current list
    hlist: null, // HTML list
    hadd: null, // HTML add item form
    hitem: null, // HTML add item input field
    init: function () {
      // (A1) GET HTML ELEMENTS
      itemList.hlist = document.getElementById("item-list");
      itemList.hadd = document.getElementById("list-add");
      itemList.hitem = document.getElementById("list-item");
      itemList.hadd.addEventListener("submit", itemList.add);

      // (A2) RESTORE PREVIOUS LIST
      /***
      if (localStorage.items == undefined) {
        localStorage.items = "[]";
      }
      itemList.items = JSON.parse(localStorage.items);***/

      // (A3) DRAW HTML LIST
      itemList.draw();
    },

    // (B) ADD NEW ITEM TO THE LIST
    add: function (evt) {
      // (B1) PREVENT FORM SUBMIT
      evt.preventDefault();

      // (B2) ADD NEW ITEM TO LIST
      itemList.items.push({
        name: itemList.hitem.value, // Item name
      });
      itemList.hitem.value = "";
      //itemList.save();

      // (B3) REDRAW HTML LIST
      itemList.draw();
    },

    // (C) DRAW THE HTML LIST
    draw: function () {
      itemList.hlist.innerHTML = "";
      //if (itemList.items.length > 0) {
      if (true) {
        let row, name, delbtn, okbtn;
        for (let i in itemList.items) {
          // (C1) ITEM ROW
          row = document.createElement("div");
          row.className = "item-row";
          itemList.hlist.appendChild(row);

          // (C2) ITEM NAME
          name = document.createElement("div");
          name.className = "item-name";
          name.innerHTML = itemList.items[i].name;
          row.appendChild(name);

          // (C3) DELETE BUTTON
          delbtn = document.createElement("input");
          delbtn.className = "item-del";
          delbtn.type = "button";
          delbtn.value = "Delete";
          delbtn.dataset.id = i;
          delbtn.addEventListener("click", itemList.delete);
          row.appendChild(delbtn);
        }
      }
    },

    // (D) SAVE LIST INTO LOCAL STORAGE
    save: function () {
      if (localStorage.items == undefined) {
        localStorage.items = "[]";
      }
      localStorage.items = JSON.stringify(itemList.items);
    },

    // (E) DELETE SELECTED ITEM
    delete: function () {
      if (confirm("Remove selected item?")) {
        itemList.items.splice(this.dataset.id, 1);
        //itemList.save();
        itemList.draw();
      }
    },
  };

function makeEvent() {
    let xhr = new XMLHttpRequest();
        let fullUrl = window.location.origin + "/api/";

        xhr.open("POST", fullUrl, true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let response = JSON.parse(this.responseText);
                //items = response.items;
                console.log(response);
            }
        };
        
        let data = {eventName: document.getElementById("eventName").value, items: []};
        items.forEach(item => {
            data.append("item", item.name);
        });
        xhr.send(JSON.stringify(data));
        return false;
}

function processForm(e) {
    if (e.preventDefault) e.preventDefault();

    /* do what you want with the form */
    //items = itemList.getItems();
    console.log("processing get data: ", items);
    let data = new FormData();

    for (let i = 0; i < items.length; i++) {
      data.append("item", items[i].name);
      console.log(items[i].name);
    }
    //get name of event from form
    data.append("eventName", document.getElementById("eventName").value);

    console.log(data.get("eventName"));
    // You must return false to prevent the default form behavior
    let xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.origin + "/");
    xhr.onload = function () { alert(this.response); };
    xhr.send(data);
    return false;
  }

  function init() {
      document.getElementById("eventForm").addEventListener("submit", makeEvent);
      itemList.init();
  }
  
  window.addEventListener("DOMContentLoaded", init);