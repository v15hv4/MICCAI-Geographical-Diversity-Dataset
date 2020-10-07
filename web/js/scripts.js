function getCurrentTab() {
    var activeTab = document.getElementById("tabbar").getElementsByClassName("active")[0];
    return activeTab.id;
}

function getCurrentView() {
    var activeView = document.getElementById("viewbar").getElementsByClassName("active")[0];
    return activeView.id;
}

function switchTab(year) {
    var activeTab = document.getElementById("tabbar").getElementsByClassName("active")[0];
    activeTab.classList.remove("active");
    var newTab = document.getElementById("t" + year);
    newTab.classList.add("active");
    getPlotSrc();
}

function switchView(view) {
    var activeView = document.getElementById("viewbar").getElementsByClassName("active")[0];
    activeView.classList.remove("active");
    var newView = document.getElementById("v" + view);
    newView.classList.add("active");
    getPlotSrc();
}

function getPlotSrc() {
    const available = [
        "../plots/2011-bar.html",
        "../plots/2012-bar.html",
        "../plots/2013-bar.html",
        "../plots/2014-bar.html",
        "../plots/2016-bar.html",
        "../plots/2016-map.html",
        "../plots/2017-bar.html",
        "../plots/2017-map.html",
        "../plots/2018-bar.html",
        "../plots/2018-map.html",
        "../plots/2019-bar.html",
        "../plots/2019-map.html",
        "../plots/2020-bar.html",
        "../plots/2020-map.html",
    ];
    var plot = document.getElementById("plot");
    const year = getCurrentTab().substring(1).toLowerCase();
    const view = getCurrentView().substring(1).toLowerCase();
    const filesrc = `../plots/${year}-${view}.html`;
    if (available.includes(filesrc)) plot.src = filesrc;
    else plot.src = `./no-data.html`;
}
