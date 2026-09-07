from app.config import Config

class UsageTracker:
    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
        self.thought_tokens = 0
        self.total_tokens = 0

        self.input_cost = 0.0
        self.output_cost = 0.0
        self.total_cost = 0.0

    def add_usage(self, input_tokens, output_tokens, thought_tokens, total_tokens):
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.thought_tokens += thought_tokens
        self.total_tokens += total_tokens

    def calculate_cost(self):
        input_cost = (
            self.input_tokens / 1_000_000
            * Config.INPUT_COST_PER_MILLION
        )

        output_cost =(
            (self.output_tokens + self.thought_tokens) / 1_000_000
            * Config.OUTPUT_COST_PER_MILLION
        )
        self.input_cost = input_cost
        self.output_cost = output_cost
        self.total_cost = input_cost + output_cost 