# Example: Use Case Diagram

@startuml
left to right direction

actor User
actor Admin
actor System

rectangle "Contact Management System" {
    User -- (View Contacts)
    User -- (Add Contact)
    User -- (Edit Contact)
    User -- (Delete Contact)
    User -- (Search Contacts)

    Admin -- (Manage Users)
    Admin -- (Generate Reports)

    (Add Contact) --> (Search Contacts)
    (Edit Contact) --> (View Contacts)
    (Delete Contact) --> (View Contacts)

    (View Contacts) --> (Search Contacts)
    (Generate Reports) --> (View Contacts)

    System -- (Sync Contacts)
    System -- (Backup Data)
    
    (Sync Contacts) --> (Add Contact)
    (Backup Data) --> (Edit Contact)
    (Backup Data) --> (Delete Contact)
}

@enduml