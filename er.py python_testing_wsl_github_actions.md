[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex 437b9a6..cd59a4a 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -1,2 +1,3 @@[m
 __pycache__/**[m
 .pytest_cache/**[m
[32m+[m[32m.venv/**[m
[1mdiff --git a/log_parser.py b/log_parser.py[m
[1mindex f4ed871..97e9f09 100644[m
[1m--- a/log_parser.py[m
[1m+++ b/log_parser.py[m
[36m@@ -11,11 +11,11 @@[m [mdef count_errors(log_file):[m
 [m
 def has_fatal(log_file):[m
     """Checks if the log contain a FATAL error"""[m
[31m-    fatal = True[m
[32m+[m[32m    fatal = False[m[41m[m
     with open(log_file, "r") as file:[m
         for line in file:[m
             if "FATAL" in line:[m
[31m-                fatal = False[m
[32m+[m[32m                fatal = True[m[41m[m
         return fatal[m
 [m
 [m
