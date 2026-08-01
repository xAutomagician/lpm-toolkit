from dynaconf import Dynaconf, Validator

validators = [
    Validator(
        "API_TOKEN",
        is_type_of=str,
    ),
]

settings = Dynaconf(load_dotenv=True, envvar_prefix="LPM", validators=validators)

API_TOKEN = settings.get("API_TOKEN", default=None)
