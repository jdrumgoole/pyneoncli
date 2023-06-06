import random
import string


def generate_random_name(prefix: str = "", length: int = 10) -> str:
    characters = string.ascii_letters + string.digits + '_'
    return f"{prefix}{''.join(random.choice(characters) for _ in range(length))}"


if __name__ == '__main__':
    print(generate_random_name())
