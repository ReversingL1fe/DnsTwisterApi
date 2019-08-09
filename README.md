# DnsTwisterApi
Developed a working python script to extract the data from the DNSTwister api and place them through some logic to print out the domians and ips that have been recently stood up. This code is ment to work in tangent with splunk, but can be used on other management systems also. (Works on linux and windows systems)

There are 3 csv's.

-The list_domains csv is used to create the incrimental list that would be for looped over and created updates/incidents for.

-The bad_items.csv is used to store all of the previously extracted data to reference for in future code executation to make sure all incidents created are unique.

-The incidents.csv list is loaded with domains and ips that have recently been stood up and need to be anaalyzed by the team. After analysis and incident creation the csv list needs to be cleared. 

Before executing the script you need to make sure the directory path within the functions lead to the appropriate folder that you allocate the program files towards. 

Have any questions, email me at dal7@rice.edu.
