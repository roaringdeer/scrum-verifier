import pytest, random
from typing import List, Callable
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database
from app.models.teams import TeamCreate, TeamInDB
from app.models.users import UserInDB
from app.models.members import MemberCreate, MemberUpdate, MemberInDB, MemberPublic
from app.db.repositories.members import MembersRepository

pytestmark = pytest.mark.asyncio

class TestMembersRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient):
        result = await client.post(app.url_path_for('members:create-member', team_id=1))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.get(app.url_path_for('members:list-members-for-team', team_id=1))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.get(app.url_path_for('members:get-member-for-user', team_id=1, username='bradpitt'))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.put(app.url_path_for('members:set-user-role', team_id=1, username='bradpitt'), json={})
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.delete(app.url_path_for('members:remove-member-from-team', team_id=1, username='not_existing_username'))
        assert result.status_code != status.HTTP_404_NOT_FOUND

class TestCreateMembers:
    async def test_user_can_successfully_create_member_for_other_users_team_job(
        self, app: FastAPI, create_authorized_client: Callable, test_team: TeamInDB, test_user3: UserInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user3)
        result = await authorized_client.post(app.url_path_for('members:create-member', team_id=test_team.id))
        assert result.status_code == status.HTTP_201_CREATED
        member = MemberPublic(**result.json())
        assert member.user_id == test_user3.id
        assert member.team_id == test_team.id
        assert member.role == 'dev'

    async def test_user_cant_create_duplicate_users_to_teams(
        self, app: FastAPI, create_authorized_client: Callable, test_team: TeamInDB, test_user4: UserInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user4)
        result = await authorized_client.post(app.url_path_for('members:create-member', team_id=test_team.id))
        assert result.status_code == status.HTTP_201_CREATED
        result = await authorized_client.post(app.url_path_for('members:create-member', team_id=test_team.id))
        assert result.status_code == status.HTTP_400_BAD_REQUEST

    async def test_user_unable_to_create_member_for_their_own_team_job(
        self, app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB, test_team: TeamInDB,
    ) -> None:
        result = await authorized_client.post(app.url_path_for('members:create-member', team_id=test_team.id))
        assert result.status_code == status.HTTP_400_BAD_REQUEST

    async def test_unauthenticated_users_cant_create_members(
        self, app: FastAPI, client: AsyncClient, test_team: TeamInDB,
    ) -> None:
        result = await client.post(app.url_path_for('members:create-member', team_id=test_team.id))
        assert result.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        'id, status_code',
        (
            (500, 404),
            (-1, 422),
            (None, 422)
        )
    )
    async def test_wrong_id_gives_proper_error_status(
        self, app: FastAPI, create_authorized_client: Callable, test_user5: UserInDB, id: int, status_code: int,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user5)
        result = await authorized_client.post(app.url_path_for('members:create-member', team_id=id))
        assert result.status_code == status_code

