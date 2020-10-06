function getCurrentTab() {
    var activeTab = document.getElementById("tabbar").getElementsByClassName("active")[0];
    console.log(activeTab.id);
    return activeTab.id;
}

function getCurrentView() {
    var activeView = document.getElementById("viewbar").getElementsByClassName("active")[0];
    console.log(activeView.id);
    return activeView.id;
}

function switchTab(year) {
    var activeTab = document.getElementById("tabbar").getElementsByClassName("active")[0];
    activeTab.classList.remove("active");
    var newTab = document.getElementById("t" + year);
    newTab.classList.add("active");
    console.log(year);
    getPlotSrc();
}

function switchView(view) {
    var activeView = document.getElementById("viewbar").getElementsByClassName("active")[0];
    activeView.classList.remove("active");
    var newView = document.getElementById("v" + view);
    newView.classList.add("active");
    console.log(view);
    getPlotSrc();
}

function getPlotSrc() {
    var plot = document.getElementById("plot");
    const year = getCurrentTab().substring(1).toLowerCase();
    const view = getCurrentView().substring(1).toLowerCase();
    plot.src = `../plots/${year}-${view}.html`;
}
