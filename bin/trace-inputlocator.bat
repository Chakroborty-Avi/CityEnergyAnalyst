rem run the trace-inputlocator for as many tools as possible, collecting the data

rem first delete the config file (force default config)
del %userprofile%\cea.config

rem new reference-case in C:\reference-case-open\baseline
cea extract-reference-case

cea trace-inputlocator --scripts copy-default-databases, data-helper
cea trace-inputlocator --scripts radiation-daysim, demand

rem make sure to run the quicker version (type-scpanel=FP)
cea-config solar-collector --type-scpanel FP
cea trace-inputlocator --scripts solar-collector

cea trace-inputlocator --scripts photovoltaic, photovoltaic-thermal
cea trace-inputlocator --scripts sewage-potential, lake-potential

cea trace-inputlocator --scripts thermal-network-matrix, decentralized

cea-config optimization --initialind 2 --ngen 2
cea trace-inputlocator --scripts optimization

cea trace-inputlocator --scripts plots

