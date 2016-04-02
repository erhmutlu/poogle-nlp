from apps.defaultapp.shapers import filter_by_entity_key, set_params

__author__ = 'erhmutlu'


class Score:

    def get_teams_match_score(self, user_input, intent):
        params = intent.get('params')
        teams = filter_by_entity_key(params, 'ENTITY_KEY_TEAM')
        if len(teams) == 1:
            team = teams[0]
            p = {
                'team': team
            }
            params = set_params(params=p)
            return params

        raise EnvironmentError('1 team is needed but given %s team' % len(teams))

    def get_matches_of_week(self, user_input, intent):
        return set_params({})