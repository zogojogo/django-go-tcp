local json = require("cjson")

-- Read the user addresses from the specified file
local file = io.open("users_200.json", "r")
local users = json.decode(file:read("*all"))
file:close()

-- The number of times to repeat each user address
local repeat_count = 5

-- The index of the current user address in the list
local user_index = 1

function request()
  local user = users[user_index]
  local payload = {
    username = user.username,
    password = "password"
  }
  local headers = {
    ["Content-Type"] = "application/json",
  }
  local body = json.encode(payload)
  user_index = user_index + 1
  if user_index > #users then
    user_index = 1
  end
  return wrk.format("POST", "http://localhost/test/", headers, body)
end

function response(status, headers, body)
  if status ~= 200 then
    print("Error: " .. body)
  end
end
