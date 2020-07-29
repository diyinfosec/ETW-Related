mkdir Provider_Meta
mkdir Provider_Event_Meta

for /F "delims=" %%a in (provider_names.txt) do (
     cli.exe /name %%a /eventmeta /out  Provider_Event_Meta/%%a_event_meta.txt
     cli.exe /name %%a /meta /out Provider_Meta/%%a_meta.txt
)