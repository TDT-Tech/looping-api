import os

from django.core.mail import EmailMessage

from emails.templates import invite, magiclink, newsletter, reply

# TODO: Remove once we finalize payloads, keep for testing Sample data payloads
"""data = {
    "PROFILE_PICTURE_HEADER": "https://i.imgur.com/VTyOmUA.jpeg",
    "GROUP_NAME": "TDT",
    "ISSUE_NUMBER": "12",
    "ISSUE_DATE": "FEBRUARY 1, 2024",
    "QUESTIONS": [
        {
            "question": {"question": "do it fart", "author": "Tommy"},
            "answers": [
                {"answer": "so loud", "author": "Tommy"},
                {"answer": "Life sucks", "author": "Tommy 2"},
            ],
        },
        {
            "question": {"question": "Second question", "author": "Looping"},
            "answers": [
                {"answer": "Is this third?", "author": "Tiffany"},
                {"answer": "Is this second?", "author": "David"},
            ],
        },
    ],
    "MADE_BY": ["Tommy", "Tiffany", "David"],
    "NEXT_ISSUE_DATE": "March, 1st 2024",
}

reply_data = {
    "website_url": "http://google.com",
    "logo_url": "https://i.imgur.com/VTyOmUA.jpeg",
    "name": "Tommy Nguyen",
    "issue_number": 4,
    "newsletter_name": "TDT",
    "reply_url": "http://reddit.com",
    "issue_date": "March, 1st 2024",
    "questions": ["How are you?", "Is it true?"],
}

invite_data = {
    "logo_url": "https://i.imgur.com/VTyOmUA.jpeg",
    "admin_name": "Tommy Dude",
    "group_name": "TDT",
    "reply_url": "http://reddit.com",
    "issue_date": "March, 1st, 2024",
} """


def build_invite(data):
    invite_html = invite.INVITE_OUTLINE.format(
        LOGO_URL=data["logo_url"],
        ADMIN_NAME=data["admin_name"],
        GROUP_NAME=data["group_name"],
        REPLY_URL=data["reply_url"],
        ISSUE_DATE=data["issue_date"],
    )

    return invite_html


def build_newsletter_body(data):
    body = ""

    # Newsletter headers
    body += newsletter.GROUP_PICTURE_HEADER.format(
        PROFILE_PICTURE_URL=data["PROFILE_PICTURE_HEADER"]
    )
    body += newsletter.GROUP_NAME_ISSUE_HEADER.format(
        GROUP_NAME=data["GROUP_NAME"],
        ISSUE_NUMBER=data["ISSUE_NUMBER"],
        ISSUE_DATE=data["ISSUE_DATE"],
    )

    # Newsletter question and answers
    body += newsletter.SECTION_HEADER.format(SECTION_NAME="QUESTIONS OF THE WEEK")
    for question in data["QUESTIONS"]:
        body += newsletter.SECTION_SPACE_BETWEEN
        question_section = newsletter.SECTION_QUESTION.format(
            AUTHOR=question["question"]["author"],
            QUESTION=question["question"]["question"],
        )
        answers = ""
        for answer in question["answers"]:
            answers += newsletter.SECTION_ANSWER.format(
                NAME=answer["author"], ANSWER=answer["answer"]
            )
        body += newsletter.SECTION_BODY.format(
            SECTION_QUESTION=question_section, SECTION_ANSWERS=answers
        )
        body += newsletter.SECTION_SPACE_BETWEEN

    # Newsletter ending
    made_by = newsletter.MADE_BY.format(
        MEMBER_NAMES=", ".join(data["MADE_BY"][:-1]) + ", and " + data["MADE_BY"][-1]
    )
    next_issue_date = newsletter.NEXT_ISSUE_DATE.format(
        NEXT_ISSUE_DATE=data["NEXT_ISSUE_DATE"]
    )
    body += newsletter.ENDING.format(MADE_BY=made_by, NEXT_ISSUE_DATE=next_issue_date)

    return body


def build_newsletter(body):
    newsletter_html = newsletter.NEWSLETTER_OUTLINE.format(SECTION_BODY=body)
    return newsletter_html


def build_reply(data):
    logo_section = reply.LOGO_SECTION.format(
        WEBSITE_URL=data["website_url"], LOGO_URL=data["logo_url"]
    )
    reply_intro_section = reply.REPLY_INTRO_SECTION.format(
        NAME=data["name"],
        ISSUE_NUMBER=data["issue_number"],
        NEWSLETTER_NAME=data["newsletter_name"],
    )
    reply_button_section = reply.REPLY_BUTTON_SECTION.format(
        REPLY_URL=data["reply_url"], ISSUE_DATE=data["issue_date"]
    )
    question_items = ""
    for q in data["questions"]:
        question_items += reply.QUESTION_SECTION_ITEM.format(QUESTION=q)
    question_section = reply.QUESTION_SECTION.format(QUESTION_ITEMS=question_items)

    reply_html = reply.REPLY_OUTLINE.format(
        LOGO_SECTION=logo_section,
        REPLY_INTRO_SECTION=reply_intro_section,
        REPLY_BUTTON_SECTION=reply_button_section,
        QUESTION_SECTION=question_section,
    )

    return reply_html


def build_magiclink(logo_url: str, magic_link_url: str) -> str:
    magiclink_html = magiclink.MAGIC_LINK_OUTLINE.format(
        LOGO_URL=logo_url, MAGIC_LINK_URL=magic_link_url
    )
    return magiclink_html


def send_email(subject: str, message: str, receipient_list: list[str]) -> None:
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=os.environ.get("EMAIL_HOST_USER"),
        to=receipient_list,
    )
    email.content_subtype = "html"
    email.send()
