$(document).ready(function () {

    var FADETIME = 200;
    // keep around some way to tell if an ajax call is in flight
    var searchRequest;
    var $searchInput = $(".search-bar .site-search input");
    var $searchContainer = $(".search-area");
    var $filters = $("[data-filters] input"); //$("#collapse-eventcategories input") #collapse-websitetopics #collapse-audience
    var $placeholder = $(".placeholder-area").length ? $(".placeholder-area").html() : "";

    var $searchPageitem = $("#searchPageitem");
    var $divisionCategoryFilters = $("#collapse-division-or-office-facets label");
    var $topicCategoryFilters = $("#collapse-websitetopics label");
    var $audienceCategoryFilters = $("#collapse-audience label");
    var $eventCategoryFilters = $("#collapse-eventcategories label");
    var $resourceCategoryFilters = $("#collapse-resourcetype label");
    var $serviceCategoryFilters = $("#collapse-servicecategories label");
    var $contentTypeFilters = $("#collapse-Types label");
    
    function updatefilterHandlers()
    {
        var $divisionCategoryFilters = $("#collapse-division-or-office-facets label");
        var $topicCategoryFilters = $("#collapse-websitetopics label");
        var $audienceCategoryFilters = $("#collapse-audience label");
        var $eventCategoryFilters = $("#collapse-eventcategories label");
        var $resourceCategoryFilters = $("#collapse-resourcetype label");
        var $serviceCategoryFilters = $("#collapse-servicecategories label");
        var $contentTypeFilters = $("#collapse-Types label");

        $divisionCategoryFilters.change(debounce(function (e) {
            e.preventDefault();
            // make our request using the updated values
            firefilter(1);
        }, 200));
        $topicCategoryFilters.change(debounce(function (e) {
            e.preventDefault();
            // make our request using the updated values
            firefilter(1);
        }, 200));
        $audienceCategoryFilters.change(debounce(function (e) {
            e.preventDefault();
            // make our request using the updated values
            firefilter(1);
        }, 200));

        if ($eventCategoryFilters) {
            $eventCategoryFilters.change(debounce(function (e) {
                e.preventDefault();
                // make our request using the updated values
                firefilter(1);
            }, 200));
        }

        if ($resourceCategoryFilters) {
            $resourceCategoryFilters.change(debounce(function (e) {
                e.preventDefault();
                // make our request using the updated values
                firefilter(1);
            }, 200));
        }

        if ($serviceCategoryFilters) {
            $serviceCategoryFilters.change(debounce(function (e) {
                e.preventDefault();
                // make our request using the updated values
                firefilter(1);
            }, 200));
        }

        if ($contentTypeFilters) {
            $contentTypeFilters.change(debounce(function (e) {
                e.preventDefault();
                // make our request using the updated values
                firefilter(1);
            }, 200));
        }

        $(".facets__reset-filters").click(function (e) {
            e.preventDefault();

            $('.facets input:checkbox').each(function (i, checkbox) {
                $(checkbox).attr('checked', false);
            });
            $('.facets .collapse').collapse('hide');
            firefilter(1);
        });
        $(".site-search__reset-search").click(function (e) {
            e.preventDefault();

            $searchInput.val('');
            $(this).hide();
            firefilter(1);
        });
        $searchInput.keyup(function () {
            if ($searchInput.val().length > 0) {
                $(".site-search__reset-search").css('display', '');
            } else {
                $(".site-search__reset-search").hide();
            }
        });
    }

    function toggleSearchUI(html) {
        if (!$(html).find('.no-search-list-items p').length) {
            $('#search-results .section-body').show();
            $('#search-results .section-header').removeClass('sr-only');
            $('.no-search-list-items').removeClass('alert alert-info').addClass('sr-only');
            // If facets exist, adjust style so 2 columns are used
            if ($(html).find('.facets ul').length) {
                $('.search-area main').attr('class', 'main-primary');
                $('.main-secondary').show();
            } else {
                $('.search-area main').attr('class', 'main');
                $('.main-secondary').hide();
            }
            if ($(html).find('.search-list-suggestions p').length) {
                $('.search-list-suggestions').removeClass('sr-only').addClass('alert alert-info');
                $('.search-list-suggestions').html($(html).find('.search-list-suggestions').html());
            } else {
                $('.search-list-suggestions').removeClass('alert alert-info').addClass('sr-only');
            }

            $('.main-secondary .facets').html($(html).find('.facets').html());
            $('#search-results .section-header h2').html($(html).find('.section-header h2').html());
            $('#search-results .section-header p').html($(html).find('.section-header p').html());
            $('#search-results .section-body').html($(html).find('.section-body').html());
            // If pagination exists, display it
            if ($(html).find('nav .pagination').length) {
                $('#search-results .search-pagination').show();
                $('#search-results .search-pagination').html($(html).find('nav').html());
            } else {
                $('#search-results .search-pagination').hide();
            }
        } else {
            $('.search-list-suggestions').removeClass('alert alert-info').addClass('sr-only');
            $('#search-results .section-body').hide();
            $('#search-results .section-header').addClass('sr-only');
            // Only hide facets if none are selected
            if ($('.facets input:checked').length == 0) {
                $('.search-area main').attr('class', 'main');
                $('.main-secondary').hide();
            }
            // No results are found, hide pagination, header & add the no results found div to the section body
            $('#search-results .search-pagination').hide();

            if ($(html).find('.no-search-list-items p').length) {
                $('.no-search-list-items').removeClass('sr-only').addClass('alert alert-info');
                $('.no-search-list-items').html($(html).find('.no-search-list-items').html());
                $('.search-area main .section-body').html($(html).find('#search-results').html());
            } else {
                $('.no-search-list-items').removeClass('alert alert-info').addClass('sr-only');
            }
        }
    }

    function GetFiltersState() {
        var filterStr = "";
        $(".facets-group.in").prop("aria-expanded", "true").each(function () {
            filterStr += $(this).siblings("button").attr('id') + '|';
        });
        return filterStr;
    }

    function paginationHandlers() {
        $(".search-area .pagination a").click(function (e) {
            e.preventDefault();
            $('#search-results a:first-of-type').focus();
            var page;
            if ($(this).find(".pagination-label").length) {
                var currPage = parseInt($(".pagination .active a").text());
                switch ($(this).find(".pagination-label").text().trim()) {
                    case "Next":
                        page = currPage + 1;
                        break;
                    case "Previous":
                        page = currPage - 1;
                        break;
                }
            } else {
                page = parseInt($(this).text().trim());
            }
            firefilter(page);
        });
    }

    function sortHandlers() {
        $(".select-wrapper #sort-by-select").change(debounce(function (e) {
            e.preventDefault();
            firefilter(1);
        }));
    }
    sortHandlers();
    paginationHandlers();
    SearchHandlers();
    updatefilterHandlers();

    function ResetContenttypeSort() {
        $(".select-wrapper #show-by-content-type").val("all");
        $(".select-wrapper #sort-by-select").val("relevance");
    }

    function SearchHandlers() {
        $(".search-bar .site-search button").click(function (e) {
            e.preventDefault();
            firefilter(1);
        });
    }


    function shouldFireSearch(searchStr) {
        if (searchStr.length >= 3 || searchStr.length == 0) {
            return true;
        } else {
            $searchContainer.find('.loading-spinner .alert').html('Search requires at least <strong>3</strong> characters in order to return results.');
            $searchContainer.find(".loading-spinner").show();
            $searchContainer.find('.section-header').remove();
            $searchContainer.find('.section-body').remove();
            $searchContainer.find('.loading-spinner + .alert').remove();
            $searchContainer.find('nav').remove();
            return false;
        }
    }

    //$searchInput.keyup(debounce(function (e) {
    //    e.preventDefault();
    //     //make our request using the updated values
    //    firefilter(1);
    //}, 500));

    // Main Helper function to fire off our ajax requests
    function firefilter(page) {
        url = "/api/sitecore/Search/PageFullAjax";

        var $divisionCategoryFilters = $("#collapse-division-or-office-facets label");
        var $topicCategoryFilters = $("#collapse-websitetopics label");
        var $audienceCategoryFilters = $("#collapse-audience label");
        var $eventCategoryFilters = $("#collapse-eventcategories label");
        var $resourceCategoryFilters = $("#collapse-resourcetype label");
        var $serviceCategoryFilters = $("#collapse-servicecategories label");
        var $contentTypeFilters = $("#collapse-Types label");

        // We need to stop the world in terms of our requests and updating
        // any pending ajax's need to be canceld and we need to then stop loading event handlers
        if (searchRequest && searchRequest.state() === 'pending') {
            searchRequest.abort();
        }
        var searchterm = $searchInput.val();
        
        var activeFilters = GetFiltersState();

        var divisionCategoryFilters = "";        

        var topicCategoryFilters = "";
        $topicCategoryFilters.each(function () {
            if ($(this).children().is(':checked')) {
                topicCategoryFilters += $(this).attr('id').trim() + ",";
            }
        });
        topicCategoryFilters = topicCategoryFilters.replace(/,\s*$/, "");

        var audienceCategoryFilters = "";
        $audienceCategoryFilters.each(function () {
            if ($(this).children().is(':checked')) {
                audienceCategoryFilters += $(this).attr('id').trim() + ",";
            }
        });
        audienceCategoryFilters = audienceCategoryFilters.replace(/,\s*$/, "");

        var eventCategoryFilters = "";
        var resourceCategoryFilters = "";
        var serviceCategoryFilters = "";

        if ($eventCategoryFilters) {
            $eventCategoryFilters.each(function () {
                if ($(this).children().is(':checked')) {
                    eventCategoryFilters += $(this).attr('id').trim() + ",";
                }
            });
            eventCategoryFilters = eventCategoryFilters.replace(/,\s*$/, "");
        }

        if ($resourceCategoryFilters) {
            $resourceCategoryFilters.each(function () {
                if ($(this).children().is(':checked')) {
                    resourceCategoryFilters += $(this).attr('id').trim() + ",";
                }
            });
            resourceCategoryFilters = resourceCategoryFilters.replace(/,\s*$/, "");
        }

        if ($serviceCategoryFilters) {
            $serviceCategoryFilters.each(function () {
                if ($(this).children().is(':checked')) {
                    serviceCategoryFilters += $(this).attr('id').trim() + ",";
                }
            });
            serviceCategoryFilters = serviceCategoryFilters.replace(/,\s*$/, "");
        }
        
        var typesCategoryFilters = "";
        if ($contentTypeFilters) {
            $contentTypeFilters.each(function () {
                if ($(this).children().is(':checked')) {
                    typesCategoryFilters += $(this).attr('id').trim() + ",";
                }
            });
            typesCategoryFilters = typesCategoryFilters.replace(/,\s*$/, "");
        }

        var isGlobalSearchPage = $("#isGlobalSearchPage").val();
        if (isGlobalSearchPage == "false"){
            divisionCategoryFilters = $("#divisionId").val();
            } else {
            $divisionCategoryFilters.each(function () {
                if ($(this).children().is(':checked')) {
                    divisionCategoryFilters += $(this).attr('id').trim() + ",";
                }
            });
            divisionCategoryFilters = divisionCategoryFilters.replace(/,\s*$/, "");
        }


        function fire() {
            showLoader($searchContainer);
            $searchContainer.find("[data-ajax-container]");
            var searchscope = $(".searchscope").val();
            var sort = $(".select-wrapper #sort-by-select").val();

            searchRequest = $.ajax({
                url: url,
                data: {
                    search: searchterm,
                    topicCategoryFilters: topicCategoryFilters,
                    audienceCategoryFilters: audienceCategoryFilters,
                    divisionid: divisionCategoryFilters,
                    eventCategoryFilters: eventCategoryFilters,
                    resourceCategoryFilters:resourceCategoryFilters,
                    serviceCategoryFilters: serviceCategoryFilters,
                    sort: sort,
                    page: page,
                    contenttype: typesCategoryFilters,
                    searchscope: searchscope,
                    activeFilters: activeFilters,
                    isGlobalSearchPage: isGlobalSearchPage
                },
                cache: false,
                success: function (html) {

                    if (supports_history_api()) {
                        if (typeof location.origin === 'undefined')
                            location.origin = location.protocol + '//' + location.host;

                        var existingurl = location.href;

                        if (existingurl.indexOf('?') == -1) {
                            existingurl = existingurl + "?";
                        }
                        else {
                            existingurl = existingurl + "&";
                        }

                        existingurl = removeURLParameter(existingurl, "search")
                        existingurl = removeURLParameter(existingurl, "topicCategoryFilters")
                        existingurl = removeURLParameter(existingurl, "divisionid")
                        existingurl = removeURLParameter(existingurl, "audienceCategoryFilters")
                        existingurl = removeURLParameter(existingurl, "contenttype")
                        existingurl = removeURLParameter(existingurl, "sort")
                        existingurl = removeURLParameter(existingurl, "page")
                        existingurl = removeURLParameter(existingurl, "activeFilters")

                        existingurl = removeURLParameter(existingurl, "eventCategoryFilters")
                        existingurl = removeURLParameter(existingurl, "resourceCategoryFilters")
                        existingurl = removeURLParameter(existingurl, "serviceCategoryFilters")

                        var formParams = [
                            { name: "search", value: searchterm },
                            { name: "topicCategoryFilters", value: topicCategoryFilters },
                            { name: "divisionid", value: divisionCategoryFilters },
                            { name: "audienceCategoryFilters", value: audienceCategoryFilters },
                            { name: "contenttype", value: typesCategoryFilters },
                            { name: "sort", value: sort },
                            { name: "eventCategoryFilters", value: eventCategoryFilters },
                            { name: "resourceCategoryFilters", value: resourceCategoryFilters },
                            { name: "serviceCategoryFilters", value: serviceCategoryFilters },
                            { name: "activeFilters", value: activeFilters },
                            { name: "page", value: page }
                        ];
                        var queryStr = $.param(formParams).replace(/%2B/g, '+');

                        var addUrl = existingurl + queryStr;

                        // Redirect to search results page
                        history.pushState(addUrl, null, addUrl);
                    }

                    hideLoader($searchContainer);
                    toggleSearchUI(html);
                    if ($(".placeholder-area").length)
                        $(".placeholder-area").html($placeholder);
                    sortHandlers();
                    paginationHandlers();
                    updatefilterHandlers();
                }
            });
        }

        fire();
    }

    function removeURLParameter(url, parameter) {
        //prefer to use l.search if you have a location/link object
        var urlparts = url.split('?');
        if (urlparts.length >= 2) {

            var prefix = encodeURIComponent(parameter) + '=';
            var pars = urlparts[1].split(/[&;]/g);

            //reverse iteration as may be destructive
            for (var i = pars.length; i-- > 0;) {
                //idiom for string.startsWith
                if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                    pars.splice(i, 1);
                }
            }

            url = urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : "");
            return url;
        } else {
            return url;
        }
    }


    // Returns a function, that, as long as it continues to be invoked, will not
    // be triggered. The function will be called after it stops being called for
    // N milliseconds. If `immediate` is passed, trigger the function on the
    // leading edge, instead of the trailing.
    function debounce(func, wait, immediate) {
        var timeout;
        return function () {
            var context = this, args = arguments;
            var later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };


    function supports_history_api() {
        return !!(window.history && history.pushState);
    }


    function showLoader($el, func) {
        $("#search-results .section-header h2").text('Loading');
        $el.find(".loading-spinner").show();
    }

    function hideLoader($el, func) {
        setTimeout(function () {
            $el.find(".loading-spinner").fadeOut(FADETIME, function () {
                $el.find('.loading-spinner .alert').html('');
            }).promise();
            $el.find('.loading-spinner + .alert').show();
        }, 2000);
    }

    function queryStringToHash(query) {
        var query_string = {};
        var vars = query.split("&");
        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split("=");
            pair[0] = decodeURIComponent(pair[0]);
            pair[1] = decodeURIComponent(pair[1]);
            // If first entry with this name
            if (typeof query_string[pair[0]] === "undefined") {
                query_string[pair[0]] = pair[1];
                // If second entry with this name
            } else if (typeof query_string[pair[0]] === "string") {
                var arr = [query_string[pair[0]], pair[1]];
                query_string[pair[0]] = arr;
                // If third or later entry with this name
            } else {
                query_string[pair[0]].push(pair[1]);
            }
        }
        return query_string;
    };
});


$(document).ready(function () {
    function setCookie(cname, cvalue, exminutes) {
        var d = new Date();
        d.setTime(d.getTime() + (exminutes * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";secure;path=/";
    }

    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
});