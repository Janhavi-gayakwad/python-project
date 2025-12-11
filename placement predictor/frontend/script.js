document.addEventListener("DOMContentLoaded", () => {
  // ---------------- Placement Prediction ----------------
  const placementForm = document.getElementById("placementForm");
  const placementResult = document.getElementById("placementResult");

  placementForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      cgpa: parseFloat(document.getElementById("cgpa").value),
      technical_skills: parseFloat(document.getElementById("technical_skills").value),
      soft_skills: parseFloat(document.getElementById("soft_skills").value),
      internships: parseInt(document.getElementById("internships").value),
      projects: parseInt(document.getElementById("projects").value),
      backlogs: parseInt(document.getElementById("backlogs").value),
      twelfth_percentage: parseFloat(document.getElementById("twelfth_percentage").value),
      branch: document.getElementById("branch").value
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        placementResult.innerHTML = `
          <p><strong>Probability:</strong> ${data.probability}%</p>
          <p><strong>Status:</strong> ${data.label}</p>
          <p><strong>Suggestions:</strong><ul>${data.suggestions.map(s => `<li>${s}</li>`).join("")}</ul></p>
        `;
      } else {
        placementResult.innerText = "Error: " + data.error;
      }
    } catch (err) {
      placementResult.innerText = "Error connecting to backend";
      console.error(err);
    }
  });

  // ---------------- Resume Analysis ----------------
  const resumeForm = document.getElementById("resumeForm");
  const resumeResult = document.getElementById("resumeResult");

  resumeForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("resumeFile");
    if (!fileInput.files.length) {
      alert("Please select a resume file!");
      return;
    }

    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/analyze_resume", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        resumeResult.innerHTML = `
          <p><strong>Skills Found:</strong> ${data.skills_found.join(", ")}</p>
          <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ")}</p>
          <p><strong>Recommended Courses:</strong><br> - ${data.recommendations.join("<br> - ")}</p>
          <p><strong>Summary:</strong> ${data.summary}</p>
        `;
      } else {
        resumeResult.innerText = "Error: " + data.error;
      }
    } catch (err) {
      resumeResult.innerText = "Error connecting to backend";
      console.error(err);
    }
  });
});
