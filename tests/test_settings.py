from sqlalchemy.engine import make_url

from app.settings import Settings


def test_mysql_credentials_with_url_characters():
    config = Settings(
        _env_file=None,
        DB_TYPE="mysql",
        DB_USER="club@host",
        DB_PASSWORD="space + @:/?#$%",
    )
    url = make_url(config.sqlalchemy_url)
    assert url.username == "club@host"
    assert url.password == "space + @:/?#$%"
