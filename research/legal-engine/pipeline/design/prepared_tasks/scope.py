"""Containment of legal units already identified by the research agent."""

def contains(scope_path, use_path):
    """Paths run from jurisdiction/instrument to the specific unit.

    Only use after the agent establishes express scope without unresolved
    qualifications. This function interprets no legal text.
    """
    for path in (scope_path, use_path):
        if not isinstance(path, (list, tuple)) or len(path) < 2:
            raise ValueError('Jurisdiction and instrument are required')
        if any(not isinstance(unit, str) or not unit.strip() for unit in path):
            raise ValueError('Unknown legal unit')
    return tuple(use_path[:len(scope_path)]) == tuple(scope_path)
