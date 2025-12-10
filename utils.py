from config import DEFAULT_PARAMS

def _prepare_params(params, kwargs):
    if params is None:
        params = DEFAULT_PARAMS.copy()
    params = params.copy()
    params.update(kwargs)
    return params




def _ensure_history(self, opponent_id):
    if opponent_id not in self.my_history:
        self.my_history[opponent_id] = []
        self.opp_history[opponent_id] = []

