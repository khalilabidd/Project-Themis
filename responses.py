def handle_response(message) -> str:
    p_message = message
    if p_message == 'Hey Themis!':
        return "Hey there everyone, I'm Themis and my mission is to ensure justice, divine order, fairness and law."
    if p_message.lower() == 'test':
        return 'Works'
        