$(document).ready(function () {

    SearchHandlers();

    if ($(".global-header .site-search__reset-search").length) {
        $(".global-header .site-search__reset-search").remove();
    }

    function SearchHandlers() {
        $(".global-header .site-search button").click(function (e) {
            e.preventDefault();

            var searchterm = $(".global-header .site-search input").val();

            var searchresultpage = $("#searchPageItemPath").val();

            var $divisionid = $("#divisionId");
            var divisionid = $divisionid.val();

            if (shouldFireSearch(searchterm)) {
                if (typeof location.origin === 'undefined')
                    location.origin = location.protocol + '//' + location.host;
                var queryStr = "search=" + encodeURIComponent(searchterm) + "&divisionid=" + divisionid;
                queryStr = divisionid.length > 0 ? queryStr + "&activeFilters=division-or-office-facets" : queryStr;
                var addUrl = location.origin + searchresultpage + "?" + queryStr;
               
                // Redirect to search results page
                window.location = addUrl;
            }
        });
    }

    function shouldFireSearch(searchStr) {
        return searchStr && searchStr.length >= 1;
    }

});