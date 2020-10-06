function getCurrentTab() {
    var activeTab = document.getElementById("tabbar").getElementsByClassName("active")[0];
    console.log(activeTab.id);
}

function getCurrentView() {
    var activeView = document.getElementById("viewbar").getElementsByClassName("active")[0];
    console.log(activeView.id);
}

function switchTab(year) {
    var activeTab = document.getElementById("tabbar").getElementsByClassName("active")[0];
    activeTab.classList.remove("active");
    var newTab = document.getElementById("t" + year);
    newTab.classList.add("active");
    console.log(year);
}

function switchView(view) {
    var activeView = document.getElementById("viewbar").getElementsByClassName("active")[0];
    activeView.classList.remove("active");
    var newView = document.getElementById("v" + view);
    newView.classList.add("active");
    console.log(view);
}
