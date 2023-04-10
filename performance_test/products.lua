local json = require("cjson")

function payload()
    local payload = {
        limit = 10,
        prev_cursor = 0,
        next_cursor = 0,
        q = "",
        cat = 0,
    }
    return json.encode(payload)
end

function response(status, headers, body)
    if status ~= 200 then
       print(string.format("Error: status=%d, body=%s", status, body))
    end

    -- if status == 200 then
    --     print(string.format("Success: status=%d, body=%s", status, body))
    --   end
end

local body = payload()
wrk.method = "GET"
wrk.headers["Content-Type"] = "application/json"
wrk.body = body
