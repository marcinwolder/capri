# TODO

In this file you can find things that should be done in this project. It is not the final list. It consists of items that were found to be bugged or poorly implemented. Those items should probably be converted into **GitHub Issues**.

- [TODO](#todo)
	- [Backend](#backend)
	- [Frontend](#frontend)
	- [Project](#project)

## Backend

- [ ] Only one LLM provider available

  - **Source**: `apps/backend/src/.`
  - **What is wrong**: The backend supports a single LLM path and cannot switch to alternatives like Gemini.
  - **Why is it bad**: Limits experimentation, fallbacks, and comparisons when models degrade or drift.
  - **Proposed solution**: Add a provider abstraction with configuration to choose between LLaMA and Gemini; update env vars and routing.

---

- [ ] No baseline LLM comparison with minimal prompt

  - **Source**: `apps/backend/.`
  - **What is wrong**: There is no captured comparison between the current LLM and an alternative run after holidays; prompts are not standardized or minimal.
  - **Why is it bad**: Hard to evaluate quality, communicate changes, or justify switching providers.
  - **Proposed solution**: Define a minimal prompt suite, run it across both LLMs, and record outputs for review.

## Frontend

- [ ] Trip generation loading flow lacks step-by-step checklist

  - **Source**: `apps/frontend/src/.`
  - **What is wrong**: During trip generation the UI only shows a generic loader and hides what is happening behind the scenes.
  - **Why is it bad**: Users wait without feedback and miss an opportunity to feel confident about progress.
  - **Proposed solution**: When a trip is generating, show an animated, mocked checklist of ~5 sequential steps (e.g., analyzing preferences, selecting attractions/POIs, arranging days, applying POI algorithms/adjusting add-remove-edit, generating descriptions with LLM). Each step should display a brief randomized duration within defined ranges (early steps ~0.5–2.5s, later steps up to the max expected generation time) so the sequence feels lively while keeping total time realistic.

## Project

- [ ] Build-and-run handoff not streamlined

  - **Source**: `.`
  - **What is wrong**: Packaging the app for others is manual; recipients lack a simple build/run path.
  - **Why is it bad**: Increases friction for reviewers or stakeholders who need to start the app quickly.
  - **Proposed solution**: Provide a repeatable build artifact or script plus concise run instructions so others can launch easily.

---

- [ ] Setup remains overly complex

  - **Source**: `.`
  - **What is wrong**: Current initialization requires many steps and decisions.
  - **Why is it bad**: Onboarding slows down and increases likelihood of misconfiguration.
  - **Proposed solution**: Simplify defaults, reduce required steps, and document the minimal path to a working environment.

---

- [ ] Docker requirement not justified

  - **Source**: `.`
  - **What is wrong**: It is unclear whether Docker is required or optional.
  - **Why is it bad**: Uncertainty causes extra setup and potential blockers for environments where Docker is restricted.
  - **Proposed solution**: Clarify when Docker is necessary, provide justification, and document alternatives if feasible.

---

- [ ] Stakeholder cannot view the app easily

  - **Source**: `.`
  - **What is wrong**: There is no guaranteed way for the stakeholder to see the application running.
  - **Why is it bad**: Feedback loops slow down and acceptance may be blocked.
  - **Proposed solution**: Publish a demo build or hosted preview and share clear access instructions.

---

- [ ] User documentation missing

  - **Source**: `README.md`
  - **What is wrong**: There is no user-facing guide that explains how to operate the application.
  - **Why is it bad**: End users cannot self-serve, leading to support overhead and confusion.
  - **Proposed solution**: Create user documentation that covers setup, core flows, and troubleshooting.

---

- [ ] Example input files absent

  - **Source**: `.`
  - **What is wrong**: No sample input files are available to showcase typical usage.
  - **Why is it bad**: Harder to test, demo, or validate behaviors consistently.
  - **Proposed solution**: Add a small set of curated input examples with descriptions of expected outputs.

---

- [ ] LLM prompt summary email not prepared

  - **Source**: `.`
  - **What is wrong**: There is no approved email summarizing the prompt sent to the LLM.
  - **Why is it bad**: Stakeholders cannot review or sign off on prompt wording before use.
  - **Proposed solution**: Draft an approval email that outlines the LLM prompt, circulate it, and capture sign-off.

---

- [ ] Windows compatibility unverified

  - **Source**: `.`
  - **What is wrong**: The application has not been validated on Windows.
  - **Why is it bad**: Windows users may encounter blockers that are undiscovered on other platforms.
  - **Proposed solution**: Test the full stack on Windows, document steps, and address platform-specific issues.
