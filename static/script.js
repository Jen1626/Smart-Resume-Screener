let currentCandidateId = null;

const resumeFile = document.getElementById("resumeFile");
const fileName = document.getElementById("fileName");
const parseResumeBtn = document.getElementById("parseResumeBtn");
const uploadStatus = document.getElementById("uploadStatus");

const candidateDetails = document.getElementById("candidateDetails");

const jobTitle = document.getElementById("jobTitle");
const jobDescription = document.getElementById("jobDescription");
const analyzeBtn = document.getElementById("analyzeBtn");
const matchStatus = document.getElementById("matchStatus");

const matchResult = document.getElementById("matchResult");

const ranking = document.getElementById("ranking");
const refreshRankingBtn =
  document.getElementById("refreshRankingBtn");


// =========================================================
// FILE SELECTION
// =========================================================

resumeFile.addEventListener("change", () => {

  if (!resumeFile.files.length) {
    fileName.textContent = "No file chosen";
    return;
  }

  fileName.textContent =
    resumeFile.files[0].name;
});


// =========================================================
// ESCAPE HTML
// =========================================================

function escapeHtml(value) {

  const entities = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  };

  return String(value ?? "")
    .replace(
      /[&<>"']/g,
      character => entities[character]
    );
}


// =========================================================
// FORMAT OBJECT VALUE
// =========================================================

function formatObject(item) {

  if (!item || typeof item !== "object") {
    return escapeHtml(item);
  }

  const values = Object.values(item)
    .filter(value => value !== null && value !== undefined && value !== "")
    .map(value => {

      if (Array.isArray(value)) {
        return value.join(", ");
      }

      return String(value);
    });

  return escapeHtml(
    values.join(" — ")
  );
}


// =========================================================
// GENERAL LIST
// =========================================================

function renderList(items) {

  if (!items || !items.length) {
    return `
      <div class="empty-state">
        No information available.
      </div>
    `;
  }

  return `
    <ul class="info-list">
      ${items.map(item => {

        if (typeof item === "object") {

          return `
            <li>
              ${formatObject(item)}
            </li>
          `;
        }

        return `
          <li>
            ${escapeHtml(item)}
          </li>
        `;

      }).join("")}
    </ul>
  `;
}


// =========================================================
// TAGS
// =========================================================

function tags(items = [], cls = "") {

  if (!items || !items.length) {
    return `
      <span class="status">
        None
      </span>
    `;
  }

  return items.map(item => {

    let value = item;

    if (typeof item === "object") {
      value = Object.values(item).join(" — ");
    }

    return `
      <span class="tag ${cls}">
        ${escapeHtml(value)}
      </span>
    `;

  }).join("");
}


// =========================================================
// EDUCATION CARDS
// =========================================================

function renderEducation(items) {

  if (!items || !items.length) {
    return `
      <div class="empty-state">
        No education information available.
      </div>
    `;
  }

  return `
    <div class="education-list">

      ${items.map(item => {

        if (typeof item !== "object") {

          return `
            <div class="education-card">
              <div class="education-title">
                ${escapeHtml(item)}
              </div>
            </div>
          `;
        }

        return `
          <div class="education-card">

            <div class="education-icon">
              🎓
            </div>

            <div class="education-content">

              <div class="education-title">
                ${escapeHtml(
                  item.degree ||
                  item.institution ||
                  "Education"
                )}
              </div>

              ${
                item.institution
                  ? `
                    <div class="education-institution">
                      ${escapeHtml(item.institution)}
                    </div>
                  `
                  : ""
              }

              ${
                item.dates
                  ? `
                    <div class="education-date">
                      ${escapeHtml(item.dates)}
                    </div>
                  `
                  : ""
              }

              ${
                item.details
                  ? `
                    <div class="education-details">
                      ${escapeHtml(item.details)}
                    </div>
                  `
                  : ""
              }

            </div>

          </div>
        `;

      }).join("")}

    </div>
  `;
}


// =========================================================
// EXPERIENCE
// =========================================================

