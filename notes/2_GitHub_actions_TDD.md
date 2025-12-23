## Configuring GitHub Actions

### What GitHub Actions?
- automation tool
- Similar to Travis-CI, GitLab CI/CD, Jenkins
- Run jobs when code changes
- Common uses:
    - Depolyument (not be covered in this course)
    - Code linting
    - Unit tests
- How it works
    - Trigger (push to github) ->Job (Run unit tests) -> Result (success/fail)
  
###  Configuration

How?
- Creatw a config file at `.github/workflow/checks.yaml`, the name of the file doesn't matter.
  - Set trigger as push, meaning everytime we push the code to out github repo, it will trigger github actions
  - Add steps for running testing and linting
- Configure DockerHub authentication. (Done in [project setup section](notes/1_Proj_setup.md))