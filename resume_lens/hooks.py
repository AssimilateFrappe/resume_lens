app_name = "resume_lens"
app_title = "Resume Lens"
app_publisher = "AT"
app_description = "to filter resume with skills & experiance"
app_email = "write-us@assimilatetechnologies.com"
app_license = "mit"
 
# Apps
# ------------------

# required_apps = [] 

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "resume_lens",
# 		"logo": "/resume-lens/resume-lens.svg",
# 		"title": "Resume Lens",
# 		"route": "/resume-lens"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/resume_lens/css/resume_lens.css"
# app_include_js = "/assets/resume_lens/js/resume_lens.js"

# include js, css files in header of web template
# web_include_css = "/assets/resume_lens/css/resume_lens.css"
# web_include_js = "/assets/resume_lens/js/resume_lens.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "resume_lens/public/scss/website"

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
# app_include_icons = "resume_lens/public/icons.svg"

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
# 	"methods": "resume_lens.utils.jinja_methods",
# 	"filters": "resume_lens.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "resume_lens.install.before_install"

# Uninstallation
# ------------

# before_uninstall = "resume_lens.uninstall.before_uninstall"
# after_uninstall = "resume_lens.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "resume_lens.utils.before_app_install"
# after_app_install = "resume_lens.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "resume_lens.utils.before_app_uninstall"
# after_app_uninstall = "resume_lens.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "resume_lens.notifications.get_notification_config"

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
# 		"resume_lens.tasks.all"
# 	],
# 	"daily": [
# 		"resume_lens.tasks.daily"
# 	],
# 	"hourly": [
# 		"resume_lens.tasks.hourly"
# 	],
# 	"weekly": [
# 		"resume_lens.tasks.weekly"
# 	],
# 	"monthly": [
# 		"resume_lens.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "resume_lens.install.before_tests"

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "resume_lens.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["resume_lens.utils.before_request"]
# after_request = ["resume_lens.utils.after_request"]

# Job Events
# ----------
# before_job = ["resume_lens.utils.before_job"]
# after_job = ["resume_lens.utils.after_job"]

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
# 	"resume_lens.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"process_resumes": "resume_lens.api.process_resumes",
    "get_jd": "resume_lens.api.get_all_records",
    "get_applicants": "resume_lens.api.get_job_applicants",
    "shortlisted_candidates": "resume_lens.api.save_shortlisted_candidates"
}

fixtures = [
    {"dt": "Workspace", "filters": [["Module", "=", "Resume Lens"]]},
]

website_route_rules = [{'from_route': '/resume-lens/<path:app_path>', 'to_route': 'resume-lens'}, {'from_route': '/resume-lens/<path:app_path>', 'to_route': 'resume-lens'},]