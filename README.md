# CTMS API

This is a work-in-progress for the Contact Management System (CTMS) API.
The API is read-only with some sample test contacts with fake data:

* ``93db83d4-4119-4e0c-af87-a713786fa81d``: sample contact with:
  - email ``ctms-user@example.com``
  - SalesForce ``001A000001aABcDEFG``
  - Basket token ``142e20b6-1ef5-43d8-b5f4-597430e956d7``

Next features for the read-only version:

* [ ] Review rounds
* [ ] Flesh out the rest of the read-only API
* [ ] Implement the ``/identity`` APIs with alternate IDs
* [ ] Add more sample contacts

Future features:

* [ ] Backing database for development
* [ ] Create / Update / Delete endpoints
* [ ] Convert template docs to CTMS docs

# Based on containerized-microservice-template

[containerized-microservice-template](https://github.com/mozilla-it/containerized-microservice-template)
is a github repo template using python3 with:

 - Using FastAPI framework (Pydantic, Swagger, included)
 - BDD testing strategies (using Gherkin and Behave)
 - Python package control through **poetry**
 - **Pre-commit** for detecting secrets, typing, linting (Detect-Secrets,Mypy, Black)
 - Containerization through **Docker**
 - Build Pipeline through **GCP's Cloudbuild**
 - Deployment yaml's for k8s

---
## Template Docs

[View All Docs](./guides/)
- [Auto Documentation Setup](guides/auto_documentation.md)
- [Deployment Guide](guides/deployment_guide.md)
- [Developer Setup](guides/developer_setup.md)
- [First Steps](guides/first_steps.md)
- [Testing Strategy](guides/testing_strategy.md)
- [Git Strategy](guides/git_strategy.md)

---
## Prerequisites

Please ensure following the [Developer Setup](guides/developer_setup.md) before developing \
for this project to ensure correct environment setup.

Then please view the [First Steps](guides/first_steps.md) and follow along for running \
the server, scripts, and docker.

[Others docs here as well](./guides/).

---
## Project Structure

The project is structured with the following in mind:

- docs/
    - Auto-generated Sphinx docs live here.
- guides/
    - Documentation to guide others around the project interactions
- ctms/
    - Operational source code exists here
    - .../app.py
        - FastAPI Handling of HTTP Requests and routing to services
    - .../models.py
        - Pydantic Models for Data Modeling, and Contract Validation
- tests/behave/
    - BDD feature testing with Behave and Gherkin feature files
- tests/resources/
    - Resources of various files types, exist here

---
## References & Regards
- https://github.com/tiangolo/fastapi
- https://github.com/samuelcolvin/pydantic
- https://github.com/michael0liver/python-poetry-docker-example
