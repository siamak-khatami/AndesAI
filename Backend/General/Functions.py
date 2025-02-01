import random
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv,  find_dotenv, dotenv_values
import datetime

# import General.Emails as email_templates
from sqlalchemy import or_, and_, cast, DATE, null
import numpy as np

load_dotenv()
config = dotenv_values(".env")


def check_email(email: str):
    """
    This function receives a candidate email and checks whether it is an email or not.
    :param email:
    :return: Flag, Email, Error
    """
    try:
        v = validate_email(email)
        # print(v.__dict__)
        return True, v.email, None
    except EmailNotValidError as e:
        return False, None, str(e)


def map_keywords_to_string_values(client, keyword_texts):
    keyword_protos = []
    for keyword in keyword_texts:
        string_val = client.get_type("StringValue")
        string_val.value = keyword
        keyword_protos.append(string_val)
    return keyword_protos


def public_id_encoder(user_id: int):
    """
    This function receives user id and generates a public id for that.
    """
    hx = [*hex(user_id).upper()]  # splits string into chars
    # First + [:3] + Sec + [3:7] + Third + [7:]
    hx = [str(random.randint(0, 9))] + hx[:3] + [str(random.randint(0, 9))] + hx[3:7] + [str(random.randint(0, 9))] + hx[7:]
    hx = "".join(hx)
    return hx


def public_id_decoder(hexa):
    """
    This function receives user public id and decodes its main id.
    """
    hexa = [*hexa]
    hexa = hexa[1:4] + hexa[5:9] + hexa[10:]
    hexa = "".join(hexa)
    return int(hexa, 16)


def registration_email(c_name: str,
                       c_email: str,
                       validation_token):

    # activation_link = EndPoints.ProductionHost if socket.gethostname() == "backend" else EndPoints.LocalHost
    # activation_link = activation_link + EndPoints.UserActivation.format(ActivationEncoded=validation_token)
    #
    # reg_email = email_templates.RegistrationEmail(user=c_name, activation_link=activation_link)
    # send_email(client_name=c_name,
    #            client_email=c_email,
    #            content=reg_email)
    # admin_reg_email = email_templates.RegistrationEmail(user=c_name)
    # send_email(client_name=Consts.Admin,
    #            client_email=Consts.AdminEmail,
    #            content=admin_reg_email)
    return


def user_reactivation_email(c_name: str,
                            c_email: str,
                            validation_token):

    # activation_link = EndPoints.ProductionHost if socket.gethostname() == Consts.ProductionHostName else EndPoints.LocalHost
    # activation_link = activation_link + EndPoints.UserActivation.format(ActivationEncoded=validation_token)
    # react_email = email_templates.UserReactivationEmail(user=c_name, activation_link=activation_link)
    # send_email(client_name=c_name,
    #            client_email=c_email,
    #            content=react_email)
    return


def user_reset_password_email(client_name: str,
                              client_email: str,
                              validation_token):

    # reset_link = EndPoints.ProductionHost if socket.gethostname() == "backend" else EndPoints.LocalHost
    # reset_link = reset_link + EndPoints.ResetPasswordFrontEnd.format(ResetEncoded=validation_token)
    # reset_email = email_templates.ResetPassword(user=c_name,
    #                                             reset_link=reset_link,
    #                                             exp_minutes=Consts.ResetPassTokenTime)
    # send_email(client_name=c_name,
    #            client_email=c_email,
    #            content=reset_email)
    return


def send_email(client_name: str,
               client_email: str,
               content,
               body_text: str = ""):
    """
    This function sends email
    client_name: is the name by client
    API: https://github.com/mailersend/mailersend-python
    """
    html = ""
    with open("GeneralFunctions/HTML/EmailTemplate/index.html") as file:
        html = file.read()

    body_html = html.format(Title=content.title,
                            SubTitle=content.sub_title,
                            Body=content.body,
                            Year=datetime.datetime.now().strftime("%Y"))
    # assigning NewEmail() without params defaults to MAILERSEND_API_KEY env var
    from mailersend import emails as ems
    mailer = ems.NewEmail(config["EmailTokenDomain"])

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": "Example",
        "email": "example@example.com",
    }

    recipients = [
        {
            "name": client_name,
            "email": client_email,
        }
    ]

    reply_to = {
        "name": "Example",
        "email": "example@example.com",
    }

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(content.subject, mail_body)
    mailer.set_html_content(body_html, mail_body)
    # mailer.set_plaintext_content(body_text, mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    mailer.send(mail_body)
