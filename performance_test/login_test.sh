wrk -t8 -c100 -d10s -s login.lua http://localhost/login/ 
wrk -t8 -c200 -d10s -s login.lua http://localhost/login/ 
