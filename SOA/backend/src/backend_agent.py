from typing import Dict, List, Optional

from django.contrib.auth.models import User

# import models
from backend.models import UserProfile
from backend.src.config import DEFAULT_KEYWORDS, OPTIONAL_KEYWORDS


class BackendAgent:
    def __init__(
        self,
        keywords: Optional[List[str]] = DEFAULT_KEYWORDS,
        optional_keywords=OPTIONAL_KEYWORDS,
        user_profile: Optional[Dict[str, str]] = None,
    ):
        '''
        user_profile save both mandatory and optional keywords
        only mandatory keywords are required to be in user_profile
        '''
        self.user = None
        self.user_profile = {}
        for key in keywords:
            self.user_profile[key] = None
        for key in optional_keywords:
            self.user_profile[key] = None
        if user_profile is not None:
            for key, value in user_profile.items():
                if ((key in keywords) or (key in optional_keywords)) and value is not None:
                    self.user_profile[key] = value
        self.keywords = keywords
        self.optional_keywords = optional_keywords

    def query_backend(self) -> Dict[str, str]:
        print("^" * 10)
        print("[QUERY BACKEND]", self.user_profile)
        return self.user_profile

    def update_user_profile(self, user_profile: Dict[str, str]) -> None:
        for key, value in user_profile.items():
            if (key in self.keywords) or (key in self.optional_keywords):
                self.user_profile[key] = value
        self.save_user_profile()

    def save_user_profile(self) -> None:
        userProfile, created = UserProfile.objects.update_or_create(
            username=self.user.username,
            defaults={
                "location": self.user_profile["location"],
                "job_title": self.user_profile["job title"],
                "level": self.user_profile["level"],
                "corporate": self.user_profile["company name"],
                "requirements": self.user_profile["requirements"]
            }
        )

    def switch_user(self, user: User):
        self.user = user
        print('Switching user to:', user)
        self._switch_history()

    def _switch_history(self):
        # get user profile from database
        username = self.user.username
        # try to get user profile from database
        try:
            userProfile = UserProfile.objects.get(username=username)
            # update user profile
            if userProfile.location:
                self.user_profile["location"] = userProfile.location
            if userProfile.job_title:
                self.user_profile["job title"] = userProfile.job_title
            if userProfile.level:
                self.user_profile["level"] = userProfile.level
            if userProfile.corporate:
                self.user_profile["company name"] = userProfile.corporate
            if userProfile.requirements:
                self.user_profile["requirements"] = userProfile.requirements
        except UserProfile.DoesNotExist:
            # if user profile does not exist, create one
            pass
