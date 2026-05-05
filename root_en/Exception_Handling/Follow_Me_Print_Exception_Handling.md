# Print Failure

## Print Document Does Not Appear on the Dashboard
　　
　　Confirm whether the job appears on the print document dashboard after the user submits the print job.
　　
```plantuml
@startuml
start
if (Is there a print job on the dashboard?) then (Yes)
  :--> Print Login and Dispatch Flow;
else (No)
    if (Are PSS consumer & monitor started?) then (Yes)
        :--> Is controlled queue printing enabled?;
    else (No)
        :Start PSS service and print again;
    endif
endif

stop
@enduml
```

## Is Controlled Queue Printing Enabled
　　
　　Check the roaming print printer settings in [Printer Management & Maintenance].

```plantuml
@startuml
start

if (Is controlled queue printing enabled?) then (Yes)
  :--> Roaming Print Queue Error Flow;
else (No)
  :Enable controlled queue printing;
endif

stop
@enduml
```

## Roaming Print Queue Error Flow
　　
　　Check why the roaming print job fails to display in the roaming queue.

```plantuml
@startuml
start
:Check roaming print queue;

if (Insufficient user permissions?) then (Yes)
  :--> Check user permissions;
elseif (Insufficient user permissions - Color?) then (Yes)
  :--> Check user permissions;
else (No)
  :For other errors, check the LOG;
endif

stop
@enduml
```

## Print Login and Dispatch Flow
　　
    Check why the roaming print job cannot be dispatched to the printer.

```plantuml
@startuml
start
:User login and printing;

if (Login successful?) then (Yes)
  :--> Check user print operation;
else (No)
  :--> Device login failure;
endif

stop
@enduml
```

## Check User Print Operation

 Check the response of the print job after submitting the print.

```plantuml
@startuml
start
:Click 'My Documents' and print;

if (Can print and output paper?) then (Yes)
  :Operation successfully completed;
else (No)
  :--> Check device connection;
endif

stop
@enduml
```

## Device Login Failure

 Check the user's device login function.

```plantuml
@startuml
start
:Is the device bound?;
/' Check user account '/
if (Already bound?) then (Yes)
    if (Account exists?) then (Yes)
        :For other errors, check the LOG;
    else (No)
        :Create a new account or check account import;
    endif 
else (No)
  :Bind the device and try again;
endif

stop
@enduml
```

## Check Device Connection

 Check if the device is online.

```plantuml
@startuml
start

if (Can access device backend?) then (Yes)
    if (System printer status is Ready?) then (Yes)
        :If unable to print, check LOG or restart Windows Spooler service;
    else (No)
        :Reboot the device;
    endif 
else (No)
  :Check device network connection;
endif

stop
@enduml
```
