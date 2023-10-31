from datetime import datetime, date, timedelta  # Import datetime-related modules.
from collections import UserList  # Import UserList for custom list.
import pickle  # Import pickle for object serialization.


from util_func import *  # Import utility functions from the custom module 'util_func'.
import sort  # Import sorting functions from the custom module 'sort'.

from abc import ABC, abstractmethod

##base class for user interface
class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_commands(self):
        pass


class ConsoleUserInterface(UserInterface):
    def display_contacts(self, contacts):
        pass

    def display_commands(self):
        pass
    


# Define a class for representing individual contacts in the address book.
class Contact:
    id = 0  # Class variable to assign unique IDs to contacts.

    def __init__(self, name: str, address: str = None, phone_number: str = None,
                 email: str = None, birthday: str = None, notes: str = None):
        # Initialize contact attributes.
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birthday = birthday
        self.notes = notes
        self.id = Contact.id  # Assign a unique ID to the contact.
        Contact.id += 1  # Increment the class variable for the next contact.

    @property ##By using the @property decorator, the value method is accessed like an attribute rather than a method. So, when you access contact_instance.value, it returns a list containing the contact's information
    ##ex. contact_instance = Contact("John Doe", "123-456-7890", "johndoe@example.com", "123 Main St", "1990-01-15", "Some notes")
    ##contact_info = contact_instance.value
    ###print(contact_info)
    def value(self):
        return [self.name, self.phone_number, self.email, self.address, self.birthday, self.notes._value]

    @property
    def value_id(self):
        return [self.id, self.name, self.phone_number, self.birthday, self.email, self.address, self.notes._value]

    def edit_attribute(self, attribute, new_value):
        # Method to edit specific attributes of a contact.
        if attribute == 'name':
            self.name = new_value
        elif attribute == 'phone number':
            self.phone_number = new_value
        elif attribute == 'email':
            self.email = new_value
        elif attribute.find('address') >= 0:
            self.address = new_value
        elif attribute == 'birthday date':
            self.birthday = new_value
        elif attribute.find('notes') >= 0:
            self.notes.value = new_value

# Define a custom list class for managing contacts.
class Book(UserList):

    def add_contact(self, contact):
        # Method to add a new contact to the list.
        self.data.append(contact)  ##the self.data list is implicitly created because the Book class is a subclass of UserList

    def existing_contact_names(self):
        # Method to retrieve names of existing contacts.
        contact_names = [contact.name for contact in self.data]
        return contact_names

    def find_contacts_of_names(self, contact_to_find):
        # Method to find contacts with names containing a specific string.
        contacts_to_find = []
        for contact in self.data:
            if contact_to_find in contact.name:
                contacts_to_find.append(contact)
        return contacts_to_find

    def find_nearest_birthday_people(self, number_of_days):
        # Method to find contacts with birthdays within a specified number of days.
        today = datetime.today().date()
        today_future_date = today + timedelta(days=number_of_days)
        contacts_within_timeframe = []

        for contact in self.data:
            split_char = contact.birthday[2]
            birthday_of_contact = contact.birthday.split(split_char)
            birthday_of_contact = date(int(birthday_of_contact[2]), int(birthday_of_contact[1]), int(birthday_of_contact[0]))
            birthday_of_contact = birthday_of_contact.replace(year=today.year)
            if today <= birthday_of_contact <= today_future_date:
                contacts_within_timeframe.append(contact)

        return contacts_within_timeframe

    def find_contacts_by_id(self, find_id):
        # Method to find contacts by their unique ID.
        found_contacts = []
        for contact in self.data:
            if find_id == contact.id:
                found_contacts.append(contact)
        return found_contacts

    def find_contacts_by_name(self, name):
        # Method to find contacts by their name.
        found_contacts = []
        for contact in self.data:
            if name == contact.name:
                found_contacts.append(contact)
        return found_contacts

    def delete_contact_by_id(self, id):
        # Method to delete a contact by its unique ID.
        contact_index = 0
        for contact in self.data:
            if contact.id == id:
                self.data.pop(contact_index)
            contact_index += 1
        return contact

    def find_contact_by_notes(self, notes):
        # Method to find contacts by the content of their notes.
        found_contacts = []
        for contact in self.data:
            if contact.notes.value.lower().find(notes.lower()) >= 0:
                found_contacts.append(contact)
        return found_contacts

    def tags_in_book(self):
        # Method to check if any contacts have tags associated with their notes.
        for contact in self.data:
            if contact.notes._tags:
                return True

