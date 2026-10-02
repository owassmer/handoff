Welcome to Palantir's in-platform custom documentation tool.

Before creating any new docs, please make sure to upgrade your repository to the latest version. You can do this by opening the "..." menu and selecting "Upgrade".

Documentation created in this repository will be published to the in-platform custom documentation when a build runs on the `master` branch.
An ideal workflow is creating a new branch, working on docs and then opening a PR into `master`. When the PR
merges into `master`, that commmit will then trigger a build and publish the documentation.

This documentation repository is the "source of truth" for the custom docs coming out of it.
Whenever it is published, only the files that exist at that moment in time will be persisted to the in-platform custom docs,
and all previous content originating from this documentation repository will be removed.

For example: You create docs about `product-a` and publish them so that they appear in the in-platform custom docs.
Later you delete the `product-a` docs and instead add `product-b` and `product-c` docs. After publishing,
the in-platform custom docs will contain `product-b` and `product-c` docs, but will no longer contain `product-a` docs.
