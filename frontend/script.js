const API_URL = "http://127.0.0.1:8000";

async function loadTasks() {
    const response = await fetch(`${API_URL}/tasks`);
    const tasks = await response.json();

    const taskList = document.getElementById("task-list");

    taskList.innerHTML = "";

    tasks.forEach(task => {
        const taskCard = document.createElement("div");

        taskCard.className = "task-card";

        taskCard.innerHTML = `
            <h3 class="${task.completed ? "completed" : ""}">
                ${task.title}
            </h3>

            <p>${task.description || ""}</p>

            <button
                class="complete-btn"
                onclick="completeTask(${task.id})"
            >
                ${task.completed ? "Completed" : "Complete"}
            </button>

            <button
                class="delete-btn"
                onclick="deleteTask(${task.id})"
            >
                Delete
            </button>
        `;

        taskList.appendChild(taskCard);
    });
}


async function addTask() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    if (!title) {
        alert("Please enter a task title.");
        return;
    }

    await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            description: description
        })
    });

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

    loadTasks();
}


async function completeTask(taskId) {
    await fetch(`${API_URL}/tasks/${taskId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            completed: true
        })
    });

    loadTasks();
}


async function deleteTask(taskId) {
    await fetch(`${API_URL}/tasks/${taskId}`, {
        method: "DELETE"
    });

    loadTasks();
}


loadTasks();
