# Example: Component Diagram

@startuml

' Define components
package "User Interface" {
    [Contact List View]
    [Contact Detail View]
    [Search View]
    [User Profile View]
}

package "Contact Management" {
    [Contact Service] 
    [Search Service]
    [User Profile Service]
}

package "Data Storage" {
    [Contact Database]
    [User Profile Database]
}

package "Notification Service" {
    [Email Notification Service]
    [SMS Notification Service]
}

package "External Services" {
    [Social Media Integration]
    [CRM Integration]
}

' Define relationships
[Contact List View] --> [Contact Service] : Request contact list
[Contact Detail View] --> [Contact Service] : Request contact details
[Search View] --> [Search Service] : Request search results
[User Profile View] --> [User Profile Service] : Request user profile

[Contact Service] --> [Contact Database] : Read/Write contact data
[User Profile Service] --> [User Profile Database] : Read/Write user profile data

[Search Service] --> [Contact Database] : Search contact data

[Contact Service] --> [Email Notification Service] : Send email notifications
[Contact Service] --> [SMS Notification Service] : Send SMS notifications

[Email Notification Service] --> [External Services] : Integration for email delivery
[SMS Notification Service] --> [External Services] : Integration for SMS delivery

[Social Media Integration] --> [Contact Service] : Sync social media contacts
[CRM Integration] --> [Contact Service] : Sync CRM contacts

@enduml