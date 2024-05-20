from config import DEFAULT_KEYWORDS


class BackendAgent:
    def __init__(
        self,
        keywords: Optional[List[str]] = DEFAULT_KEYWORDS,
        user_profile: Optional[Dict[str, str]] = None,
    ):
        self.user_profile = {keyword: None for keyword in keywords}
        if user_profile is not None:
            for key, value in user_profile.items():
                if key in keywords and value is not None:
                    self.user_profile[key] = value
            
        self.keywords = keywords
        
    def query_backend(self) -> Dict[str, str]:
        return self.user_profile
    
    def update_user_profile(self, user_profile: Dict[str, str]) -> None:
        for key, value in user_profile.items():
            if key in self.keywords:
                self.user_profile[key] = value
        self.save_user_profile()
        
    def save_user_profile(self) -> None:
        # TODO: Save user profile to database
        pass
        
    def switch_user(self, user: User):
        self.user = user
        print('Switching user to:', user)
        self._switch_history()
        
    def _switch_history(self):
        # TODO: Load user history from database
        pass