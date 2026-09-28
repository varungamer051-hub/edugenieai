console.log("EduGenie app.js loaded");

document.addEventListener("DOMContentLoaded", function () {
    console.log("EduGenie DOM ready");

    const generateBtn = document.getElementById("generateBtn");
    const clearBtn = document.getElementById("clearBtn");
    const task = document.getElementById("task");
    const userInput = document.getElementById("userInput");
    const level = document.getElementById("level");
    const result = document.getElementById("result");

    if (!generateBtn) {
        console.error("Generate button not found");
        return;
    }

    console.log("Generate button found");

    generateBtn.addEventListener("click", async function () {
        console.log("GENERATE CLICKED");

        const selectedTask = task.value;
        const input = userInput.value.trim();
        const selectedLevel = level.value;

        if (!input) {
            result.innerHTML = `
                <div class="error">
                    Please enter a question or topic.
                </div>
            `;
            return;
        }

        generateBtn.disabled = true;
        generateBtn.textContent = "Generating...";

        result.innerHTML = `
            <div class="loading">
                🤖 EduGenie is thinking...
            </div>
        `;

        let endpoint;
        let body;

        if (selectedTask === "explain") {
            endpoint = "/explain";
            body = {
                text: input
            };

        } else if (selectedTask === "qa") {
            endpoint = "/qa";
            body = {
                question: input
            };

        } else if (selectedTask === "quiz") {
            endpoint = "/quiz";
            body = {
                text: input
            };

        } else if (selectedTask === "summarize") {
            endpoint = "/summarize";
            body = {
                text: input
            };

        } else if (selectedTask === "recommend") {
            endpoint = "/learn/recommendations";
            body = {
                topic: input,
                level: selectedLevel
            };

        } else {
            result.innerHTML = `
                <div class="error">
                    Unknown task selected.
                </div>
            `;

            generateBtn.disabled = false;
            generateBtn.textContent = "Generate";
            return;
        }

        console.log("Sending POST request:", endpoint);
        console.log("Request body:", body);

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(body)
            });

            console.log("Backend status:", response.status);

            const responseText = await response.text();

console.log("Raw backend response:", responseText);

let data;

try {
    data = JSON.parse(responseText);
} catch (parseError) {
    throw new Error(
        "Backend returned invalid JSON: " + responseText
    );
}

console.log("Backend response:", data);

if (!response.ok) {
    throw new Error(
        data.error ||
        data.detail ||
        data.message ||
        "Backend returned an error."
    );
}

            let answer = "";

            if (typeof data === "string") {
                answer = data;

            } else if (data.answer) {
                answer = data.answer;

            } else if (data.explanation) {
                answer = data.explanation;

            } else if (data.result) {
                answer = data.result;

            } else if (data.summary) {
                answer = data.summary;

            } else if (data.content) {
                answer = data.content;

            } else if (data.recommendations) {
                answer = data.recommendations;

            } else {
                answer = JSON.stringify(data, null, 2);
            }

            result.innerHTML = `
                <div class="ai-result">
                    <div class="ai-result-label">
                        ✨ AI Response
                    </div>

                    <div class="ai-result-content">
                        ${escapeHtml(answer)}
                    </div>
                </div>
            `;

        } catch (error) {
            console.error("EduGenie request failed:", error);

            result.innerHTML = `
                <div class="error">
                    <h3>Request failed</h3>
                    <p>${escapeHtml(error.message)}</p>
                    <p>Check the VS Code terminal for more information.</p>
                </div>
            `;

        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = "Generate";
        }
    });

    if (clearBtn) {
        clearBtn.addEventListener("click", function () {
            userInput.value = "";

            result.innerHTML = `
                <p class="placeholder">
                    Your AI-generated result will appear here.
                </p>
            `;
        });
    }
});


function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}