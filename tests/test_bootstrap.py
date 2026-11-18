"""Check fresh-install credentials without needing a database server."""

import re
import runpy
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
encrypt_md5 = runpy.run_path(str(ROOT / "python/app/utils.py"))["encrypt_md5"]
SCHEMA_DDL = runpy.run_path(str(ROOT / "python/app/db_schema.py"))["SCHEMA_DDL"]


class BootstrapTests(unittest.TestCase):
    def test_sqlite_admin_login_and_preserve_changed_password(self):
        with sqlite3.connect(":memory:") as conn:
            for statement in SCHEMA_DDL:
                conn.execute(statement)
            password, state = conn.execute(
                "select password, state from users where username='admin'"
            ).fetchone()
            self.assertEqual(password, encrypt_md5("admin"))
            self.assertEqual(state, 4)

            conn.execute("update users set password=? where username='admin'", ("changed",))
            for statement in SCHEMA_DDL:
                conn.execute(statement)
            self.assertEqual(
                conn.execute("select password from users where username='admin'").fetchall(),
                [("changed",)],
            )

    def test_mysql_admin_password_matches_login_hash(self):
        sql = (ROOT / "database/install.sql").read_text(encoding="utf-8")
        match = re.search(r"INSERT INTO `users` VALUES \(1,'admin','([^']+)'", sql)
        self.assertIsNotNone(match)
        self.assertEqual(match[1], encrypt_md5("admin"))


if __name__ == "__main__":
    unittest.main()