class TestGetMembers:
    async def test_team_owner_can_get_member_from_user(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user2)
        selected_user = random.choice(test_user_list)
        res = await authorized_client.get(
            app.url_path_for(
                'members:get-member-for-user', 
                team_id=test_team_with_members.id, 
                username=selected_user.username,
            )
        )
        assert res.status_code == status.HTTP_200_OK
        member = MemberPublic(**res.json())
        assert member.user_id == selected_user.id

    async def test_member_owner_can_get_own_member(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB,
    ) -> None:
        first_test_user = test_user_list[0]
        authorized_client = create_authorized_client(user=first_test_user)        
        res = await authorized_client.get(
            app.url_path_for(
                'members:get-member-for-user',
                team_id=test_team_with_members.id,
                username=first_test_user.username,
            )
        )
        assert res.status_code == status.HTTP_200_OK
        member = MemberPublic(**res.json())
        assert member.user_id == first_test_user.id
    
    async def test_other_authenticated_users_cant_view_member_from_user(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB,
    ) -> None:
        first_test_user = test_user_list[0]
        second_test_user = test_user_list[1]
        authorized_client = create_authorized_client(user=first_test_user)
        res = await authorized_client.get(
            app.url_path_for(
                'members:get-member-for-user',
                team_id=test_team_with_members.id,
                username=second_test_user.username,
            )
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    async def test_team_owner_can_get_all_members_for_teams(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user2)
        res = await authorized_client.get(
            app.url_path_for('members:list-members-for-team', team_id=test_team_with_members.id)
        )
        assert res.status_code == status.HTTP_200_OK
        for member in res.json():
            assert member['user_id'] in [user.id for user in test_user_list]

    async def test_non_owners_forbidden_from_fetching_all_members_for_team(
        self, app: FastAPI, authorized_client: AsyncClient, test_team_with_members: TeamInDB,
    ) -> None:
        res = await authorized_client.get(
            app.url_path_for('members:list-members-for-team', team_id=test_team_with_members.id)
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

class TestSetMembersRole:
    async def test_team_owner_can_change_member_role(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB
    ) -> None:
        selected_user = random.choice(test_user_list)
        authorized_client = create_authorized_client(user=test_user2)
        res = await authorized_client.put(
            app.url_path_for(
                'members:set-user-role',
                team_id=test_team_with_members.id,
                username=selected_user.username,
            ),
            json={
                'member_update': {'role': 'sm'}
            }
        )
        assert res.status_code == status.HTTP_200_OK
        member = MemberPublic(**res.json())
        assert member.role == 'sm'
        assert member.user == selected_user.id
        assert member.team == test_team_with_members.id

    async def test_non_owner_forbidden_from_changeing_member_role(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB,
    ) -> None:
        selected_user = random.choice(test_user_list)
        res = await authorized_client.put(
            app.url_path_for(
                'members:set-user-role',
                team_id=test_team_with_members.id,
                username=selected_user.username,
            ),
            json={
                'member_update': {'role': 'sm'}
            }
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    async def test_team_owner_cant_set_multiple_scrum_masters(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB,
    ) -> None:
        selected_users = random.sample(test_user_list, k=2)
        authorized_client = create_authorized_client(user=test_user2)
        res = await authorized_client.put(
            app.url_path_for(
                'members:set-user-role',
                team_id=test_team_with_members.id,
                username=selected_users[0].username,
            ),
            json={
                'member_update': {'role': 'sm'}
            }
        )
        assert res.status_code == status.HTTP_200_OK
        res = await authorized_client.put(
            app.url_path_for(
                'members:set-user-role',
                team_id=test_team_with_members.id,
                username=selected_users[1].username,
            ),
            json={
                'member_update': {'role': 'sm'}
            }
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    async def test_team_owner_cant_set_multiple_product_owners(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB,
    ) -> None:
        selected_users = random.sample(test_user_list, k=2)
        authorized_client = create_authorized_client(user=test_user2)
        res = await authorized_client.put(
            app.url_path_for(
                'members:set-user-role',
                team_id=test_team_with_members.id,
                username=selected_users[0].username,
            ),
            json={
                'member_update': {'role': 'po'}
            }
        )
        assert res.status_code == status.HTTP_200_OK
        res = await authorized_client.put(
            app.url_path_for(
                'members:set-user-role',
                team_id=test_team_with_members.id,
                username=selected_users[1].username,
            ),
            json={
                'member_update': {'role': 'po'}
            }
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST

class TestRemoveMember:
    async def test_team_owner_can_successfully_remove_member(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user2: UserInDB,
        test_user_list: List[UserInDB],
        test_team_with_members: TeamInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user2)
        selected_user = random.choice(test_user_list)
        res = await authorized_client.delete(
            app.url_path_for(
                "members:remove-member-from-team",
                team_id=test_team_with_members.id,
                username=selected_user.username    
            )
        )
        assert res.status_code == status.HTTP_200_OK
        members_repo = MembersRepository(app.state._db)
        members = await members_repo.list_members_for_team(team=test_team_with_members)
        user_ids = [user.id for user in test_user_list]
        for member in members:
            assert member.user_id in user_ids
            assert member.user_id != test_user2.id
        
    async def test_team_member_can_remove_themselves(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user3: UserInDB,
        test_team_with_members: TeamInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user3)
        res = await authorized_client.delete(
            app.url_path_for(
                "members:remove-member-from-team",
                team_id=test_team_with_members.id,
                username=test_user3.username 
            )
        )
        assert res.status_code == status.HTTP_200_OK

    async def test_team_members_cannot_remove_other_members(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        test_user3: UserInDB,
        test_user4: UserInDB,
        test_team_with_members: TeamInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user3)
        res = await authorized_client.delete(
            app.url_path_for(
                "members:remove-member-from-team",
                team_id=test_team_with_members.id,
                username=test_user4.username    
            )
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN
