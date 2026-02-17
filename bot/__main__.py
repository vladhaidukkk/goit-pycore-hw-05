import sys
from functools import wraps
from typing import Callable

from bot.commands import (
    CommandArgs,
    CommandContext,
    CommandNotFoundError,
    CommandsRegistry,
)


def input_error(*, error_msg: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, IndexError, KeyError):
                print(error_msg)

        return wrapper

    return decorator


commands = CommandsRegistry()


@commands.register("hello")
def say_hello() -> None:
    print("How can I help you?")


@commands.register("add")
@input_error(error_msg="Give me name and phone number please.")
def add_contact(args: CommandArgs, context: CommandContext) -> None:
    name, phone = args
    contacts = context["contacts"]

    if name not in contacts:
        contacts[name] = phone
        print("Contact added.")
    else:
        print("Contact already exists.")


@commands.register("change")
@input_error(error_msg="Give me name and new phone number please.")
def change_contact(args: CommandArgs, context: CommandContext) -> None:
    name, new_phone = args
    contacts = context["contacts"]

    if name in contacts:
        contacts[name] = new_phone
        print("Contact updated.")
    else:
        print("Contact doesn't exist.")


@commands.register("phone")
@input_error(error_msg="Give me name please.")
def show_phone(args: CommandArgs, context: CommandContext) -> None:
    name = args[0]
    contacts = context["contacts"]

    if name in contacts:
        phone = contacts[name]
        print(phone)
    else:
        print("Contact doesn't exist.")


@commands.register("all")
def show_all(context: CommandContext) -> None:
    contacts = context["contacts"]
    if contacts:
        print("\n".join(f"{name}: {phone}" for name, phone in contacts.items()))
    else:
        print("No contacts.")


@commands.register("exit", "close", "quit", "bye")
def say_goodbye() -> None:
    print("Good bye!")
    sys.exit(0)


def parse_input(user_input: str) -> tuple[str, ...]:
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, *args


def main() -> None:
    contacts: dict[str, str] = {}

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        try:
            commands.run(command, *args, contacts=contacts)
        except CommandNotFoundError:
            print("Invalid command.")
        except Exception as e:
            print(f"Whoops, an unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
