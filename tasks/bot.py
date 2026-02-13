class BotError(Exception):
    pass


class InvalidArgumentsError(BotError):
    pass


class ContactExistsError(BotError):
    pass


class ContactNotFoundError(BotError):
    pass


def parse_input(user_input: str) -> tuple[str, ...]:
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, *args


def add_contact(args: tuple[str, ...], contacts: dict[str, str]) -> None:
    try:
        name, phone = args
    except:
        raise InvalidArgumentsError("Give me contact name and phone please.")

    if name in contacts:
        raise ContactExistsError

    contacts[name] = phone


def change_contact(args: tuple[str, ...], contacts: dict[str, str]) -> None:
    try:
        name, new_phone = args
    except:
        raise InvalidArgumentsError("Give me contact name and phone please.")

    if name not in contacts:
        raise ContactNotFoundError

    contacts[name] = new_phone


def show_phone(args: tuple[str, ...], contacts: dict[str, str]) -> str:
    try:
        name = args[0]
    except:
        raise InvalidArgumentsError("Give me contact name please.")

    if name not in contacts:
        raise ContactNotFoundError

    phone = contacts[name]
    return f"{name}: {phone}"


def show_all(contacts: dict[str, str]) -> str:
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main() -> None:
    contacts: dict[str, str] = {}

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in {"exit", "close"}:
            print("Good bye!")
            break

        try:
            if command == "hello":
                print("How can I help you?")
            elif command == "add":  # "add [name] [phone number]"
                add_contact(args, contacts)
                print("Contact added.")
            elif command == "change":  # "change [name] [new phone number]"
                change_contact(args, contacts)
                print("Contact updated.")
            elif command == "phone":  # "phone [name]"
                contact_phone = show_phone(args, contacts)
                print(contact_phone)
            elif command == "all":
                all_contacts = show_all(contacts)
                print(all_contacts or "No contacts.")
            else:
                print("Invalid command.")
        except InvalidArgumentsError as e:
            print(f"Wait, I can't do that: {e}")
        except ContactExistsError:
            print("Contact already exists.")
        except ContactNotFoundError:
            print("Contact doesn't exist.")
        except Exception as e:
            print(f"Whoops, an unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
