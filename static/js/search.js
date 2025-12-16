// Debounce function to limit the rate of function calls
function debounce(fn, delay=250) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}

// Fetch JSON data from a given URL
async function fetchJSON(url) {
    const response = await fetch(url, {
    method: "GET",
    credentials: "same-origin", // garantee cookies are sent
    headers: { "Accept": "application/json" } 
  });

  const contentType = response.headers.get("content-type") || "";

  // if response is not JSON, throw an error with details
  if (!contentType.includes("application/json")) {
    const text = await response.text();
    throw new Error(`Expected JSON, got: ${contentType}. First chars: ${text.slice(0, 80)}`);
  }

  // if response not ok, throw error with status
  if (!response.ok) throw new Error(`HTTP ${response.status}`);

  return response.json();
}

// Helper to create a table row message
function rowMessage(colspan, msg) {
  return `<tr><td colspan="${colspan}" class="text-muted">${msg}</td></tr>`;
}

// Clients
function initClientSearch() {

    const input = document.getElementById("clientSearch");
    const tbody = document.getElementById("clientsTbody");
    if (!input || !tbody) return;

    // Render clients into the table body
    const render = (clients) => {
        // If no clients, show "No results" message
        if (!clients.length) {
            tbody.innerHTML = rowMessage(6, "No results");
            return;
        }

        // Otherwise, render client rows
        tbody.innerHTML = clients.map(client => `
        <tr>
            <td>${client.name ?? ""}</td>
            <td>${client.company ?? ""}</td>
            <td>${client.email ?? ""}</td>
            <td>${client.phone ?? ""}</td>
            <td>${client.project_count ?? 0}</td>
            <td><a class="btn btn-sm btn-primary" href="/clients/${client.id}">View</a></td>
        </tr>
        `).join("");
    };

    // Debounced function to fetch and render clients
    const run = debounce(async () => {
        const q = input.value.trim();

        // Show searching message
        tbody.innerHTML = rowMessage(6, "Searching...");
        try {
            const data = await fetchJSON(`/api/clients?q=${encodeURIComponent(q)}`);
            render(data.results || []);
        } catch (err) {
            console.error(err);
            tbody.innerHTML = rowMessage(6, "Search error. Check console (F12).");
        }
    });

    input.addEventListener("input", run);
}

// Projects
function initProjectSearch() {
    const input = document.getElementById("projectSearch");
    const tbody = document.getElementById("projectsTbody");
    if (!input || !tbody) return;

    // Determine badge class based on project status
    const badge = (status) => {
        if (status === "Completed") return "bg-success";
        if (status === "In Progress") return "bg-warning text-dark";
        if (status === "Pending") return "bg-secondary";
        return "bg-light text-dark";
    };

    // Render projects into the table body
    const render = (projects) => {
        // If no projects, show "No results" message
        if (!projects.length) {
            tbody.innerHTML = rowMessage(5, "No results");
            return;
        }

        tbody.innerHTML = projects.map(project => `
        <tr>
            <td>${project.name ?? ""}</td>
            <td><a href="/clients/${project.client_id}">${project.client_name ?? ""}</a></td>
            <td><span class="badge ${badge(project.status)}">${project.status ?? ""}</span></td>
            <td>${project.due_date ? project.due_date : "-"}</td>
            <td><a class="btn btn-sm btn-outline-primary" href="/projects/${project.id}">View</a></td>
        </tr>
        `).join("");
    };

    // Debounced function to fetch and render projects
    const run = debounce(async () => {
        const q = input.value.trim();
        tbody.innerHTML = rowMessage(5, "Searching...");
        try {
            const data = await fetchJSON(`/api/projects?q=${encodeURIComponent(q)}`);
            render(data.results || []);
        } catch (err) {
            console.error(err);
            tbody.innerHTML = rowMessage(5, "Search error. Check console (F12).");
        }
    });

    input.addEventListener("input", run);
}

// Initialize search functionalities on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
    initClientSearch();
    initProjectSearch();
});