function renderExperience(items) {

  if (!items || !items.length) {
    return `
      <div class="empty-state">
        No professional experience listed.
      </div>
    `;
  }

  return `
    <div class="experience-list">

      ${items.map(item => {

        if (typeof item !== "object") {

          return `
            <div class="experience-card">
              ${escapeHtml(item)}
            </div>
          `;
        }

        return `
          <div class="experience-card">

            <div class="experience-icon">
              💼
            </div>

            <div class="experience-content">

              <div class="experience-title">
                ${escapeHtml(
                  item.role ||
                  item.position ||
                  item.title ||
                  "Experience"
                )}
              </div>

              ${
                item.company
                  ? `
                    <div class="experience-company">
                      ${escapeHtml(item.company)}
                    </div>
                  `
                  : ""
              }

              ${
                item.dates
                  ? `
                    <div class="experience-date">
                      ${escapeHtml(item.dates)}
                    </div>
                  `
                  : ""
              }

              ${
                item.description
                  ? `
                    <div class="experience-description">
                      ${escapeHtml(item.description)}
                    </div>
                  `
                  : ""
              }

            </div>

          </div>
        `;

      }).join("")}

    </div>
  `;
}


// =========================================================
// PROJECTS
// =========================================================

function renderProjects(items) {

  if (!items || !items.length) {
    return `
      <div class="empty-state">
        No projects available.
      </div>
    `;
  }

  return `
    <div class="project-list">

      ${items.map(item => {

        if (typeof item !== "object") {

          return `
            <div class="project-card">

              <div class="project-title">
                🚀 ${escapeHtml(item)}
              </div>

            </div>
          `;
        }

        const technologies =
          item.technologies ||
          item.technology ||
          [];

        return `
          <div class="project-card">

            <div class="project-title">
              🚀
              ${escapeHtml(
                item.name ||
                item.title ||
                "Project"
              )}
            </div>

            ${
              item.description
                ? `
                  <div class="project-description">
                    ${escapeHtml(item.description)}
                  </div>
                `
                : ""
            }

            ${
              technologies.length
                ? `
                  <div class="project-technologies">

                    ${technologies.map(
                      technology => `
                        <span class="project-tag">
                          ${escapeHtml(technology)}
                        </span>
                      `
                    ).join("")}

                  </div>
                `
                : ""
            }

          </div>
        `;

      }).join("")}

    </div>
  `;
}


// =========================================================
// CERTIFICATIONS
// =========================================================

function renderCertifications(items) {

  if (!items || !items.length) {
    return `
      <div class="empty-state">
        No certifications available.
      </div>
    `;
  }

  return `
    <div class="certification-list">

      ${items.map(item => {

        if (typeof item === "object") {

          const name =
            item.name ||
            item.title ||
            item.certification ||
            "Certification";

          const issuer =
            item.issuer ||
            item.organization ||
            item.provider ||
            "";

          return `
            <div class="certification-card">

              <div class="certification-icon">
                🏆
              </div>

              <div class="certification-content">

                <div class="certification-title">
                  ${escapeHtml(name)}
                </div>

                ${
                  issuer
                    ? `
                      <div class="certification-issuer">
                        ${escapeHtml(issuer)}
                      </div>
                    `
                    : ""
                }

              </div>

            </div>
          `;
        }

        const text = String(item);

        let name = text;
        let issuer = "";

        if (text.includes(" – ")) {
          const parts = text.split(" – ");
          name = parts[0];
          issuer = parts.slice(1).join(" – ");
        } else if (text.includes(" - ")) {
          const parts = text.split(" - ");
          name = parts[0];
          issuer = parts.slice(1).join(" - ");
        }

        return `
          <div class="certification-card">

            <div class="certification-icon">
              🏆
            </div>

            <div class="certification-content">

              <div class="certification-title">
                ${escapeHtml(name)}
              </div>

              ${
                issuer
                  ? `
                    <div class="certification-issuer">
                      ${escapeHtml(issuer)}
                    </div>
                  `
                  : ""
              }

            </div>

          </div>
        `;

      }).join("")}

    </div>
  `;
}


// =========================================================
// PARSE RESUME
// =========================================================

parseResumeBtn.addEventListener(
  "click",
  async () => {

    if (!resumeFile.files.length) {

      uploadStatus.textContent =
        "Please choose a PDF or TXT resume.";

      return;
    }

    const file =
      resumeFile.files[0];

    uploadStatus.textContent =
      "Parsing resume with Gemini...";

    parseResumeBtn.disabled = true;

    try {

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      const response =
        await fetch(
          "/api/resumes/upload",
          {
            method: "POST",
            body: formData
          }
        );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Resume parsing failed."
        );
      }

      currentCandidateId =
        data.candidate_id;

      displayCandidate(
        data.candidate
      );

      analyzeBtn.disabled = false;

      uploadStatus.textContent =
        "Resume parsed successfully.";

      await refreshRanking();

    } catch (error) {

      console.error(error);

      uploadStatus.textContent =
        error.message;

    } finally {

      parseResumeBtn.disabled =
        false;
    }
  }
);


// =========================================================
// DISPLAY CANDIDATE
// =========================================================

