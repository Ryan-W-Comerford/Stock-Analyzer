class ApiInfo:
    api_flag = None
    api_key = None

    @classmethod
    def get_api_info(cls):
        return cls.api_flag, cls.api_key
