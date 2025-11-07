# TODO

In this file you can find things that should be done in this project. It is not the final list. It consists of items that were found to be bugged or poorly implemented. Those items should probably be converted into **GitHub Issues**.

- [TODO](#todo)
  - [Backend](#backend)
  - [Cloud](#cloud)
  - [Project](#project)

## Backend

- [ ] Project does not have documented dependencies
  
  - **Source**: `apps/backend/.`
  - **What is wrong**: Because there is poor documentation on the startup and installation process, it is hard to even launch the backend. Additionally, the number of dependencies is huge.
  - **Why is it bad**: We want the project to be easy to launch for people that download our project. Otherwise interest drops and frustration rises. Having such a large number of dependencies makes the project initialization process very long and is not memory efficient.
  - **Proposed solution**: Use tools like `uv` to automate the process of venv creation and `make` for easier interactions with the backend. All project dependencies should be examined to confirm they are needed.

  > [!Note]
  > Work is in progress. `uv` project was created, you can find `pyproject.toml` and `uv.lock` files with dependencies in the project as well as `.python-version` file.

---

- [ ] Restaurants stored in a pickle file

  - **Source**: `apps/backend/src/backend/get_restaurants.py`
  - **What is wrong**: Recommendations of nearby restaurants are stored in a pickle file that is expected to live inside the project. In addition, this pickle file is not included in the repository.
  - **Why is it bad**: Storing a static set of restaurants is bad because it requires additional work to keep this file updated. This file will grow in size very quickly.
  - **Proposed solution**: Use Google Places API for nearby restaurant searches as we already use this API in the project.

---

- [ ] No code convention

  - **Source**: `apps/backend/.`
  - **What is wrong**: The project lacks a naming convention and clear structure. Additionally, it uses two languages for documentation and naming (Polish and English).
  - **Why is it bad**: We should stick to industry standards. It also helps new developers start working on the project quickly instead of spending dozens of hours just learning the codebase.
  - **Proposed solution**: The project should be restructured. There should be required use of linting, type checking, and formatting tools. Use default Python naming conventions (`snake_case` and `TitleCase`). Only English should be used in the project.

---

- [ ] Project does not contain all files needed for startup

  - **Source**: `apps/backend/.`
  - **What is wrong**: There are multiple files such as the spaCy English small model that are not installed during initialization, and there is no mention in the documentation about that requirement.
  - **Why is it bad**: Having these hidden dependencies builds frustration in developers and users. Sometimes these dependencies can cause a bug that is very hard to debug.
  - **Proposed solution**: All dependencies should be added into the `pyproject.toml` file, or there should be an automated macro for downloading them.

---

- [ ] No `.env.example` file

  - **Source**: `apps/backend/.env.example`
  - **What is wrong**: There is no example of the expected environment variables.
  - **Why is it bad**: We want the project to be easy to launch for people that download our project. Otherwise interest drops and frustration rises. Having such a large number of dependencies makes the project initialization process very long and is not memory efficient.
  - **Proposed solution**: Use tools like `uv` to automate the process of venv creation and `make` for easier interactions with the backend. All project dependencies should be examined if they are needed.

  > [!Note]
  > Work is in progress.

---

- [ ] Backend is running on the development server

  - **Source**: `apps/backend/main.py`
  - **What is wrong**: Even when starting the server, it states that this shouldn't be used in production.
  - **Why is it bad**: Development servers are unstable and can be buggy sometimes.
  - **Proposed solution**: We should change the entrypoint for the server to use a production-ready server.

---

## Cloud

- [ ] No documentation for the cloud part of the project

  - **What is wrong**: The project lacks a naming convention and clear structure. Additionally, it uses two languages for documentation and naming (Polish and English).
  - **Why is it bad**: We should stick to industry standards. It also helps new developers start working on the project quickly instead of spending dozens of hours just learning the codebase.
  - **Proposed solution**: The project should be restructured. There should be required use of linting, type checking, and formatting tools. Use default Python naming conventions (`snake_case` and `TitleCase`). Only English should be used in the project.

---

- [ ] Two separate accounts in Firebase

  - **What is wrong**: The author of the project created two separate Firebase accounts (probably as a workaround for one free database).
  - **Why is it bad**: There is no reason for this kind of workaround as we need the Blaze plan either way (because enabling Google Places API will cause it).
  - **Proposed solution**: Merge the two separate Firebase accounts into one.

---

- [ ] No Terraform file

  - **What is wrong**: Right now the cloud infrastructure is not easily reproducible. There is no Terraform file in the project.
  - **Why is it bad**: If someone causes any cloud service to fail there is no fallback other than manually fixing it. If we had a Terraform file, this job would be reduced to a few commands.
  - **Proposed solution**: Create a Terraform file for this project.

---

## Project

- [ ] No Dockerfile and Docker Compose

  - **What is wrong**: There is no Dockerfile. Every component needs to be launched separately.
  - **Why is it bad**: Setting up a system with so many components is time consuming.
  - **Proposed solution**: Create `Dockerfile` and `docker-compose.yml` to set up and deploy the whole system.