# Define a class to represent the notes associated with a contact.
class Notes:

    def __init__(self, value):
        self._value = value
        self._tags = set()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        # Setter for modifying the note's value.
        if new_value:
            self._value = new_value

    @property
    def tags(self):
        if self._tags:
            return ', '.join([str(tag) for tag in self._tags])
        return 'There are no tags.'

    @tags.setter
    def tags(self, new_tag_values):
        # Setter for adding tags to the note.
        if new_tag_values:
            for tag in new_tag_values:
                self._tags.add(tag.strip())

    def delete(self):
        if self._value:
            self._value = None
            return 'Notes have been deleted.'
        return 'There are no notes.'

    def add_tags(self, new_tag):
        for tag in new_tag:
            self._tags.update(tag.strip())

# The main function provides a menu-based interface for managing the contact book.
def main():

    my_contact_book = Book()

    user_interface = ConsoleUserInterface()

    
    user_interface.display_contacts(my_contact_book.data)  
    user_interface.display_commands()


    # Menu text with options for different operations.
    MENU_TEXT = """
    Menu:
    1. Create a new contact
    2. Edit contact
    3. Find nearest birthday people
    4. Display all contacts
    5. Find contacts
    6. Delete contact
    7. Find notes
    8. Sort or find contacts by tags
    9. Sort folders in the path
    10. Save information as a file
    11. Load data from a file
    0. Exit bot-assistant
    """
    THERE_ARE_NO_CONTACTS_TEXT = f'There are no contacts yet. Please create a new contact.'

    # Text for creating a new contact.
    CREATE_NEW_CONTACT_TEXT = """
    To create a new contact, you will be asked for a name, phone number, email address, address, birthday date, and notes.
    A contact cannot be created without a name.
    """
    # Text for editing a contact.
    EDIT_TEXT = """
    Choose the attribute to edit:
    1. Name
    2. Phone number
    3. Birthday date
    4. Email address
    5. Address
    6. Notes
    7. Tags
    """

    contacts = Book()  # Create a Book instance to store contacts.

    while True:
        print(MENU_TEXT)  # Display the menu.
        menu_choice = valid_choice_menu_edit_find('menu')  # Get a valid menu choice.

        if not menu_choice:
            print(not_valid_message('choice'))
            continue

        if menu_choice == '0':
            break  # Exit the program.

        if menu_choice == '1':
            print(CREATE_NEW_CONTACT_TEXT)  # Prompt for creating a new contact.

            input_name = valid_name('name')  # Get a valid name.
            input_phone_number = valid_phone_number('phone number', contacts)  # Get a valid phone number.
            input_birthday = valid_birthday('birthday date')  # Get a valid birthday date.
            input_email = valid_email('email address')  # Get a valid email address.
            input_address = input('Please enter address: ')  # Get an address.
            input_notes = Notes(input('Please enter notes: '))  # Get notes as input and create a Notes instance.

            new_contact = [Contact(input_name, input_address, input_phone_number, input_email, input_birthday, input_notes)]

            input_tags = input('Would you like to add tags to this contact? (Please separate them by comma)\nTags: ').lower().strip()
            if input_tags:
                new_contact[0].notes.tags = input_tags.split(',')

            contacts.add_contact(new_contact[0])  # Add the new contact to the contact list.

            print('Contact has been created.')
            display_contacts(new_contact)

        if menu_choice == '2':
            if contacts:
                name_of_contact_to_edit = valid_name('name to edit')  # Get the name of the contact to edit.
                found_contacts = list(filter(lambda x: name_of_contact_to_edit in x, contacts.existing_contact_names()))
                if len(found_contacts) > 1:
                    print("There are several contacts in the book.")
                    found_contacts = contacts.find_contacts_of_names(name_of_contact_to_edit)
                    display_contacts(found_contacts)
                    id_of_the_contact_to_edit = input('Choose ID: ')
                    contact_to_edit = [contact for contact in found_contacts if contact.id == int(id_of_the_contact_to_edit)]
                    display_contacts(contact_to_edit)

                if len(found_contacts) == 1:
                    contact_to_edit = contacts.find_contacts_of_names(name_of_contact_to_edit)
                    display_contacts(contact_to_edit)

                if len(found_contacts) == 0:
                    print(f'There is no contact named {name_of_contact_to_edit}.')
                    continue

            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue

            print(EDIT_TEXT)  # Display the options for editing.

            edit_choice = valid_choice_menu_edit_find('edit')  # Get a valid edit choice.

            command, arg = get_attribute_to_edit(edit_choice)  # Get the attribute to edit and the corresponding command function.

            if arg == 'phone number':
                new_value_of_attribute = command(arg, contacts)  # Get a new phone number.

            elif arg == "":
                show_input_tag(contact_to_edit[0])
                continue

            else:
                new_value_of_attribute = command(arg)  # Get a new value for the specified attribute.

            contact_to_edit[0].edit_attribute(arg, new_value_of_attribute)  # Edit the specified attribute of the contact.

            display_contacts(contact_to_edit)  # Display the updated contact.

        if menu_choice == '3':
            if contacts:
                days_within_to_search_birthday_people = int(get_valid_number_of_days())  # Get the number of days to search for upcoming birthdays.
                contacts_within_timeframe = contacts.find_nearest_birthday_people(days_within_to_search_birthday_people)
                if contacts_within_timeframe:
                    display_contacts(contacts_within_timeframe)
                else:
                    print(f'There are no coming birthdays in the nearest {days_within_to_search_birthday_people} days.')

            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue

        if menu_choice == '4':
            if contacts:
                display_contacts(contacts)  # Display all contacts.

            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue

        if menu_choice == '5':
            if contacts:
                print("How do you want to find contacts?\n1. By ID\n2. By name")
                edit_contact_choice = valid_choice_menu_edit_find('find')  # Get a choice for finding contacts.

                if edit_contact_choice == '1':
                    id_to_find = get_valid_id_to_find(contacts)  # Get a valid ID to find.
                    found_contacts = contacts.find_contacts_by_id(id_to_find)
                    display_contacts(found_contacts)
                    continue

                if edit_contact_choice == '2':
                    while True:
                        name_to_find = valid_name('name')  # Get a name to find.
                        found_contacts = contacts.find_contacts_by_name(name_to_find)
                        if found_contacts:
                            display_contacts(found_contacts)
                            break
                        print(f'There is no contact with the name {name_to_find}. Would you like to try again?\n1. Yes\n2. No')
                        decision_to_try_again = valid_choice_menu_edit_find('find')  # Get a choice to try again.
                        if decision_to_try_again == 2:
                            break

            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue

        if menu_choice == '6':
            if contacts:
                display_contacts(contacts)
                print('Which contact would you like to delete?')
                id_to_delete = int(get_valid_id_to_find(contacts))  # Get the ID of the contact to delete.
                deleted_contact = [contacts.delete_contact_by_id(id_to_delete)]  # Delete the contact.
                print("The following contact has been deleted from the book:")
                display_contacts(deleted_contact)

            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)

        if menu_choice == '7':
            if contacts:
                notes_to_find = input('Please enter notes you would like to find: ')  # Get notes to find.
                if not notes_to_find:
                    display_contacts(contacts)
                    continue
                found_contacts = contacts.find_contact_by_notes(notes_to_find)  # Find contacts by notes.
                display_contacts(found_contacts)

            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue

        if menu_choice == '9':
            folder_to_sort = get_valid_path()  # Get a valid folder path to sort.
            sort.sort_files_to_folders(folder_to_sort)  # Sort files into folders within the specified path.
            print('Folder is sorted. Go check it!')

        if menu_choice == '8':
            if contacts:
                find_sort_contacts_by_tags(contacts)  # Find and sort contacts by tags.
                continue
            print(THERE_ARE_NO_CONTACTS_TEXT)

        if menu_choice == '10':
            if contacts:
                with open('book_with_contacts.bin', "wb") as fh:
                    pickle.dump(contacts, fh)  # Save the contact book to a binary file.
                    print('File has been saved.')
                    continue
            print(THERE_ARE_NO_CONTACTS_TEXT)

        if menu_choice == '11':
            contacts = load_data_from_file()  # Load the contact book data from a file.
            print('Data has been loaded!')
            display_contacts(contacts)

if __name__ == '__main__':
    main() 