function displayCandidate(candidate) {

  candidateDetails.innerHTML = `

    <div class="candidate-header">

      <div>

        <h3>
          ${escapeHtml(
            candidate.name ||
            "Unknown Candidate"
          )}
        </h3>

        <p>
          ${escapeHtml(
            candidate.email ||
            "No email provided"
          )}
        </p>

        <p>
          ${escapeHtml(
            candidate.phone ||
            "No phone provided"
          )}
        </p>

      </div>

    </div>


    <!-- SKILLS -->

    <div class="info-section">

      <h3>
        Skills
      </h3>

      <div class="tags">

        ${tags(
          candidate.skills,
          "skill"
        )}

      </div>

    </div>


    <!-- EDUCATION -->

    <div class="info-section">

      <h3>
        Education
      </h3>

      ${renderEducation(
        candidate.education
      )}

    </div>


    <!-- EXPERIENCE -->

    <div class="info-section">

      <h3>
        Experience
      </h3>

      ${renderExperience(
        candidate.experience
      )}

    </div>


    <!-- PROJECTS -->

    <div class="info-section">

      <h3>
        Projects
      </h3>

      ${renderProjects(
        candidate.projects
      )}

    </div>


    <!-- CERTIFICATIONS -->

    <div class="info-section">

      <h3>
        Certifications
      </h3>

      ${renderCertifications(
        candidate.certifications
      )}

    </div>

  `;
}


// =========================================================
// ANALYZE MATCH
// =========================================================

analyzeBtn.addEventListener(
  "click",
  async () => {

    if (!currentCandidateId) {

      matchStatus.textContent =
        "Please parse a resume first.";

      return;
    }

    if (!jobDescription.value.trim()) {

      matchStatus.textContent =
        "Please enter a job description.";

      return;
    }

    analyzeBtn.disabled = true;

    matchStatus.textContent =
      "Analyzing candidate against the job description...";

    try {

      const formData =
        new FormData();

      formData.append(
        "candidate_id",
        currentCandidateId
      );

      formData.append(
        "job_title",
        jobTitle.value ||
        "Untitled Job"
      );

      formData.append(
        "job_description",
        jobDescription.value
      );

      const response =
        await fetch(
          "/api/match",
          {
            method: "POST",
            body: formData
          }
        );

      const data =
        await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Matching failed."
        );
      }

      displayMatch(
        data
      );

      matchStatus.textContent =
        "Analysis completed successfully.";

      await refreshRanking();

    } catch (error) {

      console.error(error);

      matchStatus.textContent =
        error.message;

    } finally {

      analyzeBtn.disabled = false;
    }
  }
);


// =========================================================
// DISPLAY MATCH
// =========================================================

function displayMatch(result) {

  const score =
    Number(
      result.score
    ).toFixed(1);

  matchResult.innerHTML = `

    <div class="match-score">

      <div class="score-number">
        ${score}
      </div>

      <div class="score-label">
        / 10 Match
      </div>

    </div>


    <div class="match-section strengths">

      <h3>
        Strengths
      </h3>

      ${renderList(
        result.strengths
      )}

    </div>


    <div class="match-section gaps">

      <h3>
        Skill Gaps
      </h3>

      ${renderList(
        result.skill_gaps
      )}

    </div>


    <div class="match-section">

      <h3>
        AI Justification
      </h3>

      <p class="justification">
        ${escapeHtml(
          result.justification ||
          "No justification provided."
        )}
      </p>

    </div>

  `;
}


// =========================================================
// REFRESH RANKING
// =========================================================

refreshRankingBtn.addEventListener(
  "click",
  refreshRanking
);


async function refreshRanking() {

  try {

    const response =
      await fetch(
        "/api/matches"
      );

    const matches =
      await response.json();

    if (!matches.length) {

      ranking.innerHTML = `
        <div class="empty-state">
          No candidates ranked yet.
        </div>
      `;

      return;
    }

    ranking.innerHTML =
      matches.map(
        (match, index) => `

        <div class="ranking-row">

          <div class="rank-position">
            #${index + 1}
          </div>

          <div class="rank-info">

            <strong>
              ${escapeHtml(
                match.candidate_name
              )}
            </strong>

            <div>
              ${escapeHtml(
                match.job_title
              )}
            </div>

          </div>

          <div class="rank-score">

            ${Number(
              match.score
            ).toFixed(1)}/10

          </div>

        </div>

      `
      ).join("");

  } catch (error) {

    console.error(
      "Ranking error:",
      error
    );
  }
}


// =========================================================
// INITIAL LOAD
// =========================================================

refreshRanking();