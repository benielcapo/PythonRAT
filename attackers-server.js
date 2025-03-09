const http = require("http")
const path = require("path")
const fs = require("fs")
const multiparty = require("multiparty")

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
        if (req.url == "/upload") {
            const form = new multiparty.Form()
            form.parse(req, (err, fields, files) => {
                if (err) {
                    console.log("error parsing form: " + err)
                    res.end("Error while uploading files")
                    return
                }
                const uploadedFile = files.file[0]
                const uploadPath = path.join(__dirname, uploadedFile.originalFilename)
                fs.copyFile(uploadedFile.path, uploadPath, (copyErr) => {
                    if (copyErr) {
                        console.log("error copying to path: " + copyErr)
                        res.end("Error copying to file")
                        return
                    }
                    res.end("Good")
                })
            })
        } else {
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
        }
    } else if (req.method == "GET") {
        res.end(GetInstructions())
    } else {
        res.end("Bad request")
    }
}).listen(8080, function() {
    console.log("listening on 8080")
})
