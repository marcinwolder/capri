# TODO

In this file you can find things that should be done in this project. It is not the final list. It consists of items that were found to be bugged or poorly implemented. Those items should probably be converted into **GitHub Issues**.

- [TODO](#todo)
	- [Backend](#backend)
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
