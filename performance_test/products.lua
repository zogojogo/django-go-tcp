local json = require("cjson")

local preserved_keyword = {
    "cincin",
    "game",
    "kamera",
    "laptop",
    "smartphone",
    "smartwatch",
    "speaker",
    "tenda",
    "kalung",
    "baju",
}

local preserved_category = {
    11043169,
    11044024,
    11043657,
    11043661,
    11043439
}

function request()
    local limit = 10
    local prev_cursor = 0
    local next_cursor = 0
    local q = preserved_keyword[math.random(#preserved_keyword)]
    local cat = 0
    local headers = {
        ["Content-Type"] = "application/json",
    }
    return wrk.format("GET", "http://localhost/products/?q=" .. q .. "&cat=" .. cat .. "&limit=" .. limit .. "&prev_cursor=" .. prev_cursor .. "&next_cursor=" .. next_cursor, headers, nil)
end

function response(status, headers, body)
    if status ~= 200 then
       print(string.format("Error: status=%d, body=%s", status, body))
    end
    -- if status == 200 then
    --     print(string.format("Success: status=%d, body=%s", status, body))
    --   end
end
