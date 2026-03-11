async function runAgent() {

const icp = document.getElementById("icp").value
const task = document.getElementById("task").value
const company = document.getElementById("company").value
const email = document.getElementById("email").value

document.getElementById("result").innerText = "Running agent..."

const response = await fetch("http://127.0.0.1:8000/run-agent", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
icp: icp,
task: task,
company: company || null,
email: email
})

})

const data = await response.json()

document.getElementById("result").innerText =
JSON.stringify(data, null, 2)

}