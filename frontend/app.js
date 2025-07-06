const API_URL = "http://localhost:5000";

async function loadAudits() {
  const response = await fetch(`${API_URL}/audits`);
  const audits = await response.json();

  const auditsList = document.getElementById("audits");
  const findingsContainer = document.getElementById("findings-container");

  auditsList.innerHTML = "";
  findingsContainer.innerHTML = "";

  audits.forEach((audit) => {
    const auditItem = document.createElement("li");

    auditItem.innerHTML = `
      <strong>${audit.title}</strong><br/>
      Department: ${audit.department}<br/>
      Date: ${audit.date}<br/>
      Status: ${audit.status}<br/>
    `;

    const button = document.createElement("button");
    button.textContent = "View Findings";
    button.addEventListener("click", () => {
      loadFindings(audit.id);
    });

    auditItem.appendChild(button);
    auditsList.appendChild(auditItem);
  });
}

async function loadFindings(auditId) {
  const response = await fetch(`${API_URL}/findings/${auditId}`);
  const findings = await response.json();

  const findingsContainer = document.getElementById("findings-container");
  findingsContainer.innerHTML = "";

  findings.forEach((finding) => {
    const findingDiv = document.createElement("div");

    findingDiv.innerHTML = `
      <h3>Finding: ${finding.description}</h3>
      <p>Severity: ${finding.severity}</p>
      <p>Status: ${finding.status}</p>

      <form onsubmit="submitCAPA(event, ${finding.id})">
        <input type="text" name="action" placeholder="Action" required />
        <input type="text" name="assignee" placeholder="Assignee" required />
        <input type="date" name="due_date" required />
        <button type="submit">Add CAPA</button>
      </form>
      <hr/>
    `;

    findingsContainer.appendChild(findingDiv);
  });
}

async function submitCAPA(event, findingId) {
  event.preventDefault();
  const form = event.target;

  const action = form.action.value;
  const assignee = form.assignee.value;
  const due_date = form.due_date.value;

  await fetch(`${API_URL}/capas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      finding_id: findingId,
      action,
      assignee,
      due_date,
    }),
  });

  alert("CAPA created!");
  form.reset();
}

window.submitCAPA = submitCAPA;

document.addEventListener("DOMContentLoaded", () => {
  loadAudits();
});
