#!/usr/bin/env bash
export NODE_INSTALLATION_VERSION=$(sed 's/^v//' "$(dirname "${BASH_SOURCE[0]}")/../.nvmrc")
export REPOSITORY_RID="ri.stemma.main.repository.83345d45-7af3-4fd4-9175-613c5971696a"
export REQUESTS_CA_BUNDLE=${SSL_CERT_FILE} # Used by the Python requests module
