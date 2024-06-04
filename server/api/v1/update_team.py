from server.utils.router import method
from server.api import router_v1

@method("/update_team", router_v1.post, id="update_team_v1")
async def update_team(scoreboardNumber: int = 1, team: int = 1, player: int = 1, session_id: str | None = None):
    return scoreboardNumber