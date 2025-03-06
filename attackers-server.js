const http = require("http")

var instructions = []

function GetInstructions() {
    console.log("parsing")
    try {
        var parsed = JSON.stringify(instructions)
    } catch (err) {
        console.log("error while parsing: " + err)
        return ""
    }
    instructions = []
    return parsed
}

http.createServer(function(req, res) {
    if (req.method == "POST") {
        let body = ""
        req.on("data", function(chunk) {
            body += chunk
        })
        req.on("end", function() {
            console.log("received data is")
            console.log(body)
            body = JSON.parse(body)
            for (const key in body) {
                const instruction = body[key]
                if (instruction) {
                    instructions.push(instruction)
                }
            }
            console.log(instructions)
            res.end("Received data")
        })
    } else if (req.method == "GET") {
        res.end(GetInstructions())
    } else {
        res.end("Bad request")
    }
}).listen(8080, function() {
    console.log("listening on 8080")
})
