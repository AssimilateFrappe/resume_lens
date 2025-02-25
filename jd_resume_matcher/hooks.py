app_name = "jd_resume_matcher"
app_title = "Jd Resume Matcher"
app_publisher = "Assimilate Technologies"
app_description = "Assimilate top match resume find from uploaded resume & job description "
app_email = "developer@assimilatetechnologies.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "jd_resume_matcher",
# 		"logo": "/assets/jd_resume_matcher/logo.png",
# 		"title": "Jd Resume Matcher",
# 		"route": "/jd_resume_matcher",
# 		"has_permission": "jd_resume_matcher.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/jd_resume_matcher/css/jd_resume_matcher.css"
# app_include_js = "/assets/jd_resume_matcher/js/jd_resume_matcher.js"

# include js, css files in header of web template
# web_include_css = "/assets/jd_resume_matcher/css/jd_resume_matcher.css"
# web_include_js = "/assets/jd_resume_matcher/js/jd_resume_matcher.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "jd_resume_matcher/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "jd_resume_matcher/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "jd_resume_matcher.utils.jinja_methods",
# 	"filters": "jd_resume_matcher.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "jd_resume_matcher.install.before_install"
# after_install = "jd_resume_matcher.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "jd_resume_matcher.uninstall.before_uninstall"
# after_uninstall = "jd_resume_matcher.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "jd_resume_matcher.utils.before_app_install"
# after_app_install = "jd_resume_matcher.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "jd_resume_matcher.utils.before_app_uninstall"
# after_app_uninstall = "jd_resume_matcher.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "jd_resume_matcher.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"jd_resume_matcher.tasks.all"
# 	],
# 	"daily": [
# 		"jd_resume_matcher.tasks.daily"
# 	],
# 	"hourly": [
# 		"jd_resume_matcher.tasks.hourly"
# 	],
# 	"weekly": [
# 		"jd_resume_matcher.tasks.weekly"
# 	],
# 	"monthly": [
# 		"jd_resume_matcher.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "jd_resume_matcher.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"process_resumes": "jd_resume_matcher.api.process_resumes",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "jd_resume_matcher.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["jd_resume_matcher.utils.before_request"]
# after_request = ["jd_resume_matcher.utils.after_request"]

# Job Events
# ----------
# before_job = ["jd_resume_matcher.utils.before_job"]
# after_job = ["jd_resume_matcher.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"jd_resume_matcher.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


website_route_rules = [{'from_route': '/jd-resume-matcher/<path:app_path>', 'to_route': 'jd-resume-matcher'},]