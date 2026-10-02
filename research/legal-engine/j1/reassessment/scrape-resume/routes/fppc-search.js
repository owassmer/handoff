var baseUrl = window.location.origin + window.location.pathname;

function getSelectedFacets() {
    return [...document.querySelectorAll('.facet2dropdown')].reduce((acc, el) => {
        const val = [...el.querySelectorAll('input[type="checkbox"]:checked')]
            .map(input => input.value.trim())
            .join(',');

        if (val) {
            acc[el.dataset.facetName] = val;
        }

        return acc;
    }, {});
}

function getCurrentSort() {
    return new URLSearchParams(window.location.search).get('sortBy') || '';
}

function navigate(options = {}) {
    const prevParams = new URLSearchParams(window.location.search);

    const params = options.clearFilters ? {} : getSelectedFacets();

    const searchTerm = options.searchTerm ?? prevParams.get('searchTerm');
    if (searchTerm) {
        params.searchTerm = searchTerm;
    }

    params.page = options.page || 1;

    // Only carry sortBy forward if it was already in the URL or explicitly set.
    // This lets the server auto-apply the default sort on first filter selection.
    const explicitSort = options.sortBy || getCurrentSort();
    if (explicitSort) {
        params.sortBy = explicitSort;
    }

    window.location.href = baseUrl + '?' + new URLSearchParams(params).toString();
}

function debounce(func, wait) {
    let timeout;
    return function () {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, arguments), wait);
    };
}

function syncCheckboxesToUrl() {
    const params = new URLSearchParams(window.location.search);

    document.querySelectorAll('.facet2dropdown').forEach(el => {
        const facetName = el.dataset.facetName;
        const selectedValues = (params.get(facetName) || '').split(',').map(v => v.trim()).filter(Boolean);

        el.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = selectedValues.includes(checkbox.value.trim());
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // Sync checkbox state with URL (fixes browser back button)
    syncCheckboxesToUrl();

    // Filter changes
    document.querySelectorAll('.filter-option').forEach(el => {
        el.addEventListener('change', debounce(() => navigate(), 200));
    });

    // Pagination
    document.querySelectorAll('.pagination .page-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const parent = link.closest('.page-item');
            if (parent?.classList.contains('disabled') || parent?.classList.contains('active')) return;

            const page = parseInt(link.dataset.page);
            if (!isNaN(page)) {
                navigate({ page });
            }
        });
    });

    // Search
    const searchInput = document.querySelector('#search-input');
    const searchBtn = document.querySelector('#search-btn');

    const submitSearch = (e) => {
        e.preventDefault();
        navigate({ page: 1, searchTerm: searchInput.value });
    };

    searchBtn?.addEventListener('click', submitSearch);
    searchInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') submitSearch(e);
    });

    // Sort
    document.querySelectorAll('.search-bar__sort ul button').forEach(button => {
        button.addEventListener('click', (e) => {
            navigate({ page: 1, sortBy: e.target.value });
        });
    });

    // Clear filters
    document.getElementById('filter-clear-btn')?.addEventListener('click', () => {
        navigate({ clearFilters: true });
    });

    // Clear search
    document.getElementById('clear-search-btn')?.addEventListener('click', () => {
        navigate({ searchTerm: ' ' });
    });
});
