"""A small rule-based customer-support chatbot.

Update BUSINESS_HOURS and FAQ_RESPONSES to match your organization before use.
"""

import re
from collections.abc import Callable

BUSINESS_HOURS = "Monday-Friday, 9:00 AM-5:00 PM (local time)"

INTENT_PATTERNS: dict[str, tuple[re.Pattern[str], ...]] = {
    "hours": (
        re.compile(r"\b(?:business|store|office|opening|operating)\s+hours?\b"),
        re.compile(r"\b(?:hours?|opening times?)\b"),
        re.compile(r"\bwhen\s+(?:are you|is (?:the )?(?:store|office))\s+open\b"),
        re.compile(r"\bwhat time (?:do you|does (?:the )?(?:store|office))\s+(?:open|close)\b"),
        re.compile(r"\b(?:are you|is the (?:store|office))\s+open\b"),
    ),
    "shipping": (
        re.compile(r"\b(?:shipping|shipment|delivery|deliver|ship|tracking|track)\b"),
    ),
    "returns": (
        re.compile(r"\b(?:return|refund|exchange|send back)\b"),
    ),
    "warranty": (
        re.compile(r"\b(?:warrant(?:y|ies)|repair|broken|defective)\b"),
    ),
    "product": (
        re.compile(r"\b(?:products?|features?|specifications?|compatible|compatibility)\b"),
    ),
    "payment": (
        re.compile(r"\b(?:payment|pay|credit card|debit card|invoice)\b"),
    ),
}

FAQ_RESPONSES = {
    "shipping": (
        "I can help with shipping and delivery. Delivery options and timing can vary; "
        "please check your order confirmation or share your question with a support "
        "representative."
    ),
    "returns": (
        "Return and refund eligibility depends on the item and purchase. Please check "
        "your order details or contact support for the applicable return instructions."
    ),
    "warranty": (
        "Warranty coverage depends on the product. Please share the product name and "
        "purchase date, or contact support to confirm the applicable coverage."
    ),
    "product": (
        "I can help with product features, specifications, or compatibility. Which "
        "product are you asking about?"
    ),
    "payment": (
        "For payment questions, please check your order confirmation or contact support "
        "so they can review the payment method and transaction."
    ),
}

EXIT_PATTERN = re.compile(r"(?:bye|goodbye|exit|quit)[.! ]*")
GREETING_PATTERN = re.compile(
    r"(?:hi|hello|hey|good morning|good afternoon|good evening)[.! ]*"
)


def normalize_input(message: str) -> str:
    """Lowercase input and collapse repeated whitespace."""
    return " ".join(message.strip().lower().split())


def handle_message(message: str) -> tuple[str, bool]:
    """Return a response and whether the conversation should end."""
    normalized = normalize_input(message)

    if not normalized:
        return "Please enter a question so I can help.", False
    if EXIT_PATTERN.fullmatch(normalized):
        return "Goodbye! Thanks for contacting support.", True

    for intent, patterns in INTENT_PATTERNS.items():
        if any(pattern.search(normalized) for pattern in patterns):
            if intent == "hours":
                return f"Our business hours are {BUSINESS_HOURS}.", False
            return FAQ_RESPONSES[intent], False

    if GREETING_PATTERN.fullmatch(normalized):
        return (
            "Hello! I can help with business hours, shipping, returns, warranties, "
            "products, and payments. What would you like to know?",
            False,
        )

    return (
        "I'm not sure I understood that. You can ask about business hours, shipping, "
        "returns, warranties, products, or payments, or contact a support representative.",
        False,
    )


def run_chat(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Run the interactive greeting, intent-resolution, and exit loop."""
    output_fn(
        "Hello! I can help with business hours, shipping, returns, warranties, "
        "products, and payments. Type 'bye', 'exit', or 'quit' to leave."
    )

    while True:
        try:
            message = input_fn("You: ")
        except EOFError:
            output_fn("\nGoodbye! Thanks for contacting support.")
            return

        response, should_exit = handle_message(message)
        output_fn(f"Support: {response}")
        if should_exit:
            return


if __name__ == "__main__":
    try:
        run_chat()
    except KeyboardInterrupt:
        print("\nGoodbye! Thanks for contacting support.")
