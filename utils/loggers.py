
def error_logger(func):
    def log_errors(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            issue = f"Could not scrape URL: {args[1]},\nError: {err}\n==================\n"
            with open("logs/scrape_errors.txt", "a") as file:
                file.write(issue)
    return log_errors