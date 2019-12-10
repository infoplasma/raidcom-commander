# RAIDCOM COMMANDER
---
### small tool to assist with the creation of Hitachi raicomm commands for creating and deleting LDEVs.

you can use the tool to create LDEV both replicated (gad) or non replicated.

you will have to provide the following data:

+ ldev id (last 4 hex digits)
+ capacity in GB
+ pool ID
+ GAD group name, if required
+ select a proper prefix for the LDEV

You can use a form by from where you can select the option from presets, by launching:

```
$ python raidcommaner.py
```

Or you can directly modify the config/config.yaml file, and the launch 'writer --create'
