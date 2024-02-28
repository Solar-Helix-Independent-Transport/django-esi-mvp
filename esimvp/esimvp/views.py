from django.shortcuts import redirect, render
from esi.decorators import token_required
from esi.models import Token
from django.contrib.auth.decorators import login_required

from .providers import esi

@login_required
@token_required(['esi-search.search_structures.v1'])
def redirect_get_new_token(request, token):
    return redirect("esimvp:index")


@login_required
def get_index(request):
    status = "ESI ERROR"
    try:
        status = esi.get_status()
    except Exception as e:
        pass

    search = {"ERROR": "No Tokens"}
    try:
        valid_token = Token.objects.filter(
            user=request.user
        ).require_valid()
        if valid_token.exists():
            search = esi.client.Search.get_characters_character_id_search(
                character_id=valid_token.first().character_id,
                categories=[
                    "character"
                ],
                search="AuthBot",
                token=valid_token.first().valid_access_token()
            ).results()
    except Exception as e:
        search["ERROR"] = e.__str__()
        print(e)
    return render(
        request,
        template_name="index.html",
        context={
            "status": status,
            "total_tokens": Token.objects.all().count(),
            "search": search
        }
    )
