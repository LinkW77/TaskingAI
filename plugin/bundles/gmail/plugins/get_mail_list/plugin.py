import imaplib
import json
from typing import Dict
import email
from email.header import decode_header
from datetime import datetime
from bundle_dependency import *


class GetMailList(PluginHandler):
    def validate_date_format(self, date_str):
        try:
            valid_date = datetime.strptime(date_str, "%Y-%m-%d")
            return valid_date
        except:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                message=f"Invalid date format: {date_str}. The date must be in the format 'YYYY-MM-DD'.",
            )

    async def execute(
        self, credentials: BundleCredentials, execution_config: Dict, plugin_input: PluginInput
    ) -> PluginOutput:
        email_username: str = execution_config.get("email_username")
        email_password: str = execution_config.get("email_password")

        folder: str = plugin_input.input_params.get("folder")
        after: str = plugin_input.input_params.get("after", None)
        before: str = plugin_input.input_params.get("before", None)
        from_who: str = plugin_input.input_params.get("from_who", None)
        keywords: str = plugin_input.input_params.get("keywords", None)
        count: int = plugin_input.input_params.get("count", 10)

        try:
            with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
                mail.login(email_username, email_password)
                if folder.upper() not in ["INBOX", "SENT", "DRAFTS"]:
                    raise_http_error(
                        ErrorCode.REQUEST_VALIDATION_ERROR,
                        message=f"Invalid folder: {folder}. The folder must be 'INBOX', 'Sent', or 'Drafts'.",
                    )
                mail.select(folder)

                criteria = []

                if after:
                    after = self.validate_date_format(after)
                    criteria.append(f'SINCE "{after.strftime("%d-%b-%Y")}"')
                if before:
                    before = self.validate_date_format(before)
                    criteria.append(f'BEFORE "{before.strftime("%d-%b-%Y")}"')
                if from_who:
                    criteria.append(f'FROM "{from_who}"')
                if not criteria:
                    criteria = ["ALL"]
                search_query = " ".join(criteria)

                result, data = mail.search(None, search_query)

                email_list = []
                if result == "OK":
                    email_ids = data[0].split()[-count:]

                    for email_id in email_ids:
                        result, msg_data = mail.fetch(email_id, "(RFC822)")

                        if result == "OK":
                            raw_email = msg_data[0][1]
                            msg = email.message_from_bytes(raw_email)

                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")

                            from_ = msg.get("From")

                            if (
                                keywords
                                and keywords.lower() not in subject.lower()
                                and not any(
                                    keywords.lower() in part.get_payload(decode=True).decode()
                                    for part in msg.walk()
                                    if part.get_content_type() == "text/plain"
                                )
                            ):
                                continue
                            email_list.append({"subject": subject, "from": from_, "id": email_id.decode()})
            return PluginOutput(data={"result": json.dumps(email_list)})
        except Exception as e:
            return PluginOutput(data={"result": f"Error retrieving email list: {e}"})
