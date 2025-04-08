import asyncio
from typing import List, Optional
from uuid import UUID
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository
from pizza_hub_app.models import BlackListToken, User
from datetime import datetime
from django.utils import timezone


class BlackListTokenRepository(GenericRepository[BlackListToken]):

    async def get_user_by_token(self, token : str) -> Optional[User]:
        blackListedToken : BlackListToken = await BlackListToken.objects.aget(token=token)
        if (timezone.now() < blackListedToken.expires_at) and blackListedToken.is_valid == True:
            user = await asyncio.get_running_loop().run_in_executor(None, lambda: blackListedToken.user)
            return user
        else:
            blackListedToken.is_valid = False
            await blackListedToken.asave()
            return None
        

    async def revoke_all_black_listed_token_by_user_id(self, user_id : UUID) -> bool:
        user : User = await User.objects.aget(pk=user_id)
        print('ciao')
        blackListedTokens =  [i async for i in BlackListToken.objects.filter(user=user)]
        if len(blackListedTokens) == 0:
            return True
        update_black_list_tokens : list = []
        for i in blackListedTokens:
            i.is_valid = False
            update_black_list_tokens.append(i)
        #print(update_black_list_tokens)
        await BlackListToken.objects.abulk_update(update_black_list_tokens, ['is_valid'])
        return True
        #return True
        