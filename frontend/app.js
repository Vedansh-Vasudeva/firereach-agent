async function runAgent() {
  const icp = document.getElementById("icp").value.trim();
  const task = document.getElementById("task").value.trim();
  const company = document.getElementById("company").value.trim();
  const email = document.getElementById("email").value.trim();
  const resultEl = document.getElementById("result");

  resultEl.textContent = "Running FireReach...";

  try {
    const response = await fetch("http://127.0.0.1:8000/run-agent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        icp,
        task,
        company: company || null,
        email: email || null,
      }),
    });

    const data = await response.json();
    const payload = data.data || {};
    const signalLines = (payload.signals || [])
      .map((signal) => `- ${signal.label}: ${signal.evidence}`)
      .join("\n");

    resultEl.textContent = [
      `Status: ${data.status || "unknown"}`,
      data.message ? `Message: ${data.message}` : null,
      payload.company ? `Company: ${payload.company}` : null,
      payload.email ? `Recipient: ${payload.email}` : null,
      payload.signal_summary ? `Signals: ${payload.signal_summary}` : null,
      signalLines ? `\nSignal Evidence\n${signalLines}` : null,
      payload.account_brief ? `\nAccount Brief\n${payload.account_brief}` : null,
      payload.subject ? `\nSubject\n${payload.subject}` : null,
      payload.body ? `\nEmail Body\n${payload.body}` : null,
      payload.delivery_status ? `\nDelivery\n${JSON.stringify(payload.delivery_status, null, 2)}` : null,
    ]
      .filter(Boolean)
      .join("\n");
  } catch (error) {
    resultEl.textContent = `Status: error\nMessage: ${error.message}`;
  }
}
