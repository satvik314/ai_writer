# Function to calculate API price
def calculate_api_price(message):
    input_price_per_million = 15
    output_price_per_million = 75

    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens

    input_price = input_tokens / 1_000_000 * input_price_per_million
    output_price = output_tokens / 1_000_000 * output_price_per_million
    total_price = input_price + output_price
    total_tokens = input_tokens + output_tokens

    return total_price, input_tokens, input_price, output_tokens, output_price, total_tokens
