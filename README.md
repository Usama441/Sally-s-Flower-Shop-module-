# Sally's Flower Shop

An Odoo 19 learning module developed in small, reviewable steps.

## Current step: the flower model

The model `flower.shop.flower` stores a flower's common name, scientific name,
season dates, watering interval in days, and watering amount in millilitres.
The common name is required and is used as the record's display name.

- `_name` registers the model with Odoo.
- `_description` gives it a readable description.
- `_rec_name` selects the field used to display the record's name.
- Both `__init__.py` files import the model so Odoo loads it.
- `__manifest__.py` declares the module, its Odoo version, and dependencies.

Views, menus, access permissions, and business validation will be added in later
steps as the assessment requirements become available. At this stage, ordinary
users have no access to flower records and there is no Flower Shop menu.

## Development checks

From this repository directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/ruff check .
.venv/bin/ruff format --check .
python3 -m compileall -q __init__.py __manifest__.py models
```

## Small-change Git workflow

Use one branch per task. Review the diff, run the checks, commit the related
files, and push that branch to GitHub. Open a pull request into `main` and wait
for CI to pass before merging.

```sh
git switch -c feat/next-flower-shop-step
git diff
# Run the development checks above, then stage only the related files.
git add models/flower.py
git commit -m "feat: describe the completed flower model change"
git push -u origin HEAD
```

GitHub Actions runs Python lint and formatting checks, then installs and
upgrades the module in Odoo 19 against a disposable PostgreSQL database on every
push and pull request. The repository root is mounted as `flower_shop` so the
technical module name stays correct regardless of the GitHub repository name.
The database password in the workflow is only for its disposable CI service.

Deployment will be configured after a staging environment is identified.

References: [Odoo module manifests](https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html)
and [GitHub PostgreSQL services](https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers).
