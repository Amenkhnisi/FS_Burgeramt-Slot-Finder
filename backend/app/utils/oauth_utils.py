import requests
from fastapi import HTTPException


def get_user_from_oauth(provider: str, code: str, client_id: str, client_secret: str, redirect_uri: str):
    """
    Exchange OAuth2 authorization code for tokens and fetch user info
    for Google or GitHub.

    Args:
        provider (str): "google" or "github"
        code (str): authorization code from OAuth callback
        client_id (str): OAuth client ID
        client_secret (str): OAuth client secret
        redirect_uri (str): must match what you set in Google/GitHub console

    Returns:
        dict: user info { "email": ..., "username": ..., ... }
    """
    if provider == "google":
        # 1. Exchange code for access token
        token_res = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_res.raise_for_status()
        tokens = token_res.json()

        # 2. Fetch user info
        userinfo_res = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        userinfo_res.raise_for_status()
        userinfo = userinfo_res.json()

        return {
            "email": userinfo.get("email"),
            "username": userinfo.get("name") or userinfo.get("email").split("@")[0],
            "provider_id": userinfo.get("id"),
        }

    elif provider == "github":
        # 1. Exchange code for access token
        token_res = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers={"Accept": "application/json"},
        )
        token_res.raise_for_status()
        tokens = token_res.json()

        # 2. Fetch user info
        userinfo_res = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        userinfo_res.raise_for_status()
        userinfo = userinfo_res.json()

        # Get email (sometimes requires another call)
        email = userinfo.get("email")
        if not email:
            emails_res = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {tokens['access_token']}"},
            )
            emails_res.raise_for_status()
            emails = emails_res.json()
            primary_email = next((e["email"]
                                 for e in emails if e.get("primary")), None)
            email = primary_email or emails[0]["email"]

        return {
            "email": email,
            "username": userinfo.get("login"),
            "provider_id": userinfo.get("id"),
        }

    else:
        raise HTTPException(
            status_code=400, detail="Unsupported OAuth provider")
