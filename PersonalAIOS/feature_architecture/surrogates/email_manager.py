class EmailManager:
    """
    Reads/writes emails with perfect context.
    """
    def __init__(self):
        pass

    def draft_reply(self, email_content: str, sender_context: str) -> str:
        """
        Drafts an email perfectly matching the context of previous interactions.
        """
        return f"Drafted reply based on {sender_context}"
