#!/bin/bash

while (true) do
	
	scanimage > ./temp_PFAS;
	if [[ -s ./temp_PFAS ]]; then #if temp_PFAS is not empty, something was scanned
		cp ./temp_PFAS ./scanned_PFAS;
	fi
done

