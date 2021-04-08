from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import vk_api


class UsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        vk_token = request.user.social_auth.get(provider="vk-oauth2").extra_data.get(
            "access_token"
        )
        vk_session = vk_api.VkApi(token=vk_token)
        vk = vk_session.get_api()
        current_user = vk.users.get(fields="photo_max_orig")[0]
        return Response(current_user)
