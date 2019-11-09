import yagmail


def send(to_addr="", from_addr="", smtp_server="", smtp_port=587, smtp_user="", smtp_password="", smtp_ssl=False,
         smtp_starttls=True, subject="", contents=None):
    if smtp_user == "":
        smtp_user = from_addr

    if contents is None:
        contents = []

    yag = yagmail.SMTP(
        user=smtp_user,
        password=smtp_password,
        host=smtp_server,
        port=smtp_port,
        smtp_ssl=smtp_ssl,
        smtp_starttls=smtp_starttls
    )
    yag.send(to_addr, subject, contents)
