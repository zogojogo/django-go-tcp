wrk -t8 -c50 -d10s -s products.lua http://localhost/products/ 
wrk -t8 -c200 -d10s -s products.lua http://localhost/products/ 
