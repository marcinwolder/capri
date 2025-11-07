# TODO

In this file you can find things that should be done in this project. It is not the final lis. It consists of things that were find as bugged or poorly implemented. Those things should probably be converted into **GitHub Issues**.

- [TODO](#todo)
  - [Backend](#backend)
  - [Cloud](#cloud)
  - [Project](#project)

## Backend

- [ ] Project do not have dependencies documented
  
  - **Source**: `apps/backend/.`
  - **What is wrong**: Because there is poor documentation on startup and instalation process it is had to even launch the backend. Additionaly number of dependencies is huge.
  - **Why is it bad**: We want the project to be easy to launch for people that download our project. Otherwise interest drops and flustration raises. having this big number of dependencies makes a project initialization process very long and is not memory efficient.
  - **Proposition of sollution**: Use tools like `uv` to automate proces of venv creation and `make` for easier interacions with backend. All project dependencies should be examined if they are needed.

  > [!Note]
  > Work is in progress. `uv` project was created, you can find `pyproject.toml` and `uv.lock` files with dependencies in the project as well as `.python-version` file.

---

- [ ] Restaurants stored in pickle file

  - **Source**: `apps/backend/src/backend/get_restaurants.py`
  - **What is wrong**: Recommendations of nearby resturants are stored in pickle file that is expected to live inside the project. In addition this pickle file is not included in the repository.
  - **Why is it bad**: Storing static number of restaurants is bad because it requires from us additional work of keeping this file updated. This file will grow in size really fast.
  - **Proposition of sollution**: Use Google Places API for nearby restaurants search as we already use this API in the project.

---

- [ ] No code convention

  - **Source**: `apps/backend/.`
  - **What is wrong**: Project lacks a naming convention and project structure. Additionaly it uses 2 languages for documentation and naming (Polish and English).
  - **Why is it bad**: We should stick to industry standards. It also helps new developers to start working on project quicly insted of spending dozen of hours to just learn the codebase.
  - **Proposition of sollution**: Project should be resturcured. There should be a required use of linting, type checking, formatting tools. Using default python naming convetion (`snake_case` and `TitleCase`). There should be only English used in the project.

---

- [ ] Project do not contain all files needed for startup

  - **Source**: `apps/backend/.`
  - **What is wrong**: There are multiple files such as scypy english small model that are not installed during initialization and there is no mention in the documentation about that requirement.
  - **Why is it bad**: having this hidden dependencies build flustration in developers and users. Sometimes those kind of dependencies can cause a bug that is very hard to debug.
  - **Proposition of sollution**: All dependencies should be added into `pyproject.toml` file or there should be automated makro for donwloading them.

---

- [ ] No `.env.example` file

  - **Source**: `apps/backend/.env.example`
  - **What is wrong**: There is no example of expected envirnment variables.
  - **Why is it bad**: We want the project to be easy to launch for people that download our project. Otherwise interest drops and flustration raises. having this big number of dependencies makes a project initialization process very long and is not memory efficient.
  - **Proposition of sollution**: Use tools like `uv` to automate proces of venv creation and `make` for easier interacions with backend. All project dependencies should be examined if they are needed.

  > [!Note]
  > Work is in progress.

  ---

- [ ] Backend is running on developer server

  - **Source**: `apps/backend/main.py`
  - **What is wrong**: Even while starting the server it says that this shouldn't be used in production.
  - **Why is it bad**: Development servers are unstable and can be buggy sometimes.
  - **Proposition of sollution**: We should change the entrypoint for the server to use production ready server.

---

## Cloud

- [ ] No documentation about cloud part of the project

  - **What is wrong**: Project lacks a naming convention and project structure. Additionaly it uses 2 languages for documentation and naming (Polish and English).
  - **Why is it bad**: We should stick to industry standards. It also helps new developers to start working on project quicly insted of spending dozen of hours to just learn the codebase.
  - **Proposition of sollution**: Project should be resturcured. There should be a required use of linting, type checking, formatting tools. Using default python naming convetion (`snake_case` and `TitleCase`). There should be only English used in the project.

---

- [ ] Two separate accounts in Firebase

  - **What is wrong**: Author of the project created two separate Firebase accounts (propably as a workaround for one free database).
  - **Why is it bad**: There are no reason for this kind of workaround as we need Blaze plan either way (cenabling Google Places API will couse it).
  - **Proposition of sollution**: Merge two separate Firebase accounts into one.

---

- [ ] No terraform file

  - **What is wrong**: Right now cloud infrastructure is not easly reproducable. There is no terraform file in the project.
  - **Why is it bad**: If someone will couse any cloud service to fail there is no backup than to manually fix it. If we had a terraform file, this job is being reduced into few commands.
  - **Proposition of sollution**: Create a terraform file for this project.

---

## Project

- [ ] No Dockerfile and docker compose

  - **What is wrong**: There is no Dockerfile. Every component needs to be launched separetly.
  - **Why is it bad**: Setting up a system with so many components is time consuming.
  - **Proposition of sollution**: Create `Dockerfile` and `docker-compose.yml` it setup and deploy whole system.
