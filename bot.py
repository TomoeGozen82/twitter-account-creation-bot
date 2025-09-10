import os
import re
import json
import random
import curl_cffi
import urllib.parse
from time import sleep
from faker import Faker
from castleio import Castle
from datetime import datetime
from urllib.parse import urlparse, parse_qs

project_path = os.path.dirname(os.path.abspath(__file__))
environment = Castle.Config("pk_AvRa79bHyJSYSQHnRpcVtzyxetSvFerx")
castle = Castle.Build(environment)

proxy = ""
cds_solver_api_key = ""

class AccountCreationBot:
    def __init__(self, email, proxy, username=None):
        fake = Faker()
        self.response = None
        self.username = username
        self.full_name = fake.name()
        self.email = email
        self.password = fake.password()
        self.proxy = proxy
        self.bd_year = random.randint(1970, 2000)
        self.bd_month = fake.month()
        self.bd_day = fake.day_of_month()
        self.code = None
        self.ct0 = None
        self.auth_token = None
        self.user_id = None
        self.js_instrumentation = None
        self.flow_token = None
        self.session = curl_cffi.Session(impersonate="chrome136")
        self.session.headers.update({
            "accept-language": "en-US,en;q=0.9",
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'origin': 'https://x.com',
            'referer': 'https://x.com/',
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en'
        })
        self.session.proxies.update({"all": self.proxy})

    def signup(self) -> str | None:
        if not self.get_guest_token():
            return
        if not self.get_js_instrumentation():
            return
        if not self.initialize_signup():
            return
        if not self.submit_profile():
            return
        if not self.verify_email():
            return
        if not self.submit_password():
            return
        if not self.get_user_features():
            return
        if not self.set_avatar():
            return
        if not self.set_username():
            return
        if not self.set_notifications():
            return            
        if not self.set_category():
            return
        if not self.set_user_recommendations():
            return
        self.finish_signup_flow()
        log(f"Account created successfuly:\n\nUsername: {self.username}\nPassword: {self.password}\nUser ID: {self.user_id}\nAuth Token: {self.auth_token}\nCTO: {self.ct0}")
    
    def get_guest_token(self):
        try:
            guest_token = self.session.post("https://api.x.com/1.1/guest/activate.json").json()["guest_token"]
            if guest_token is None:
                log("Failed to find guest_token")
                return False
            self.session.headers.update({"x-guest-token": guest_token})
            log("Successfuly fetched guest_token")
            return True
        except Exception as e:
            log(f"Error getting guest_token: {e}")
            return False
    
    def get_js_instrumentation(self):
        try:
            js_inst = self.session.get('https://x.com/i/js_inst?c_name=ui_metrics').text
            self.js_instrumentation = re.findall(r'return ({.*?});', js_inst, re.DOTALL)[0]
            if self.js_instrumentation is None:
                log("Failed to find js_instrumentation")
                return False
            log("Successfuly fetched js_instrumentation")
            return True
        except Exception as e:
            log(f"Error getting js_instrumentation: {e}")
            return False
    
    def initialize_signup(self):
        try:
            splash_screen_data = {
                'input_flow_data': {
                    'requested_variant': "{\"signup_type\":\"phone_email\"}",
                    'flow_context': {
                        'debug_overrides': {},
                        'start_location': {
                            'location': 'splash_screen'
                        }
                    }
                },
                'subtask_versions': {
                    'action_list': 2,
                    'alert_dialog': 1,
                    'app_download_cta': 1,
                    'check_logged_in_account': 1,
                    'choice_selection': 3,
                    'contacts_live_sync_permission_prompt': 0,
                    'cta': 7,
                    'email_verification': 2,
                    'end_flow': 1,
                    'enter_date': 1,
                    'enter_email': 2,
                    'enter_password': 5,
                    'enter_phone': 2,
                    'enter_recaptcha': 1,
                    'enter_text': 5,
                    'enter_username': 2,
                    'generic_urt': 3,
                    'in_app_notification': 1,
                    'interest_picker': 3,
                    'js_instrumentation': 1,
                    'menu_dialog': 1,
                    'notifications_permission_prompt': 2,
                    'open_account': 2,
                    'open_home_timeline': 1,
                    'open_link': 1,
                    'phone_verification': 4,
                    'privacy_options': 1,
                    'security_key': 3,
                    'select_avatar': 4,
                    'select_banner': 2,
                    'settings_list': 7,
                    'show_code': 1,
                    'sign_up': 2,
                    'sign_up_review': 4,
                    'tweet_selection_urt': 1,
                    'update_users': 1,
                    'upload_media': 1,
                    'user_recommendations_list': 4,
                    'user_recommendations_urt': 1,
                    'wait_spinner': 3,
                    'web_modal': 1
                }
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/task.json?flow_name=signup", json=splash_screen_data).json()
            subtasks = self.response.get('subtasks')
            for subtask in subtasks:
                if subtask["subtask_id"] == "ArkoseEmail":
                    blob = parse_qs(urlparse(subtask["web_modal"]["url"]).query).get('data', [None])[0]
                    self.solve_arkose_email(blob)
            if self.code is None:
                log("Failed to solve arkose funcaptcha")
                return False
            self.flow_token = self.response.get('flow_token')
            return True
        except Exception as e:
            log(f"Error initializing signup: {e}")
            return False
    
    def submit_profile(self):
        try:
            castle_token = castle.create_token()
            email_data = {
                "flow_token": self.flow_token,
                "display_name": self.full_name,
                "email": self.email,
                "castle_token": castle_token[0]
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/begin_verification.json", json=email_data)
            if self.response.status_code != 200:
                log("Failed to submit profile")
                return False
            log("Successfuly submitted profile")
            return True
        except Exception as e:
            log(f"Error submitting profile: {e}")
            return False

    def verify_email(self):
        try:
            email_code = input("Enter email code: ") #TODO:fetch code from an email api source automatically
            signup_data = {
                "flow_token": self.flow_token,
                "subtask_inputs": [
                    {
                        "subtask_id": "Signup",
                        "sign_up": {
                            "js_instrumentation": {
                                "response": self.js_instrumentation
                            },
                            "link": "email_next_link",
                            "name": self.full_name,
                            "email": self.email,
                            "birthday": {
                                "year": self.bd_year,
                                "month": self.bd_month,
                                "day": self.bd_day
                            },
                            "personalization_settings": {
                                "allow_cookie_use": True,
                                "allow_device_personalization": True,
                                "allow_partnerships": True,
                                "allow_ads_personalization": True
                            }
                        }
                    },
                    {
                        "subtask_id": "ArkoseEmail",
                        "web_modal": {
                            "completion_deeplink": "twitter://onboarding/web_modal/next_link?access_token="+self.code,
                            "link": "signup_with_email_next_link"
                        }
                    },
                    {
                        "subtask_id": "EmailVerification",
                        "email_verification": {
                            "code": email_code,
                            "email": self.email,
                            "link": "next_link"
                        }
                    }
                ]
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/task.json", json=signup_data).json()
            if self.response.status_code != 200:
                log("Failed to verify email")
                return False
            self.flow_token = self.response.get('flow_token')
            log("Successfuly verified email")
            return True
        except Exception as e:
            log(f"Error verifying email: {e}")
            return False
    
    def submit_password(self):
        try:
            castle_token = castle.create_token()
            password_data = {
                "flow_token": self.flow_token,
                "subtask_inputs": [
                    {
                        "subtask_id": "EnterPassword",
                        "enter_password": {
                            "password": self.password,
                            "link": "next_link",
                            "castle_token": castle_token[0]
                        }
                    }
                ]
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/task.json", json=password_data).json()
            if self.response.status_code != 200:
                log("Failed to submit password")
                return False
            self.session.headers.update({"x-csrf-token": self.session.cookies["ct0"]})
            self.flow_token = self.response.get('flow_token')
            log("Successfuly submitted password")
            return True
        except Exception as e:
            log(f"Error submitting password: {e}")
            return False
        
    def get_user_features(self):
        try:
            features = {
                "subscriptions_upsells_api_enabled": True,
                "payments_enabled": False,
                "profile_label_improvements_pcf_label_in_post_enabled": True,
                "rweb_tipjar_consumption_enabled": True,
                "verified_phone_label_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True
            }
            variables = {
                "withCommunitiesMemberships": True
            }
            fieldToggles = {
                "isDelegate": False,
                "withAuxiliaryUserLabels": True
            }
            user = self.session.get(f"https://api.x.com/graphql/RTSjxYbzVsRECfMtoB1Cqw/Viewer?variables={urllib.parse.quote(json.dumps(variables))}&features={urllib.parse.quote(json.dumps(features))}&fieldToggles={urllib.parse.quote(json.dumps(fieldToggles))}")
            if user.status_code != 200:
                log("Failed to get user features")
                return False
            self.ct0 = self.session.cookies["ct0"]
            self.session.headers.update({"x-csrf-token": self.ct0})
            log("Successfuly got user features")
            return True
        except Exception as e:
            log(f"Error getting user features: {e}")
            return False

    def set_avatar(self):
        try:
            avatar_data = {
                "flow_token": self.flow_token,
                "subtask_inputs": [{
                    "subtask_id": "SelectAvatar",
                    "select_avatar": {
                        "link": "skip_link"
                    }
                }]
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/task.json", json=avatar_data).json()
            if self.response.status_code != 200:
                log("Failed to set avatar")
                return False
            self.flow_token = self.response.get('flow_token')
            log("Successfuly set avatar")
            return True
        except Exception as e:
            log(f"Error setting avatar: {e}")
            return False

    def set_username(self):
        try:
            if self.username:
                data = {
                    "username": self.username, 
                    "link": "next_link"
                }
            else:
                data = {
                    "link": "skip_link"
                }
            username_data = {
                "flow_token": self.flow_token,
                "subtask_inputs": [
                    {
                        "subtask_id": "UsernameEntryBio",
                        "enter_username": data
                    }
                ]
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/task.json", json=username_data).json()
            if self.response.status_code != 200:
                log("Failed to set username")
                return False
            self.flow_token = self.response.get('flow_token')
            log("Successfuly set username")
            return True
        except Exception as e:
            log(f"Error setting username: {e}")
            return False
    
    def set_notifications(self):
        try:
            notifications_data = {
                "flow_token": self.flow_token,
                "subtask_inputs": [
                    {
                        "subtask_id": "NotificationsPermissionPrompt",
                        "notifications_permission_prompt": {
                            "link": "skip_link"
                        }
                    }
                ]
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/task.json", json=notifications_data).json()
            if self.response.status_code != 200:
                log("Failed to set notifications")
                return False
            self.flow_token = self.response.get('flow_token')
            log("Successfuly set notifications")
            return True
        except Exception as e:
            log(f"Error setting notifications: {e}")
            return False
    
    def set_category(self):
        try:
            category_data = {
                "flow_token": self.flow_token,
                "subtask_inputs": [
                    {
                        "subtask_id": "StandAloneCategoryPickerBlockingNextURT",
                        "generic_urt": {
                            "link": "next_link"
                        }
                    }
                ]
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/task.json", json=category_data).json()
            if self.response.status_code != 200:
                log("Failed to set category")
                return False
            self.flow_token = self.response.get('flow_token')
            log("Successfuly set category")
            return True
        except Exception as e:
            log(f"Error setting category: {e}")
            return False

    def set_user_recommendations(self):
        try:
            user_recommendations_data = {
                "flow_token": self.flow_token,
                "subtask_inputs": [
                    {
                        "subtask_id": "UserRecommendationsURTFollowGating",
                        "user_recommendations_urt": {
                            "link": "next_link",
                            "selected_user_recommendations": [
                                "44196397" #following @elonmusk as first account, you can change it to any account ID you want or add more
                            ]
                        }
                    }
                ]
            }
            self.response = self.session.post("https://api.x.com/1.1/onboarding/task.json", json=user_recommendations_data).json()
            if self.response.status_code != 200:
                log("Failed to set user recommendations")
                return False
            self.flow_token = self.response.get('flow_token')
            self.username = self.response.get('subtasks')[1].get('update_users').get('users')[0].get('screen_name')
            self.user_id = self.response.get('subtasks')[1].get('update_users').get('users')[0].get('id_str')
            log("Successfuly set user recommendations")
            return True
        except Exception as e:
            log(f"Error setting user recommendations: {e}")
            return False

    def finish_signup_flow(self):
        try:
            finish_signup_flow = {
                "flow_token": self.flow_token,
                "subtask_inputs": []
            }
            self.session.post("https://api.x.com/1.1/onboarding/task.json", json=finish_signup_flow)
            self.auth_token = self.session.cookies["auth_token"]
            log("Successfuly finished signup flow")
            return True
        except Exception as e:
            log(f"Error finishing signup flow: {e}")
            return False

    def solve_arkose_email(self, blob):
        log(f"Solving arkose funcaptcha")
        base_url = "https://cds-solver.com"
        payload = {
            "api_key": cds_solver_api_key,
            "site_key": "2CB16598-CB82-4CF7-B332-5990DB66F3AB",
            "browser": "chrome",
            "browser_version": 136,
            "platform": "PC",
            "locale": "en-US",
            "proxy": self.proxy,
            "blob": blob,
            "site_referer": "https://iframe.arkoselabs.com/"
        }
        try:
            response = curl_cffi.post(f'{base_url}/createTask', json=payload).json()
        except Exception as e:
            log(f"Error creating task: {e}")
            return False
        if response.get("task_id") == None:
            log("Failed to create task")
            return False
        task_id = response.get("task_id")
        log(f"Task ID: {task_id}")
        count_retry = 0
        while count_retry <= 120:
            try:
                response = curl_cffi.post(f'{base_url}/getTask', json={"api_key": cds_solver_api_key, "task_id": task_id}).json()
                status = response["status"]
                if status == "processing":
                    count_retry += 1
                    sleep(0.5)
                    continue
                elif status == "success":
                    log(f"Arkose email solved successfuly")
                    self.code = response.get("token")
                    return True
                else:
                    log(status)
                    return False
            except Exception as e:
                log(f"Error getting task: {e}")
                count_retry += 1
                sleep(0.5)
                continue
        return False

def main():
    log(f"Signing up for X account")
    email = input("Enter email: ")
    username = input("Enter username (must be unique, leave empty to use auto generated username): ").strip()
    if username == "":
        username = None
    account_creation_bot = AccountCreationBot(email, proxy, username)
    account_creation_bot.signup()

def log(*msg):
    with open(os.path.join(project_path, "log.txt"), 'a', encoding="utf-8") as log_writer:
        log_writer.write('[{:%d/%m/%Y - %H:%M:%S}]  {}\n'.format(datetime.now(), *msg))
    print('[{:%d/%m/%Y - %H:%M:%S}]  {}'.format(datetime.now(), *msg))

if __name__ == '__main__':
    main()