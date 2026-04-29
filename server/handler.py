from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

import server.config
from server.utils.helpers import read_json, send_json, hash_password, get_session_user
from server.db import database
from server.services.auth_service import handle_register, handle_login, handle_logout
from server.services.admin_services import handle_delete_user, handle_make_admin, handle_edit_recipe
from server.services.fridge_services import handle_add_fridge, handle_get_fridge
from server.services.profile_services import handle_view_profile, handle_like_profile, handle_follow, handle_unfollow
from server.services.chat_services import handle_chat
from server.services.nutritional_servicies import handle_nutritional_info

class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        return send_json(self, data, status)

    def read_json(self):
        return read_json(self)

    def get_session_user(self):
        return get_session_user(self)

    def do_POST(self):
        print("=== POST HIT ===", self.path)
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path  # "/"
        if path == "/register":
            handle_register(self)
        elif path == "/login":
            handle_login(self)
        elif path == "/logout":
            handle_logout(self)
        elif path.startswith("/admin/"):
            if path == "/admin/delete-user":
                handle_delete_user(self)
            elif path == "/admin/make-admin":
                handle_make_admin(self)
            elif path == "/admin/edit-recipe":
                handle_edit_recipe(self)
        elif path == "/recipes":
            from server.services.recipes_services import handle_create_recipe
            handle_create_recipe(self)
        elif path == "/fridge":
            handle_add_fridge(self)
        elif path == "/view-profile":
            handle_view_profile(self)
        elif path == "/like-profile":
            handle_like_profile(self)
        elif path == "/follow":
            handle_follow(self)
        elif path == "/feed/like":
            from services.feed_services import handle_like_services
            handle_like_services(self)
        elif path == "/feed/comment":
            from services.feed_services import handle_post_comment
            handle_post_comment(self)
        elif path == "/unfollow":
            handle_unfollow(self)
        elif path == "/nutritional-info":
            handle_nutritional_info(self)
        elif  path.startswith ("/chat"):
            handle_chat(self)
        else:
           send_json(self,{"error": "not found"}, 404)

    def do_GET(self):
        print("hi")
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path  # "/"

        print(path)
        # Serve static files
        if path.startswith("/static/") or path in ["/", "/index.html"]:

            if path in ["/", "/index.html"]:
                path = "/static/index.html"

            file_path = "." + path  # now build it here

            if os.path.exists(file_path):
                self.send_response(200)

                if file_path.endswith(".html"):
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                elif file_path.endswith(".js"):
                    self.send_header("Content-Type", "application/javascript")
                elif file_path.endswith(".css"):
                    self.send_header("Content-Type", "text/css")

                self.end_headers()

                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return


        elif path.startswith("/recipes"):
            from server.services.recipes_services import handle_get_recipes
            handle_get_recipes(self)
        elif path.startswith("/chat"):
            handle_chat(self)
        elif path == "/my-recipes":
            from server.services.recipes_services import handle_get_my_recipes
            handle_get_my_recipes(self)
        elif path == "/fridge":
            handle_get_fridge(self)
        elif path.startswith("/user-profile"):
            from server.services.profile_services import handle_get_profile
            handle_get_profile(self)
        elif path.startswith("/is-following"):
            from server.services.profile_services import handle_is_following
            handle_is_following(self)
        elif path.startswith("/feed"):
            from server.services.feed_services import handle_feed_services
            handle_feed_services(self)
        elif path.startswith("/users") or path.startswith("/admin/users"):
            from server.services.profile_services import handle_get_users
            handle_get_users(self)
        elif path.startswith("/ingredients"):
            from server.services.recipes_services import handle_search_ingredient
            handle_search_ingredient(self)
        elif path == "/me":
            from server.services.auth_service import handle_me
            handle_me(self)
        else:
            send_json(self,{"error": "not found"}, 404)