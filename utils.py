from config import DEFAULT_PARAMS

def _prepare_params(params, kwargs):
    if params is None:
        params = DEFAULT_PARAMS.copy()
    params = params.copy()
    params.update(kwargs)
    return params






