# Example: Activity Diagram

@startuml
|User|
start
:Login;
:View Dashboard;

|System|
if (Has Contacts?) then (yes)
  :Display Contacts List;
else (no)
  :Show No Contacts Message;
endif

|User|
:Add New Contact;
:Enter Contact Details;

|System|
:Validate Contact Information;
if (Valid?) then (yes)
  :Save Contact;
  :Update Contacts List;
else (no)
  :Show Validation Errors;
endif

|User|
:Edit Contact;
:Select Contact to Edit;
:Modify Contact Details;

|System|
:Validate Updated Information;
if (Valid?) then (yes)
  :Update Contact;
  :Refresh Contacts List;
else (no)
  :Show Validation Errors;
endif

|User|
:Delete Contact;
:Select Contact to Delete;

|System|
:Confirm Deletion;
if (Confirmed?) then (yes)
  :Remove Contact;
  :Update Contacts List;
else (no)
  :Cancel Deletion;
endif

|User|
:Sync Contacts;
:Initiate Synchronization;

|System|
:Synchronize with Server;
:Update Local Contact Database;

|User|
:Logout;
:End Session;
stop

@enduml